# Solver...

## Requirements

- Python 3.9 or newer
- NumPy
- pandas

There is currently no `requirements.txt` or package configuration file. Install
the runtime dependencies with:

```powershell
python -m pip install numpy pandas
```

## Network model

The default case uses a 100 MVA and 12.5 kV base and contains:

- 18 buses
- PQ, PV, and slack bus types
- 17 transmission lines
- 1 transformer
- Generator operating limits and sequence parameters

Input files are comma-separated and use the following fields:

| File | Purpose |
| --- | --- |
| `data/buses.csv` | Bus number, active/reactive injection, bus type, and initial voltage |
| `data/lines.csv` | Positive- and zero-sequence line resistance, reactance, and shunt susceptance |
| `data/transformers.csv` | Transformer impedance and grounding connection |
| `data/generators.csv` | Generator output limits and reactance parameters |

`system_data.py` loads these files into pandas DataFrames. Data paths are
currently relative to the repository root, so commands should be run from that
directory.

## Running the project

From the repository root, make the source directory importable and start the
main driver:

```powershell
$env:PYTHONPATH = "$PWD\src\python"
python src\python\main.py
```

The driver is intended to:

1. Run the Gauss-Seidel solver.
2. Run the Newton-Raphson solver.
3. Print bus voltage/current and power results.
4. Print branch flows and losses for both methods.

Individual modules can also be inspected or run as scripts. For example:

```powershell
$env:PYTHONPATH = "$PWD\src\python"
python src\python\newton_raphson.py
python src\python\jacobian.py
```

## Solver outputs

The Newton-Raphson solver returns a result table with:

- `Bus`: bus number
- `V_mag`: voltage magnitude in per-unit
- `V_ang_deg`: voltage angle in degrees
- `I_real`, `I_imag`: current-injection components
- `P_MW`: active-power injection
- `Q_MVAr`: reactive-power injection

The Gauss-Seidel solver returns bus voltage, current, and complex-power
results, together with the number of iterations and final convergence error.

Branch calculations report, for each connected pair of buses:

- Sending-end and receiving-end active power in MW
- Sending-end and receiving-end reactive power in MVAr
- Active and reactive losses