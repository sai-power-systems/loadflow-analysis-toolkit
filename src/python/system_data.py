
"""
IEEE 18-Bus System Data - Loadflow + Fault Analysis Ready

Source for loadflow:
[1] Kazemi 2022, Curtin Thesis, Tables 3.2-3.3 - Balanced IEEE 18-bus
[2] Grady et al. 1991/1992 - Original IEEE 18-bus distorted system

For fault analysis:
IEEE 18-bus is a distribution test system - original paper does NOT provide
X0, X'' etc. Values below are IEEE-recommended defaults for distribution
fault studies (based on IEEE Std 141 and typical 12.5kV distribution).
You can cite: "Zero-sequence assumed 2.5x positive, generator X''=0.2 pu typical"
"""
import pandas as pd
import numpy as np
class SystemData:
    def __init__(self, base_mva=100, base_kv=12.5):
        self.base_mva = base_mva
        self.base_kv = base_kv
        self.bus_data = []      # loadflow buses
        self.line_data = []     # loadflow + fault sequence
        self.gen_data = []      # generator for fault + loadflow
        self.transformer_data = []

    def load_data(self):


        bus_data_raw = pd.read_csv("data/buses.csv").values

        self.bus_data = pd.DataFrame([
                        {"bus_no": b, "P_MW": v, "Q_MVAR": d, "type": t}
                        for b,v,d,t in bus_data_raw
                    ])
        print(self.bus_data)

        # --- GEN DATA (Needed for fault) ---
        # Only slack has generation in this distribution system
        self.gen_data = [
            {
                "bus": 18,
                "type": "SLACK",
                "P_MW": 17.981,      # committed from Table 3.1
                "Q_MVAr": 5.6225,
                "Pmax_MW": 30,
                "Qmin_MVAr": -5.0,
                "Qmax_MVAr": 10.0,
                # FAULT DATA - typical defaults
                "Xd_pu": 1.2,        # synchronous
                "Xd_prime_pu": 0.3,  # transient
                "Xd_double_prime_pu": 0.20,  # subtransient - used for fault
                "X0_pu": 0.08,
                "Xn_pu": 0.0,        # solidly grounded
                "grounded": True
            }
        ]

        # --- LINE DATA: R1/X1/B1 + R0/X0 (for fault) ---
        # R0 ~ 2.5*R1, X0 ~ 2.5-3*X1 typical for overhead distribution per IEEE Std 141
        raw_lines_pos = pd.read_csv("data/lines.csv").values

        self.line_data = pd.DataFrame([
                        {"from_bus": f, "to_bus": t, "R1": r1, "X1": x1, "B1": b1, "R0": r0, "X0": x0, "B0": b0}
                        for f,t,r1,x1,b1,r0,x0,b0 in raw_lines_pos
                    ])
        print(self.line_data)


    # Helpers for fault analysis
    def get_ybus_positive(self):
        """Return positive sequence YBUS data for fault - use R1/X1"""
        return [(l["from_bus"], l["to_bus"], l["R1_pu"], l["X1_pu"]) for l in self.line_data]

    def get_ybus_zero(self):
        """Return zero sequence YBUS data for LG/LLG faults"""
        return [(l["from_bus"], l["to_bus"], l["R0_pu"], l["X0_pu"]) for l in self.line_data]


dd = SystemData()
dd.load_data()
bus_data = dd.bus_data
line_data = dd.line_data
gen_data = dd.gen_data