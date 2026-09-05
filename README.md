<link rel="stylesheet" href="./assets/css/mermaid.css">

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
  ┗━ 📦 loadflow_analysis
    ┣━━ 📂 data ## data input files (CSV)
    ┃   ┣━━ 📊 buses.csv ## bus data
    ┃   ┣━━ ⚡ generators.csv ## Generator data
    ┃   ┣━━ 🔗 lines.csv ## line data
    ┃   ┗━━ 🔌 transformers.csv ## transformer data
    ┣━━ 💻 src
    ┃   ┗━━ 🐍 python ## code files
    ┃       ┣━━ 🚀 main.py ## main file to run
    ┃       ┣━━ 📋 system_data.py ## load system data
    ┃       ┣━━ 🧮 ybus.py ## Bus admittance matrix
    ┃       ┣━━ 🔄 gauss_seidel.py ## Gauss-Seidel method of loadflow
    ┃       ┣━━ ⚙️ newton_raphson.py ## Newton-Raphson method of loadflow
    ┃       ┣━━ 📐 jacobian.py ## Jacobian for NR method
    ┃       ┣━━ ∑ power_calc.py ## del P and del Q
    ┃       ┗━━ 📈 line_flows_and_losses.py ## line flows and losses
    ┣━━ ⚖️ LICENSE ## MIT license
    ┗━━ 📘 README.md


```


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
