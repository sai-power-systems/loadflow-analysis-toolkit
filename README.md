# Load Flow Analysis Toolkit

Python toolkit for steady-state power-system load-flow analysis on an IEEE
18-bus distribution test system. The project builds a positive-sequence
network admittance matrix (Y-bus), solves bus voltages with Gauss-Seidel and
Newton-Raphson methods, and calculates branch power flows and losses.

## Implemented stages

- Network data loading from CSV files
- Positive-sequence Y-bus construction
- Bus classification into PQ, PV, and slack buses
- Gauss-Seidel load-flow iteration
- Damped Newton-Raphson load-flow iteration
- Active and reactive bus-power calculation
- Branch power-flow and line-loss calculation
- Transformer inclusion in the Y-bus
- Storage of zero-sequence and generator parameters for future fault-analysis
  work

## Repository layout

```mermaid
treeView-beta
loadflow-analysis/
  data/
    buses.csv
    generators.csv
    lines.csv
    transformers.csv
  src/
    python/
      main.py
      system_data.py
      ybus.py
      gauss_seidel.py
      newton_raphson.py
      jacobian.py
      power_calc.py
      line_flows_and_losses.py
  LICENSE
  README.md

```

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

## Method overview

### Y-bus

`ybus.py` converts each line impedance into a series admittance, adds line
charging susceptance, and stamps the resulting terms into the complex bus
admittance matrix. Transformer impedance is stamped using the same positive-
sequence representation.

### Gauss-Seidel

`gauss_seidel.py` iteratively updates PQ-bus voltages and PV-bus voltage angles.
PV generator reactive power is limited using the generator data in
`data/generators.csv`.

### Newton-Raphson

`newton_raphson.py` solves the active-power and reactive-power mismatch
equations using the Jacobian assembled by `jacobian.py`. It applies damped
updates and preserves PV and slack-bus voltage constraints.

## Current development notes

The repository is an active prototype. Before relying on the top-level driver
for production studies, the following integration issues should be resolved:

- `gauss_seidel.py` shadows the imported `gen_data` name before using it.
- `line_flows_and_losses.py` expects a Gauss-Seidel result column named `V`,
  while the current Gauss-Seidel result table does not expose that column.
- There are no automated tests or pinned dependency versions yet.

These limitations do not change the intended solver design described above,
but they can prevent `src/python/main.py` from completing successfully in its
current state.

## Contributing

1. Create a feature branch.
2. Keep input schemas and units documented when changing the CSV files.
3. Add regression tests for solver or network-model changes.
4. Run the relevant solver scripts from the repository root.
5. Open a pull request with a concise description of the numerical or
   electrical-system impact.

## License

This project is distributed under the [MIT License](LICENSE).
