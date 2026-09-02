
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
                        {"bus_no": b, "P_MW": p, "Q_MVAR": q, "type": t, "V_mag": v, "V_ang": d}
                        for b,p,q,t,v,d in bus_data_raw
                    ])
      


        generator_columns = [
        "bus",
        "type",
        "P_MW",
        "Q_MVAr",
        "Pmax_MW",
        "Qmin_MVAr",
        "Qmax_MVAr",
        "Xd_pu",
        "Xd_prime_pu",
        "Xd_double_prime_pu",
        "X0_pu",
        "Xn_pu",
        "grounded",
    ]
        # --- GEN DATA (Load from CSV for loadflow and fault analysis) ---
        gen_data = pd.read_csv("data/generators.csv")
        self.gen_data = pd.DataFrame(gen_data, columns=generator_columns)
        

        # --- LINE DATA: R1/X1/B1 + R0/X0 (for fault) ---
        # R0 ~ 2.5*R1, X0 ~ 2.5-3*X1 typical for overhead distribution per IEEE Std 141
        raw_lines_pos = pd.read_csv("data/lines.csv").values

        self.line_data = pd.DataFrame([
                        {"from_bus": f, "to_bus": t, "R1": r1, "X1": x1, "B1": b1, "R0": r0, "X0": x0, "B0": b0}
                        for f,t,r1,x1,b1,r0,x0,b0 in raw_lines_pos
                    ])
      



    def classify_buses(self):
        """Classify buses into PQ, PV, and Slack types."""
        bus_types = self.bus_data["type"].values
        pq_buses = np.where(bus_types == "PQ")[0]
        pv_buses = np.where(bus_types == "PV")[0]
        slack_buses = np.where(bus_types == "SLACK")[0]
        return pq_buses, pv_buses, slack_buses

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
dd.classify_buses()
slack_buses = dd.classify_buses()[2]
pv_buses = dd.classify_buses()[1]
pq_buses = dd.classify_buses()[0]
