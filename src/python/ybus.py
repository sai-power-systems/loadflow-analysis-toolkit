import numpy as np
import pandas as pd
def compute_ybus(bus_data, line_data, transformer_data=None):
    ybus = np.zeros((len(bus_data), len(bus_data)), dtype=complex)

    lines = line_data.to_dict("records")

    if transformer_data is not None:
        transformers = transformer_data.to_dict("records")

        for transformer in transformers:
            lines.append({
                "from_bus": transformer["from_bus"],
                "to_bus": transformer["to_bus"],
                "R1": transformer["R_pu"],
                "X1": transformer["X_pu"],
                "B1": 0.0,
            })


    for line in lines:
        from_bus = int(line["from_bus"]) - 1
        to_bus = int(line["to_bus"]) - 1

        resistance = float(line["R1"])
        reactance = float(line["X1"])
        susceptance = float(line.get("B1", 0.0))

        impedance = complex(resistance, reactance)
        series_admittance = 1 / impedance
        shunt_admittance = complex(0, susceptance / 2)

        ybus[from_bus, from_bus] += series_admittance + shunt_admittance
        ybus[to_bus, to_bus] += series_admittance + shunt_admittance
        ybus[from_bus, to_bus] -= series_admittance
        ybus[to_bus, from_bus] -= series_admittance

    return ybus