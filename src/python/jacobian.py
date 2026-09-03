import numpy as np

from system_data import bus_data, line_data, dd
from ybus import compute_ybus


def calculate_injected_power(voltage, ybus):
    """Return calculated active and reactive bus-power injections."""
    current = ybus @ voltage
    apparent_power = voltage * np.conj(current)
    return apparent_power.real, apparent_power.imag


def build_jacobian(voltage, ybus, pq_buses, pv_buses):
    """
    Build the Newton-Raphson load-flow Jacobian.

    State variables:
        Voltage angles for PV and PQ buses
        Voltage magnitudes for PQ buses
    """
    voltage_magnitude = np.abs(voltage)
    voltage_angle = np.angle(voltage)

    conductance = ybus.real
    susceptance = ybus.imag

    calculated_p, calculated_q = calculate_injected_power(voltage, ybus)

    angle_buses = np.concatenate((pv_buses, pq_buses))
    magnitude_buses = pq_buses

    h = np.zeros((len(angle_buses), len(angle_buses)))
    n = np.zeros((len(angle_buses), len(magnitude_buses)))
    m = np.zeros((len(magnitude_buses), len(angle_buses)))
    l = np.zeros((len(magnitude_buses), len(magnitude_buses)))

    for row, i in enumerate(angle_buses):
        for column, j in enumerate(angle_buses):
            if i == j:
                h[row, column] = (
                    -calculated_q[i]
                    - susceptance[i, i] * voltage_magnitude[i] ** 2
                )
            else:
                angle_difference = voltage_angle[i] - voltage_angle[j]
                h[row, column] = voltage_magnitude[i] * voltage_magnitude[j] * (
                    conductance[i, j] * np.sin(angle_difference)
                    - susceptance[i, j] * np.cos(angle_difference)
                )

        for column, j in enumerate(magnitude_buses):
            if i == j:
                n[row, column] = (
                    calculated_p[i] / voltage_magnitude[i]
                    + conductance[i, i] * voltage_magnitude[i]
                )
            else:
                angle_difference = voltage_angle[i] - voltage_angle[j]
                n[row, column] = voltage_magnitude[i] * (
                    conductance[i, j] * np.cos(angle_difference)
                    + susceptance[i, j] * np.sin(angle_difference)
                )

    for row, i in enumerate(magnitude_buses):
        for column, j in enumerate(angle_buses):
            if i == j:
                m[row, column] = (
                    calculated_p[i]
                    - conductance[i, i] * voltage_magnitude[i] ** 2
                )
            else:
                angle_difference = voltage_angle[i] - voltage_angle[j]
                m[row, column] = -voltage_magnitude[i] * voltage_magnitude[j] * (
                    conductance[i, j] * np.cos(angle_difference)
                    + susceptance[i, j] * np.sin(angle_difference)
                )

        for column, j in enumerate(magnitude_buses):
            if i == j:
                l[row, column] = (
                    calculated_q[i] / voltage_magnitude[i]
                    - susceptance[i, i] * voltage_magnitude[i]
                )
            else:
                angle_difference = voltage_angle[i] - voltage_angle[j]
                l[row, column] = voltage_magnitude[i] * (
                    conductance[i, j] * np.sin(angle_difference)
                    - susceptance[i, j] * np.cos(angle_difference)
                )

    return np.block([
        [h, n],
        [m, l],
    ])


if __name__ == "__main__":
    ybus = compute_ybus(bus_data, line_data)

    pq_buses, pv_buses, slack_buses = dd.classify_buses()

    voltage = (
        bus_data["V_mag"].to_numpy(dtype=float)
        * np.exp(1j * np.radians(bus_data["V_ang"].to_numpy(dtype=float)))
    )

    jacobian = build_jacobian(
        voltage,
        ybus,
        pq_buses,
        pv_buses,
    )

    print("Jacobian shape:", jacobian.shape)
    print(jacobian)