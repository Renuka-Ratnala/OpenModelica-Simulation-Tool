# OpenModelica Simulation Tool

A Python desktop application for running OpenModelica simulations and interactively visualizing their results.

The application provides a PyQt6-based graphical interface that allows users to select an OpenModelica-generated executable, configure simulation start and stop times, execute the simulation, automatically read the generated `.mat` result file, detect available simulation variables, visualize selected variables, and export simulation results to CSV.

---

## Features

- Select an OpenModelica simulation executable using a file browser
- Configure simulation start and stop times
- Validate simulation inputs before execution
- Enforce the required simulation condition:
  `0 <= start time < stop time < 5`
- Run the OpenModelica executable using Python `subprocess`
- Automatically locate the generated `.mat` result file
- Read OpenModelica result files using DyMat
- Dynamically detect available simulation variables
- Select multiple variables for visualization
- Interactive Matplotlib visualization
- Zoom, pan, reset, and save graph functionality
- Export selected simulation variables to CSV
- Display simulation status and errors through the GUI

---

## Technologies

| Technology | Purpose |
|---|---|
| Python 3.11 | Application development |
| PyQt6 | Desktop GUI |
| OpenModelica | Simulation engine |
| DyMat | Reading OpenModelica result files |
| Matplotlib | Data visualization |
| NumPy | Numerical processing |
| SciPy | Scientific computing |
| Git | Version control |

---

## Project Architecture

```text
OpenModelica Model
        │
        ▼
Compiled OpenModelica executable
        │
        ▼
Python subprocess
        │
        ▼
Simulation result (.mat)
        │
        ▼
DyMat result reader
        │
        ▼
Dynamic variable detection
        │
        ▼
PyQt6 variable selection
        │
        ▼
Matplotlib visualization
        │
        ▼
CSV export
