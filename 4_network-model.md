---
nav_order: 4
---
# Network Model & Data Schemas

The default case uses a **100 MVA** and **12.5 kV** base and contains:
* 18 buses
* PQ, PV, and slack bus types
* 17 transmission lines
* 1 transformer
* Generator operating limits and sequence parameters

## Input Files

Input files are comma-separated (`.csv`) and located in the `data/` directory.

| File | Purpose |
| --- | --- |
| `data/buses.csv` | Bus number, active/reactive injection, bus type, and initial voltage |
| `data/lines.csv` | Positive- and zero-sequence line resistance, reactance, and shunt susceptance |
| `data/transformers.csv` | Transformer impedance and grounding connection |
| `data/generators.csv` | Generator output limits and reactance parameters |

`system_data.py` handles loading these files directly into pandas DataFrames.

