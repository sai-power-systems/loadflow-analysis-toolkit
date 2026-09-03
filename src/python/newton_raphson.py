import numpy as np
import pandas as pd

from system_data import bus_data, line_data, dd
from ybus import compute_ybus
from jacobian import build_jacobian, calculate_injected_power

def initialize_voltage(bus_data):
	"""Create the initial complex voltage vector from the bus data."""
	voltage_magnitude = bus_data["V_mag"].fillna(1.0).to_numpy(dtype=float)
	voltage_angle = bus_data["V_ang"].fillna(0.0).to_numpy(dtype=float)

	return voltage_magnitude * np.exp(1j * np.radians(voltage_angle))


def calculate_mismatch(
	voltage,
	ybus,
	specified_p,
	specified_q,
	angle_buses,
	magnitude_buses,
):
	"""Return active- and reactive-power mismatches in solver order."""
	calculated_p, calculated_q = calculate_injected_power(voltage, ybus)

	p_mismatch = specified_p[angle_buses] - calculated_p[angle_buses]
	q_mismatch = specified_q[magnitude_buses] - calculated_q[magnitude_buses]

	return np.concatenate((p_mismatch, q_mismatch))


def apply_voltage_update(
	voltage,
	correction,
	angle_buses,
	magnitude_buses,
	pv_buses,
	slack_buses,
	bus_data,
	damping_factor,
):
	"""Apply a damped correction and restore PV/slack constraints."""
	angle_count = len(angle_buses)
	voltage_angle = np.angle(voltage).copy()
	voltage_magnitude = np.abs(voltage).copy()

	voltage_angle[angle_buses] += (
		damping_factor * correction[:angle_count]
	)
	voltage_magnitude[magnitude_buses] += (
		damping_factor * correction[angle_count:]
	)

	pv_magnitudes = (
		bus_data.loc[pv_buses, "V_mag"]
		.fillna(1.0)
		.to_numpy(dtype=float)
	)
	voltage_magnitude[pv_buses] = pv_magnitudes

	slack_index = slack_buses[0]
	slack_magnitude = bus_data.loc[slack_index, "V_mag"]
	if pd.isna(slack_magnitude):
		slack_magnitude = 1.0

	voltage_magnitude[slack_index] = float(slack_magnitude)
	voltage_angle[slack_index] = 0.0

	if (
		np.any(voltage_magnitude <= 0.0)
		or not np.all(np.isfinite(voltage_magnitude))
		or not np.all(np.isfinite(voltage_angle))
	):
		return None

	return voltage_magnitude * np.exp(1j * voltage_angle)


def newton_raphson(
	bus_data,
	ybus,
	base_mva,
	tolerance=1e-6,
	max_iterations=300,
):
	"""Solve the load flow using a damped Newton-Raphson method."""
	bus_types = bus_data["type"].to_numpy()
	pq_buses = np.flatnonzero(bus_types == "PQ")
	pv_buses = np.flatnonzero(bus_types == "PV")
	slack_buses = np.flatnonzero(bus_types == "SLACK")

	if len(slack_buses) != 1:
		raise ValueError("The system must contain exactly one slack bus.")

	angle_buses = np.concatenate((pv_buses, pq_buses))
	magnitude_buses = pq_buses
	voltage = initialize_voltage(bus_data)

	specified_p = bus_data["P_MW"].to_numpy(dtype=float) / base_mva
	specified_q = bus_data["Q_MVAR"].to_numpy(dtype=float) / base_mva

	for iteration in range(max_iterations):
		mismatch = calculate_mismatch(
			voltage,
			ybus,
			specified_p,
			specified_q,
			angle_buses,
			magnitude_buses,
		)
		maximum_mismatch = np.max(np.abs(mismatch))

		# print(
		# 	f"Iteration {iteration + 1:03d}: "
		# 	f"mismatch = {maximum_mismatch:.6e}"
		# )

		if maximum_mismatch < tolerance:
			return voltage, iteration + 1, maximum_mismatch

		jacobian = build_jacobian(
			voltage,
			ybus,
			pq_buses,
			pv_buses,
		)

		try:
			correction = np.linalg.solve(jacobian, mismatch)
		except np.linalg.LinAlgError as error:
			raise np.linalg.LinAlgError(
				"The Jacobian is singular. Check network connectivity "
				"and bus classification."
			) from error

		damping_factor = 1.0
		accepted = False

		while damping_factor >= 1e-6:
			candidate_voltage = apply_voltage_update(
				voltage,
				correction,
				angle_buses,
				magnitude_buses,
				pv_buses,
				slack_buses,
				bus_data,
				damping_factor,
			)

			if candidate_voltage is None:
				damping_factor *= 0.5
				continue

			candidate_mismatch = calculate_mismatch(
				candidate_voltage,
				ybus,
				specified_p,
				specified_q,
				angle_buses,
				magnitude_buses,
			)
			candidate_error = np.max(np.abs(candidate_mismatch))

			if candidate_error < maximum_mismatch:
				voltage = candidate_voltage
				accepted = True
				break

			damping_factor *= 0.5

		if not accepted:
			raise RuntimeError(
				"Newton-Raphson could not find a valid correction that "
				"reduces the mismatch."
			)

	raise RuntimeError(
		f"Newton-Raphson did not converge after {max_iterations} "
		f"iterations. Final mismatch: {maximum_mismatch:.6e}"
	)


def run_load_flow():
	"""Build the network, solve it, and return the result table."""
	ybus = compute_ybus(
		bus_data,
		line_data,
		dd.transformer_data,
	)

	voltage, iterations, final_mismatch = newton_raphson(
		bus_data,
		ybus,
		base_mva=dd.base_mva,
	)

	current = ybus @ voltage
	power = voltage * np.conj(current)

	resultnr = pd.DataFrame({
		"Bus": bus_data["bus_no"].to_numpy(),
		"V_mag": np.abs(voltage),
		"V_ang_deg": np.degrees(np.angle(voltage)),
		"I_real": current.real,
		"I_imag": current.imag,
		"P_MW": power.real * dd.base_mva,
		"Q_MVAr": power.imag * dd.base_mva,
	})

	# print()
	# print(f"Converged after {iterations} iterations")
	# print(f"Final mismatch: {final_mismatch:.6e}")
	# print()
	

	return [resultnr,iterations,final_mismatch]


if __name__ == "__main__":
	print("Newton-Raphson Load Flow Results")
	print("--------------------------------")
	run_load_flow()
