import csv
import sys
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QFileDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg,
    NavigationToolbar2QT,
)
from matplotlib.figure import Figure

from app.executor import run_simulation
from app.result_reader import read_simulation_result


class OpenModelicaGUI(QMainWindow):
    """Main window for the OpenModelica simulation application."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "OpenModelica Simulation Tool"
        )

        self.setMinimumSize(
            950,
            650
        )

        self.resize(
            1100,
            750
        )

        # ----------------------------------------------------
        # Application state
        # ----------------------------------------------------

        self.simulation_data = None
        self.selected_application = None

        # Store dynamically created variable checkboxes
        self.variable_checks = {}

        # ----------------------------------------------------
        # Build interface
        # ----------------------------------------------------

        self.create_ui()

    # ========================================================
    # USER INTERFACE
    # ========================================================

    def create_ui(self):
        """Create the complete graphical user interface."""

        central_widget = QWidget()

        self.setCentralWidget(
            central_widget
        )

        main_layout = QVBoxLayout(
            central_widget
        )

        main_layout.setContentsMargins(
            25,
            20,
            25,
            20
        )

        main_layout.setSpacing(
            15
        )

        # ====================================================
        # HEADER
        # ====================================================

        title = QLabel(
            "OpenModelica Simulation Tool"
        )

        title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        title.setStyleSheet(
            "font-size: 26px; font-weight: bold;"
        )

        subtitle = QLabel(
            "Run and analyze OpenModelica simulations"
        )

        subtitle.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        subtitle.setStyleSheet(
            "font-size: 13px;"
        )

        main_layout.addWidget(
            title
        )

        main_layout.addWidget(
            subtitle
        )

        # ====================================================
        # SIMULATION CONTROLS
        # ====================================================

        controls_group = QGroupBox(
            "Simulation Controls"
        )

        controls_layout = QGridLayout()

        # ----------------------------------------------------
        # Application
        # ----------------------------------------------------

        application_label = QLabel(
            "Application:"
        )

        self.application_entry = QLineEdit()

        self.application_entry.setPlaceholderText(
            "Select an executable..."
        )

        browse_button = QPushButton(
            "Browse"
        )

        browse_button.clicked.connect(
            self.select_application
        )

        controls_layout.addWidget(
            application_label,
            0,
            0
        )

        controls_layout.addWidget(
            self.application_entry,
            0,
            1
        )

        controls_layout.addWidget(
            browse_button,
            0,
            2
        )

        # ----------------------------------------------------
        # Start Time
        # ----------------------------------------------------

        start_label = QLabel(
            "Start Time:"
        )

        self.start_entry = QLineEdit(
            "0"
        )

        self.start_entry.setPlaceholderText(
            "Integer: 0-3"
        )

        controls_layout.addWidget(
            start_label,
            1,
            0
        )

        controls_layout.addWidget(
            self.start_entry,
            1,
            1
        )

        # ----------------------------------------------------
        # Stop Time
        # ----------------------------------------------------

        stop_label = QLabel(
            "Stop Time:"
        )

        self.stop_entry = QLineEdit(
            "4"
        )

        self.stop_entry.setPlaceholderText(
            "Integer: 1-4"
        )

        controls_layout.addWidget(
            stop_label,
            2,
            0
        )

        controls_layout.addWidget(
            self.stop_entry,
            2,
            1
        )

        # ----------------------------------------------------
        # Run Simulation
        # ----------------------------------------------------

        self.run_button = QPushButton(
            "▶  Run Simulation"
        )

        self.run_button.clicked.connect(
            self.run_and_plot
        )

        controls_layout.addWidget(
            self.run_button,
            3,
            1
        )

        # ----------------------------------------------------
        # Export CSV
        # ----------------------------------------------------

        self.export_button = QPushButton(
            "Export CSV"
        )

        self.export_button.clicked.connect(
            self.export_csv
        )

        # CSV is disabled until a simulation succeeds
        self.export_button.setEnabled(
            False
        )

        controls_layout.addWidget(
            self.export_button,
            3,
            2
        )

        controls_group.setLayout(
            controls_layout
        )

        main_layout.addWidget(
            controls_group
        )

        # ====================================================
        # VARIABLES
        # ====================================================

        variables_group = QGroupBox(
            "Variables"
        )

        self.variables_layout = QHBoxLayout()

        self.variables_placeholder = QLabel(
            "Run a simulation to load available variables."
        )

        self.variables_layout.addWidget(
            self.variables_placeholder
        )

        self.variables_layout.addStretch()

        variables_group.setLayout(
            self.variables_layout
        )

        main_layout.addWidget(
            variables_group
        )

        # ====================================================
        # STATUS
        # ====================================================

        status_layout = QHBoxLayout()

        status_title = QLabel(
            "Status:"
        )

        status_title.setStyleSheet(
            "font-weight: bold;"
        )

        self.status_label = QLabel(
            "Ready"
        )

        status_layout.addWidget(
            status_title
        )

        status_layout.addWidget(
            self.status_label
        )

        status_layout.addStretch()

        main_layout.addLayout(
            status_layout
        )

        # ====================================================
        # GRAPH
        # ====================================================

        graph_group = QGroupBox(
            "Simulation Results"
        )

        graph_layout = QVBoxLayout()

        # Matplotlib figure
        self.figure = Figure(
            figsize=(9, 5),
            dpi=100
        )

        # Matplotlib canvas
        self.canvas = FigureCanvasQTAgg(
            self.figure
        )

        # Matplotlib toolbar
        self.toolbar = NavigationToolbar2QT(
            self.canvas,
            self
        )

        graph_layout.addWidget(
            self.toolbar
        )

        graph_layout.addWidget(
            self.canvas
        )

        graph_group.setLayout(
            graph_layout
        )

        main_layout.addWidget(
            graph_group,
            stretch=1
        )

        # Display initial message
        self.update_graph()

    # ========================================================
    # APPLICATION SELECTION
    # ========================================================

    def select_application(self):
        """Allow the user to select an executable."""

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Application",
            "",
            "Executable Files (*.exe);;All Files (*)"
        )

        if file_path:

            self.selected_application = Path(
                file_path
            )

            self.application_entry.setText(
                file_path
            )

    # ========================================================
    # VALIDATION
    # ========================================================

    def validate_inputs(self):
        """
        Validate application and simulation time inputs.

        FOSSEE requirement:

            0 <= start time < stop time < 5

        Start and stop times must be integers.
        """

        # ----------------------------------------------------
        # Validate application
        # ----------------------------------------------------

        application = (
            self.application_entry
            .text()
            .strip()
        )

        if not application:

            raise ValueError(
                "Please select an application to execute."
            )

        application_path = Path(
            application
        )

        if not application_path.exists():

            raise FileNotFoundError(
                "Selected application does not exist."
            )

        if application_path.suffix.lower() != ".exe":

            raise ValueError(
                "Please select a valid executable (.exe) file."
            )

        # ----------------------------------------------------
        # Validate times
        # ----------------------------------------------------

        try:

            start_time = int(
                self.start_entry
                .text()
                .strip()
            )

            stop_time = int(
                self.stop_entry
                .text()
                .strip()
            )

        except ValueError:

            raise ValueError(
                "Start time and stop time must be integers."
            )

        # ----------------------------------------------------
        # FOSSEE test condition
        # ----------------------------------------------------

        if start_time < 0:

            raise ValueError(
                "Start time must be greater than or equal to 0."
            )

        if stop_time >= 5:

            raise ValueError(
                "Stop time must be less than 5."
            )

        if start_time >= stop_time:

            raise ValueError(
                "Start time must be less than stop time."
            )

        return (
            application_path,
            start_time,
            stop_time
        )

    # ========================================================
    # RUN SIMULATION
    # ========================================================

    def run_and_plot(self):
        """Run the selected OpenModelica executable."""

        try:

            (
                application,
                start_time,
                stop_time
            ) = self.validate_inputs()

            # ------------------------------------------------
            # Update status
            # ------------------------------------------------

            self.status_label.setText(
                "Running simulation..."
            )

            self.run_button.setEnabled(
                False
            )

            QApplication.processEvents()

            # ------------------------------------------------
            # Run OpenModelica executable
            # ------------------------------------------------

            result = run_simulation(
                executable_path=application,
                start_time=start_time,
                stop_time=stop_time
            )

            # ------------------------------------------------
            # Check simulation result
            # ------------------------------------------------

            if result.returncode != 0:

                error_message = (
                    result.stderr
                    if result.stderr
                    else result.stdout
                )

                if not error_message:

                    error_message = (
                        "Simulation process failed."
                    )

                raise RuntimeError(
                    error_message
                )

            # ------------------------------------------------
            # Locate result file
            # ------------------------------------------------

            result_file = application.with_name(
                application.stem + "_res.mat"
            )

            if not result_file.exists():

                raise FileNotFoundError(
                    "Simulation completed, but "
                    "the result file was not found:\n\n"
                    f"{result_file}"
                )

            # ------------------------------------------------
            # Read simulation results
            # ------------------------------------------------

            self.status_label.setText(
                "Reading simulation results..."
            )

            QApplication.processEvents()

            self.simulation_data = (
                read_simulation_result(
                    result_file
                )
            )

            # ------------------------------------------------
            # Create variable checkboxes
            # ------------------------------------------------

            self.update_variable_selection()

            # ------------------------------------------------
            # Update graph
            # ------------------------------------------------

            self.update_graph()

            # ------------------------------------------------
            # Enable CSV export
            # ------------------------------------------------

            self.export_button.setEnabled(
                True
            )

            self.status_label.setText(
                "Simulation completed successfully."
            )

        except Exception as error:

            self.status_label.setText(
                "Simulation failed."
            )

            QMessageBox.critical(
                self,
                "Simulation Error",
                str(error)
            )

        finally:

            self.run_button.setEnabled(
                True
            )

    # ========================================================
    # EXPORT CSV
    # ========================================================

    def export_csv(self):
        """Export selected simulation variables to CSV."""

        if self.simulation_data is None:

            QMessageBox.warning(
                self,
                "No Results",
                "Run a simulation before exporting results."
            )

            return

        # ----------------------------------------------------
        # Find selected variables
        # ----------------------------------------------------

        selected_variables = [
            name
            for name, checkbox
            in self.variable_checks.items()
            if checkbox.isChecked()
        ]

        if not selected_variables:

            QMessageBox.warning(
                self,
                "No Variables Selected",
                "Please select at least one variable to export."
            )

            return

        # ----------------------------------------------------
        # Select CSV save location
        # ----------------------------------------------------

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Simulation Results",
            "simulation_results.csv",
            "CSV Files (*.csv)"
        )

        if not file_path:

            return

        # ----------------------------------------------------
        # Get simulation data
        # ----------------------------------------------------

        time = self.simulation_data[
            "time"
        ]

        variables = self.simulation_data[
            "variables"
        ]

        # ----------------------------------------------------
        # Write CSV
        # ----------------------------------------------------

        try:

            with open(
                file_path,
                "w",
                newline="",
                encoding="utf-8"
            ) as csv_file:

                writer = csv.writer(
                    csv_file
                )

                # Header
                writer.writerow(
                    ["time"] + selected_variables
                )

                # Data
                for index in range(
                    len(time)
                ):

                    row = [
                        time[index]
                    ]

                    for name in selected_variables:

                        row.append(
                            variables[name][index]
                        )

                    writer.writerow(
                        row
                    )

            self.status_label.setText(
                "CSV exported successfully."
            )

            QMessageBox.information(
                self,
                "Export Successful",
                "Simulation results exported successfully:\n\n"
                f"{file_path}"
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Export Error",
                f"Could not export CSV:\n\n"
                f"{error}"
            )

    # ========================================================
    # VARIABLE SELECTION
    # ========================================================

    def update_variable_selection(self):
        """Create checkboxes from simulation variables."""

        # ----------------------------------------------------
        # Remove existing widgets
        # ----------------------------------------------------

        while self.variables_layout.count():

            item = (
                self.variables_layout
                .takeAt(0)
            )

            widget = item.widget()

            if widget is not None:

                widget.deleteLater()

        # ----------------------------------------------------
        # Clear previous references
        # ----------------------------------------------------

        self.variable_checks.clear()

        # ----------------------------------------------------
        # Safety check
        # ----------------------------------------------------

        if self.simulation_data is None:

            self.variables_placeholder = QLabel(
                "Run a simulation to load available variables."
            )

            self.variables_layout.addWidget(
                self.variables_placeholder
            )

            self.variables_layout.addStretch()

            return

        # ----------------------------------------------------
        # Get available variables
        # ----------------------------------------------------

        variables = self.simulation_data[
            "variables"
        ]

        # ----------------------------------------------------
        # Create checkboxes
        # ----------------------------------------------------

        for name in variables:

            checkbox = QCheckBox(
                name
            )

            # Select tank heights by default
            if name in (
                "tank1.h",
                "tank2.h"
            ):

                checkbox.setChecked(
                    True
                )

            checkbox.stateChanged.connect(
                self.update_graph
            )

            self.variable_checks[
                name
            ] = checkbox

            self.variables_layout.addWidget(
                checkbox
            )

        self.variables_layout.addStretch()

    # ========================================================
    # GRAPH
    # ========================================================

    def update_graph(self, *args):
        """Update the graph based on selected variables."""

        # ----------------------------------------------------
        # Clear previous graph
        # ----------------------------------------------------

        self.figure.clear()

        axis = self.figure.add_subplot(
            111
        )

        # ----------------------------------------------------
        # No simulation yet
        # ----------------------------------------------------

        if self.simulation_data is None:

            axis.text(
                0.5,
                0.5,
                "Run a simulation to display results.",
                ha="center",
                va="center",
                transform=axis.transAxes
            )

            axis.set_axis_off()

            self.canvas.draw()

            return

        # ----------------------------------------------------
        # Get simulation data
        # ----------------------------------------------------

        time = self.simulation_data[
            "time"
        ]

        variables = self.simulation_data[
            "variables"
        ]

        plotted = False

        # ----------------------------------------------------
        # Plot selected variables
        # ----------------------------------------------------

        for name, checkbox in (
            self.variable_checks.items()
        ):

            if checkbox.isChecked():

                if name not in variables:

                    continue

                axis.plot(
                    time,
                    variables[name],
                    label=name
                )

                plotted = True

        # ----------------------------------------------------
        # Nothing selected
        # ----------------------------------------------------

        if not plotted:

            axis.text(
                0.5,
                0.5,
                "Select at least one variable.",
                ha="center",
                va="center",
                transform=axis.transAxes,
                fontsize=12
            )

            axis.set_axis_off()

        # ----------------------------------------------------
        # Graph formatting
        # ----------------------------------------------------

        else:

            axis.set_title(
                "OpenModelica Simulation Results"
            )

            axis.set_xlabel(
                "Time (s)"
            )

            axis.set_ylabel(
                "Value"
            )

            axis.grid(
                True,
                alpha=0.3
            )

            axis.legend()

        self.figure.tight_layout()

        self.canvas.draw()


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

def create_gui():
    """Create and start the PyQt6 application."""

    app = QApplication(
        sys.argv
    )

    window = OpenModelicaGUI()

    window.show()

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":

    create_gui()