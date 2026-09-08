import numpy as np
import pandas as pd
from gauss_seidel import gauss_seidel
from newton_raphson import run_load_flow
from system_data import dd, line_data


def line_flows_and_losses(voltage, line_data, base_mva=100.0):
    """Return branch flows and losses as NumPy arrays."""
    lines = line_data.to_dict("records")
    flows_dtype = [
        ("from_bus", int),
        ("to_bus", int),
        ("P_from_MW", float),
        ("Q_from_MVAr", float),
        ("P_to_MW", float),
        ("Q_to_MVAr", float),
    ]

    losses_dtype = [
        ("from_bus", int),
        ("to_bus", int),
        ("P_loss_MW", float),
        ("Q_loss_MVAr", float),
    ]

    flows = np.zeros(len(lines), dtype=flows_dtype)
    losses = np.zeros(len(lines), dtype=losses_dtype)
    for index, line in enumerate(lines):
        from_bus = int(line["from_bus"]) - 1
        to_bus = int(line["to_bus"]) - 1
        impedance = complex(float(line["R1"]), float(line["X1"]))
        series_admittance = 1.0 / impedance

        current_from = (voltage[from_bus] - voltage[to_bus]) * series_admittance
        current_to = (voltage[to_bus] - voltage[from_bus]) * series_admittance
        power_from = voltage[from_bus] * np.conj(current_from) * base_mva
        power_to = voltage[to_bus] * np.conj(current_to) * base_mva
        power_loss = power_from + power_to

        flows[index] = (
            from_bus + 1,
            to_bus + 1,
            power_from.real,
            power_from.imag,
            power_to.real,
            power_to.imag,
        )

        losses[index] = (
            from_bus + 1,
            to_bus + 1,
            power_loss.real,
            power_loss.imag,
        )

    return flows, losses


def _build_voltage_vector(results, mag_column, ang_column):
    """Build a complex bus-voltage vector from magnitude/angle tables."""
    magnitude = results[mag_column].to_numpy(dtype=float)
    angle = np.radians(results[ang_column].to_numpy(dtype=float))
    return magnitude * np.exp(1j * angle)


def _format_flows_and_losses(flows, losses):
    """Convert flow and loss arrays into labeled DataFrames."""
    flow_columns = {
        "from_bus": "from",
        "to_bus": "to",
        "P_from_MW": "P_from_MW",
        "Q_from_MVAr": "Q_from_MVAr",
        "P_to_MW": "P_to_MW",
        "Q_to_MVAr": "Q_to_MVAr",
    }
    loss_columns = {
        "from_bus": "from",
        "to_bus": "to",
        "P_loss_MW": "P_loss_MW",
        "Q_loss_MVAr": "Q_loss_MVAr",
    }

    flow_df = pd.DataFrame(flows).rename(columns=flow_columns)
    loss_df = pd.DataFrame(losses).rename(columns=loss_columns)
    return flow_df, loss_df


def calculate_gs_line_flows_and_losses():
    """Calculate branch flows and losses from the Gauss-Seidel solution."""
    gs_results = gauss_seidel()[0]
    gs_voltage = _build_voltage_vector(gs_results, "V_mag_pu", "V_ang_deg")
    gs_flows, gs_losses = line_flows_and_losses(
        gs_voltage,
        line_data,
        dd.base_mva,
    )
    return _format_flows_and_losses(gs_flows, gs_losses)


def calculate_nr_line_flows_and_losses():
    """Calculate branch flows and losses from the Newton-Raphson solution."""
    nr_results = run_load_flow()[0]
    nr_voltage = _build_voltage_vector(nr_results, "V_mag", "V_ang_deg")
    nr_flows, nr_losses = line_flows_and_losses(
        nr_voltage,
        line_data,
        dd.base_mva,
    )
    return _format_flows_and_losses(nr_flows, nr_losses)


def calculate_line_flows_and_losses():
    """Backward-compatible wrapper returning GS and NR tables together."""
    gs_flows, gs_losses = calculate_gs_line_flows_and_losses()
    nr_flows, nr_losses = calculate_nr_line_flows_and_losses()
    return gs_flows, nr_flows, gs_losses, nr_losses


def calculate_method_comparison():
    """Return voltage, current, flow, and loss tables grouped by method."""
    gs_results = gauss_seidel()[0]
    nr_results = run_load_flow()[0]

    gs_flows, gs_losses = calculate_gs_line_flows_and_losses()
    nr_flows, nr_losses = calculate_nr_line_flows_and_losses()

    return {
        "voltage": {
            "gs": gs_results[["Bus", "V_mag_pu", "V_ang_deg"]].copy(),
            "nr": nr_results[["Bus", "V_mag", "V_ang_deg"]].copy(),
        },
        "current": {
            "gs": gs_results[["Bus", "I_pu"]].copy(),
            "nr": nr_results[["Bus", "I_pu"]].copy(),
        },
        "line_flow": {
            "gs": gs_flows,
            "nr": nr_flows,
        },
        "line_loss": {
            "gs": gs_losses,
            "nr": nr_losses,
        },
    }
   


