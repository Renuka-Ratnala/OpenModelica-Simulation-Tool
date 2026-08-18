# OpenModelica Simulation Tool

A desktop application built with **Python, PyQt6, OpenModelica, DyMat, and Matplotlib** for running OpenModelica simulation executables and interactively analyzing their simulation results.

## Features

- Select an OpenModelica-generated `.exe` using a file browser
- Configure simulation start and stop times
- Validate simulation inputs
- Execute OpenModelica simulations directly from the GUI
- Automatically locate the generated `.mat` result file
- Read OpenModelica result files using DyMat
- Dynamically detect available simulation variables
- Select multiple variables for visualization
- Interactive Matplotlib graph
- Zoom, pan, reset, and save graph functionality
- Simulation status and error reporting

## Technologies Used

- **Python 3.11**
- **PyQt6** - Desktop GUI
- **OpenModelica** - Simulation engine
- **DyMat** - OpenModelica result-file reader
- **Matplotlib** - Simulation data visualization
- **NumPy / SciPy** - Numerical and scientific computing
- **Git / GitHub** - Version control

## Project Structure

```text
OpenModelica-Simulation-Tool/
│
├── app/
│   ├── executor.py
│   ├── gui.py
│   ├── main.py
│   └── result_reader.py
│
├── model/
│   └── TwoTanksConnected/
│       └── OpenModelica model files
│
├── requirements.txt
├── .gitignore
└── README.md
