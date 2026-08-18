# OpenModelica Simulation Tool

A Python desktop application for running OpenModelica simulations and interactively visualizing their results.

The application provides a PyQt6-based graphical interface that allows users to select an OpenModelica-generated executable, configure simulation time, run the simulation, automatically detect variables from the generated result file, and visualize selected variables using Matplotlib.

## Features

- Select an OpenModelica simulation executable through a file browser
- Configure simulation start and stop times
- Validate simulation inputs
- Run OpenModelica simulations directly from the desktop application
- Automatically locate the generated `.mat` result file
- Read OpenModelica result files using DyMat
- Dynamically detect available simulation variables
- Select multiple variables for visualization
- Interactive Matplotlib visualization
- Zoom, pan, reset, and save graph functionality
- Simulation status and error handling

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

## Architecture

```text
OpenModelica Model
        │
        ▼
OpenModelica-generated executable
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
