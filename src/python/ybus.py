import numpy as np
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
    for line in line_data:
        from_bus = int(line[0]) - 1  # Adjust for zero-based indexing
        to_bus = int(line[1]) - 1    # Adjust for zero-based indexing
        r = line[2]
        x = line[3]
        b = line[4]

        z = complex(r, x)
        y = 1 / z

        ybus[from_bus, from_bus] += y + complex(0, b / 2)
        ybus[to_bus, to_bus] += y + complex(0, b / 2)
        ybus[from_bus, to_bus] -= y
        ybus[to_bus, from_bus] -= y

    return ybus

