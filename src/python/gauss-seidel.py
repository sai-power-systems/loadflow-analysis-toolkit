import numpy as np
import pandas as pd

from system_data import bus_data, line_data, dd
from ybus import compute_ybus

ybus = compute_ybus(bus_data, line_data)

pq_buses, pv_buses, slack_buses = dd.classify_buses()

# Initial complex voltage vector from buses.csv
V = (
    bus_data["V_mag"].to_numpy(dtype=float)
    * np.exp(1j * np.radians(bus_data["V_ang"].to_numpy(dtype=float)))
)

# Keep slack voltage fixed
for bus_index in slack_buses:
    V[bus_index] = (
        bus_data.loc[bus_index, "V_mag"]
        * np.exp(1j * np.radians(bus_data.loc[bus_index, "V_ang"]))
    )

max_iterations = 100
tolerance = 1e-3

for iteration in range(max_iterations):
    previous_V = V.copy()

    for i in pq_buses:
        power_specified = complex(
            bus_data.loc[i, "P_MW"],
            bus_data.loc[i, "Q_MVAR"],
        )

        off_diagonal_sum = sum(
            ybus[i, j] * V[j]
            for j in range(len(V))
            if j != i
        )

        # Gauss-Seidel update:
        # V_i = (conj(S_i) / conj(V_i) - sum(Y_ij V_j)) / Y_ii
        V[i] = (
            np.conj(power_specified) / np.conj(V[i])
            - off_diagonal_sum
        ) / ybus[i, i]

    error = np.max(np.abs(V - previous_V))

    if error < tolerance:
        print(f"Converged after {iteration + 1} iterations")
        break
else:
    print("Warning: solution did not converge")

# Calculate current and complex power
I = ybus @ V
S = V * np.conj(I)

results = pd.DataFrame({
    "Bus": bus_data["bus_no"].to_numpy(),
    "V": V,
    "I": I,
    "S": S,
    "P_MW": S.real,
    "Q_MVAr": S.imag,
})

print(results.to_string(index=False))