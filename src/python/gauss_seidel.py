import numpy as np
import pandas as pd
from system_data import bus_data, line_data, gen_data,dd
from ybus import compute_ybus


def gauss_seidel(
    base_mva: float = 100.0, max_iterations: int = 100, tolerance: float = 1e-6
):
    """Executes the Gauss-Seidel load flow analysis on a power system network.

    Parameters:
        base_mva (float): Base MVA of the system (default: 100.0).
        max_iterations (int): Maximum allowable iterations.
        tolerance (float): Convergence threshold for max voltage change.

    Returns:
        tuple: (results_dataframe, iterations_completed, final_error)
    """
    ybus = compute_ybus(bus_data, line_data)
    pq_buses, pv_buses, slack_buses = dd.classify_buses()
    gen_data = gen_data.set_index("bus_no")
    
    # Initialize complex voltage array (pu)
    v_mag = bus_data["V_mag"].to_numpy(dtype=float)
    v_ang = np.radians(bus_data["V_ang"].to_numpy(dtype=float))
    V = v_mag * np.exp(1j * v_ang)

    # Lock slack bus voltages to specified values
    for bus in slack_buses:
        V[bus] = bus_data.loc[bus, "V_mag"] * np.exp(
            1j * np.radians(bus_data.loc[bus, "V_ang"])
        )

    # Iterative solver loop
    for iteration in range(max_iterations):
        previous_V = V.copy()

        # Update PQ Buses
        for i in pq_buses:
            # Convert MW/MVAr to per-unit
            p_spec = bus_data.loc[i, "P_MW"] / base_mva
            q_spec = bus_data.loc[i, "Q_MVAR"] / base_mva
            s_spec = complex(p_spec, q_spec)

            sum_yv = np.dot(ybus[i, :], V) - ybus[i, i] * V[i]
            V[i] = (np.conj(s_spec) / np.conj(V[i]) - sum_yv) / ybus[i, i]

        # Update PV Buses
        for i in pv_buses:
            p_spec = bus_data.loc[i, "P_MW"] / base_mva

            # Calculate reactive power injection (Q_calc)
            i_i = np.dot(ybus[i, :], V)
            q_calc = -np.imag(np.conj(V[i]) * i_i)

            # Enforce reactive power limits (converted to per-unit)
            q_min = gen_data.loc[i, "Qmin_MVAr"] / base_mva
            q_max = gen_data.loc[i, "Qmax_MVAr"] / base_mva
            q_calc = np.clip(q_calc, q_min, q_max)

            s_spec = complex(p_spec, q_calc)
            sum_yv = np.dot(ybus[i, :], V) - ybus[i, i] * V[i]
            v_temp = (np.conj(s_spec) / np.conj(V[i]) - sum_yv) / ybus[i, i]

            # Preserve scheduled magnitude and update angle
            v_set = bus_data.loc[i, "V_mag"]
            V[i] = v_set * np.exp(1j * np.angle(v_temp))

        # Check convergence
        error = np.max(np.abs(V - previous_V))
        if error < tolerance:
            print(f"Gauss-Seidel converged in {iteration + 1} iterations.")
            break
    else:
        print("Warning: Gauss-Seidel did not converge.")

    # Calculate final current injection and power flows
    I = ybus @ V
    S_pu = V * np.conj(I)
    S_mva = S_pu * base_mva

    # Construct final output table
    results = pd.DataFrame(
        {
            "Bus": bus_data["bus_no"].to_numpy(),
            "V_mag_pu": np.abs(V),
            "V_ang_deg": np.degrees(np.angle(V)),
            "I_pu": I,
            "S_MVA": S_mva,
            "P_MW": S_mva.real,
            "Q_MVAr": S_mva.imag,
        }
    )

    return results, iteration + 1, error