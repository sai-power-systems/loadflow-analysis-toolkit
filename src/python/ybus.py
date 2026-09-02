import numpy as np
from system_data import bus_data, line_data

def compute_ybus(bus_data, line_data):
    """
    Compute the Y-bus matrix for the power system.

    Args:
        bus_data (numpy.ndarray): The bus data array.
        line_data (numpy.ndarray): The line data array.

    Returns:
        ybus (numpy.ndarray): The Y-bus matrix.
    """

    ybus = np.zeros((len(bus_data), len(bus_data)), dtype=complex)
    lines = line_data.to_dict("records") if hasattr(line_data, "to_dict") else line_data
    for line in lines:
        from_bus = int(line["from_bus"]) - 1  # Adjust for zero-based indexing
        to_bus = int(line["to_bus"]) - 1    # Adjust for zero-based indexing
        r = float(line["R1"])
        x = float(line["X1"])
        b = float(line["B1"])

        z = complex(r, x)
        y = 1 / z

        ybus[from_bus, from_bus] += y + complex(0, b / 2)
        ybus[to_bus, to_bus] += y + complex(0, b / 2)
        ybus[from_bus, to_bus] -= y
        ybus[to_bus, from_bus] -= y

    return ybus

