# Load Flow Analysis Toolkit

Python toolkit for steady-state power-system load-flow analysis on an IEEE
18-bus distribution test system. The project builds a positive-sequence
network admittance matrix (Y-bus), solves bus voltages with Gauss-Seidel and
Newton-Raphson methods, and calculates branch power flows and losses.

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