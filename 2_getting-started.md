---
nav_order: 2
---
# Getting Started

## Requirements

* Python 3.9 or newer
* NumPy
* pandas

## Installation

There is currently no `requirements.txt` or package configuration file. Install the runtime dependencies with:

```powershell
python -m pip install numpy pandas

```

## Running the Project

Data paths are currently relative to the repository root, so commands should be run from that directory.

From the repository root, make the source directory importable and start the main driver:

```powershell
$env:PYTHONPATH = "$PWD\src\python"
python src\python\main.py

```

The driver executes the following workflow:

1. Runs the Gauss-Seidel solver.
2. Runs the Newton-Raphson solver.
3. Prints bus voltage/current and power results.
4. Prints branch flows and losses for both methods.

Individual modules can also be inspected or run as standalone scripts:

```powershell
$env:PYTHONPATH = "$PWD\src\python"
python src\python\newton_raphson.py
python src\python\jacobian.py

```
