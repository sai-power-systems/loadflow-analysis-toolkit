---
nav_order: 1
---
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

## Dataset Citation

The IEEE 18-bus test system used in this project is based on the standard IEEE 18-bus radial distribution system originally reported by Grady, Samotyj, and Noyola (1992). The line and load parameters used in this project were obtained from the reproduced IEEE 18-bus test-system data provided in Appendix A of Milovanović, Radosavljević, and Perović (2018).

### References

1. W. M. Grady, M. J. Samotyj, and A. H. Noyola, "The application of network objective functions for actively minimizing the impact of voltage harmonics in power systems," *IEEE Transactions on Power Delivery*, vol. 7, pp. 1379–1386, July 1992.

2. M. Milovanović, J. Radosavljević, B. Perović, and M. Dragičević, "A Decoupled Approach for Harmonic Power Flow in Radial Distribution Systems with Nonlinear Loads," *International Journal of Electrical Engineering and Computing*, vol. 2, no. 1, 2018.

The system data are specified on a 10 MVA, 12.5 kV base.

### Data Source

The IEEE 18-bus line and load parameters are given in **Appendix A, Table A.I** of the following paper:

[Milovanović et al. (2018) – IEEE 18-bus test system data](https://ijeec.etf.ues.rs.ba/index.php/ijeec/article/download/29/14/)
