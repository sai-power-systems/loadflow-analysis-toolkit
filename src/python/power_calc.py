from system_data import *
import numpy as np
from ybus import compute_ybus


def calculate_power(bus_data, Ybus):
    V = (
        bus_data["V_mag"].to_numpy(dtype=float)
        * np.exp(1j * np.radians(bus_data["V_ang"].to_numpy(dtype=float)))
    )
    I = Ybus @ V
    return V * np.conj(I)


Ybus = compute_ybus(bus_data, line_data)


V = bus_data["V_mag"].values
D = bus_data["V_ang"].values
P = bus_data["P_MW"].values
Q = bus_data["Q_MVAR"].values
I = Ybus @ (V * np.exp(1j * np.radians(D)))
S = complex(P, Q) # Complex power S = P + jQ

# Complex voltage phasors

results = pd.DataFrame({
    "Bus": bus_data["bus_no"].to_numpy(),
    "V": V,
    "I": I,
    "S": S,
    "P_MW": S.real,
    "Q_MVAr": S.imag,
}, columns=["Bus", "V", "I", "S", "P_MW", "Q_MVAr"])

print(results.to_string(index=False))

# ---- Initial guess for voltage magnitudes and angles (in radians) ----
for s in slack_buses:
    bus_data.loc[s, "V_mag"] = 1.25
    bus_data.loc[s, "V_ang"] = 0.0

for p in pq_buses:
    bus_data.loc[p, "V_mag"] = 1.0
    bus_data.loc[p, "V_ang"] = 0.0

    P_sp = bus_data.loc[p, ["P_MW"]].values
    Q_sp = bus_data.loc[p, ["Q_MVAR"]].values


print("+++++++++++++++++++++")
print(calculate_power(bus_data, Ybus))