import subprocess
import os
from pathlib import Path


OPENMODELICA_BIN = Path(
    r"C:\Program Files\OpenModelica1.27.0-64bit\bin"
)


def run_simulation(
    executable_path,
    start_time=0,
    stop_time=4
):

    executable = Path(executable_path)

    # Check executable
    if not executable.exists():
        raise FileNotFoundError(
            f"Simulation executable not found:\n{executable}"
        )

    # Check OpenModelica
    if not OPENMODELICA_BIN.exists():
        raise FileNotFoundError(
            f"OpenModelica bin folder not found:\n{OPENMODELICA_BIN}"
        )

    # Copy current environment
    env = os.environ.copy()

    # Add OpenModelica DLL folder to PATH
    env["PATH"] = (
        str(OPENMODELICA_BIN)
        + os.pathsep
        + env.get("PATH", "")
    )

    # OpenModelica executable command
    command = [
        str(executable),
        f"-startTime={start_time}",
        f"-stopTime={stop_time}",
    ]

    print("Running command:")
    print(" ".join(command))

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        cwd=str(executable.parent),
        env=env
    )

    return result