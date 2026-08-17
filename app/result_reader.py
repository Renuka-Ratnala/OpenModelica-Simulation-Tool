from pathlib import Path
import DyMat


def read_simulation_result(result_file):
    result_file = Path(result_file)

    if not result_file.exists():
        raise FileNotFoundError(
            f"Result file not found: {result_file}"
        )

    result = DyMat.DyMatFile(str(result_file))

    # Get all available variables
    variable_names = result.names()

    print("Available variables:")
    for name in variable_names:
        print(" -", name)

    # OpenModelica stores time as the abscissa
    # rather than as a normal variable.
    if not variable_names:
        raise ValueError(
            "No variables were found in the simulation result."
        )

    # Use the first variable to obtain the time axis.
    first_variable = next(iter(variable_names))

    time = result.abscissa(
    first_variable,
    valuesOnly=True
    )

    # Read every variable
    data = {}

    for name in variable_names:
        try:
            data[name] = result.data(name)
        except Exception as error:
            print(
                f"Warning: Could not read '{name}': {error}"
            )

    return {
        "time": time,
        "variables": data
    }