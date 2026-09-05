---
nav_order: 3
---
# Numerical Methods & Outputs

## Method Overview

* **Y-bus (`ybus.py`):** Converts each line impedance into a series admittance, adds line charging susceptance, and stamps the resulting terms into the complex bus admittance matrix. Transformer impedance is stamped using the same positive-sequence representation.
* **Gauss-Seidel (`gauss_seidel.py`):** Iteratively updates PQ-bus voltages and PV-bus voltage angles. PV generator reactive power is limited using the generator data in `data/generators.csv`.
* **Newton-Raphson (`newton_raphson.py`):** Solves active-power and reactive-power mismatch equations using the Jacobian assembled by `jacobian.py`. Applies damped updates while preserving PV and slack-bus voltage constraints.

## Solver Outputs

### Newton-Raphson Results
Returns a result table with:
* `Bus`: bus number
* `V_mag`: voltage magnitude in per-unit
* `V_ang_deg`: voltage angle in degrees
* `I_real`, `I_imag`: current-injection components
* `P_MW`: active-power injection
* `Q_MVAr`: reactive-power injection

### Gauss-Seidel Results
Returns bus voltage, current, and complex-power results, together with the number of iterations and final convergence error.

### Branch Calculations
Reports the following for each connected pair of buses:
* Sending-end and receiving-end active power in MW
* Sending-end and receiving-end reactive power in MVAr
* Active and reactive losses

