
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

class SystemData:
    def __init__(self, base_mva=100, base_kv=12.5):
        self.base_mva = base_mva
        self.base_kv = base_kv
        self.bus_data = []      # loadflow buses
        self.line_data = []     # loadflow + fault sequence
        self.gen_data = []      # generator for fault + loadflow
        self.transformer_data = []

    def load_ieee_18_bus(self):
        # --- BUS DATA (Loadflow) ---
        raw_buses = [
            (1,  0.0, 0.0, "PV"),
            (2,  0.2, 0.12, "PQ"),
            (3,  0.4, 0.25, "PQ"),
            (4,  1.5, 0.93, "PQ"),
            (5,  0.0, 0.0, "PV"),  # NL bus
            (6,  0.8, 0.5, "PQ"),
            (7,  0.2, 0.12, "PQ"),
            (8,  1.0, 0.62, "PQ"),
            (9,  0.5, 0.31, "PQ"), # NL bus
            (10, 1.0, 0.62, "PQ"),
            (11, 0.3, 0.19, "PQ"),
            (12, 0.2, 0.12, "PQ"),
            (13, 0.8, 0.5, "PQ"),  # NL bus
            (14, 0.5, 0.31, "PQ"),
            (15, 1.0, 0.62, "PQ"),
            (16, 0.2, 0.12, "PQ"),
            (17, 0.0, 0.0, "PV"), # transformer bus
            (18, 0.0, 0.0, "SLACK"),       # main substation
        ]
        self.bus_data = [
            {"bus": b, "Pd_MW": pd, "Qd_MVAr": qd, "type": t, "V_pu": 1.0 if "SLACK" in t else None}
            for b,pd,qd,t in raw_buses
        ]

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
        raw_lines_pos = [
            (1,  2,  0.00431, 0.01204, 0.000035),
            (2,  3,  0.00601, 0.01677, 0.000049),
            (3,  4,  0.00316, 0.00882, 0.000026),
            (4,  5,  0.00896, 0.02502, 0.000073),
            (5,  6,  0.00295, 0.00824, 0.000024),
            (6,  7,  0.01720, 0.02120, 0.000046),
            (7,  8,  0.04070, 0.03053, 0.000051),
            (2,  9,  0.01706, 0.02209, 0.000043),
            (1,  10, 0.02910, 0.03768, 0.000074),
            (10, 11, 0.02222, 0.02877, 0.000056),
            (11, 12, 0.04803, 0.06218, 0.000122),
            (11, 13, 0.03985, 0.05160, 0.000101),
            (13, 14, 0.02910, 0.03768, 0.000074),
            (13, 15, 0.03727, 0.04593, 0.000100),
            (15, 16, 0.02208, 0.02720, 0.000059),
            (25, 26, 0.02208, 0.02720, 0.000059)
            ]
        for f,t,r1,x1,b1 in raw_lines_pos:
            # Estimate zero seq for fault analysis
            r0 = r1 * 2.5
            x0 = x1 * 2.5
            b0 = b1 * 0.5  # zero seq shunt is smaller
            self.line_data.append({
                "from_bus": f, "to_bus": t,
                "R1_pu": r1, "X1_pu": x1, "B1_pu": b1,
                "R0_pu": r0, "X0_pu": x0, "B0_pu": b0,
                "length_km": None  # not given in source
            })

        # --- TRANSFORMER (17-18) ---
        self.transformer_data = [{
            "from_bus": 17, "to_bus": 18,
            "X_pu": 0.06753, "R_pu": 0.00312,
            "X0_pu": 0.06753, # assume same, grounded-wye
            "connection": "Dyn11",
            "grounded": True
        }]

        self.BUS_MAPPING = {orig:i+1 for i, orig in enumerate([b["bus"] for b in self.bus_data])}
        return self

    # Helpers for fault analysis
    def get_ybus_positive(self):
        """Return positive sequence YBUS data for fault - use R1/X1"""
        return [(l["from_bus"], l["to_bus"], l["R1_pu"], l["X1_pu"]) for l in self.line_data]

    def get_ybus_zero(self):
        """Return zero sequence YBUS data for LG/LLG faults"""
        return [(l["from_bus"], l["to_bus"], l["R0_pu"], l["X0_pu"]) for l in self.line_data]

if __name__ == "__main__":
    sd = SystemData().load_ieee_18_bus()
    print(f"Buses: {len(sd.bus_data)}, Lines: {len(sd.line_data)}, Gens: {len(sd.gen_data)}")
    print("Gen:", sd.gen_data[0])
    print("Sample line with seq:", sd.line_data[0])
