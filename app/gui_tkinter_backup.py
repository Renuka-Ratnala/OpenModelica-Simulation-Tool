import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

from app.executor import run_simulation
from app.result_reader import read_simulation_result

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ============================================================
# CONFIGURATION
# ============================================================

RESULT_FILE = (
    Path(r"C:\OpenModelica-Desktop-App")
    / "model"
    / "TwoTanksConnected"
    / "TwoConnectedTanks_res.mat"
)


# ============================================================
# MAIN GUI
# ============================================================

class OpenModelicaGUI:

    def __init__(self, root):

        self.root = root

        self.root.title("OpenModelica Simulation Tool")
        self.root.geometry("1150x780")
        self.root.minsize(950, 650)

        self.canvas = None

        # Store simulation data
        self.simulation_data = None

        # Variable selection
        self.tank1_selected = tk.BooleanVar(value=True)
        self.tank2_selected = tk.BooleanVar(value=True)

        self.create_styles()
        self.create_widgets()

    # ========================================================
    # STYLES
    # ========================================================

    def create_styles(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Title.TLabel",
            font=("Arial", 24, "bold")
        )

        style.configure(
            "Subtitle.TLabel",
            font=("Arial", 11)
        )

        style.configure(
            "Section.TLabelframe.Label",
            font=("Arial", 11, "bold")
        )

        style.configure(
            "Run.TButton",
            font=("Arial", 11, "bold"),
            padding=(20, 10)
        )

        style.configure(
            "Status.TLabel",
            font=("Arial", 10)
        )

    # ========================================================
    # CREATE WIDGETS
    # ========================================================

    def create_widgets(self):

        # Main frame
        main_frame = ttk.Frame(
            self.root,
            padding=20
        )

        main_frame.pack(
            fill=tk.BOTH,
            expand=True
        )

        # ====================================================
        # HEADER
        # ====================================================

        title = ttk.Label(
            main_frame,
            text="OpenModelica Simulation Tool",
            style="Title.TLabel"
        )

        title.pack(pady=(5, 2))

        subtitle = ttk.Label(
            main_frame,
            text="Run and analyze OpenModelica simulations",
            style="Subtitle.TLabel"
        )

        subtitle.pack(pady=(0, 18))

        # ====================================================
        # CONTROLS
        # ====================================================

        control_frame = ttk.LabelFrame(
            main_frame,
            text="Simulation Controls",
            padding=15,
            style="Section.TLabelframe"
        )

        control_frame.pack(
            fill=tk.X,
            pady=(0, 12)
        )

        # Start time
        ttk.Label(
            control_frame,
            text="Start Time:"
        ).grid(
            row=0,
            column=0,
            padx=(0, 6),
            pady=5
        )

        self.start_entry = ttk.Entry(
            control_frame,
            width=10
        )

        self.start_entry.insert(
            0,
            "0"
        )

        self.start_entry.grid(
            row=0,
            column=1,
            padx=(0, 20)
        )

        # Stop time
        ttk.Label(
            control_frame,
            text="Stop Time:"
        ).grid(
            row=0,
            column=2,
            padx=(0, 6)
        )

        self.stop_entry = ttk.Entry(
            control_frame,
            width=10
        )

        self.stop_entry.insert(
            0,
            "4"
        )

        self.stop_entry.grid(
            row=0,
            column=3,
            padx=(0, 25)
        )

        # Run button
        self.run_button = ttk.Button(
            control_frame,
            text="▶  Run Simulation",
            style="Run.TButton",
            command=self.run_and_plot
        )

        self.run_button.grid(
            row=0,
            column=4,
            padx=10
        )

        # Clear button
        self.clear_button = ttk.Button(
            control_frame,
            text="Clear Results",
            command=self.clear_graph
        )

        self.clear_button.grid(
            row=0,
            column=5,
            padx=10
        )

        # ====================================================
        # VARIABLES
        # ====================================================

        variable_frame = ttk.LabelFrame(
            main_frame,
            text="Variables",
            padding=12,
            style="Section.TLabelframe"
        )

        variable_frame.pack(
            fill=tk.X,
            pady=(0, 12)
        )

        self.tank1_check = ttk.Checkbutton(
            variable_frame,
            text="Tank 1 Height (tank1.h)",
            variable=self.tank1_selected,
            command=self.update_graph
        )

        self.tank1_check.pack(
            side=tk.LEFT,
            padx=(5, 25)
        )

        self.tank2_check = ttk.Checkbutton(
            variable_frame,
            text="Tank 2 Height (tank2.h)",
            variable=self.tank2_selected,
            command=self.update_graph
        )

        self.tank2_check.pack(
            side=tk.LEFT
        )

        # ====================================================
        # STATUS
        # ====================================================

        status_frame = ttk.Frame(
            main_frame
        )

        status_frame.pack(
            fill=tk.X,
            pady=(0, 8)
        )

        ttk.Label(
            status_frame,
            text="Status:",
            font=("Arial", 10, "bold")
        ).pack(
            side=tk.LEFT
        )

        self.status_label = ttk.Label(
            status_frame,
            text="Ready",
            style="Status.TLabel"
        )

        self.status_label.pack(
            side=tk.LEFT,
            padx=6
        )

        # ====================================================
        # GRAPH
        # ====================================================

        self.graph_frame = ttk.LabelFrame(
            main_frame,
            text="Simulation Results",
            padding=10,
            style="Section.TLabelframe"
        )

        self.graph_frame.pack(
            fill=tk.BOTH,
            expand=True
        )

        self.placeholder = ttk.Label(
            self.graph_frame,
            text="Run a simulation to display the results.",
            font=("Arial", 12)
        )

        self.placeholder.pack(
            expand=True
        )

    # ========================================================
    # RUN SIMULATION
    # ========================================================

    def run_and_plot(self):

        try:
            start_time = float(
                self.start_entry.get()
            )

            stop_time = float(
                self.stop_entry.get()
            )

            if stop_time <= start_time:
                messagebox.showwarning(
                    "Invalid Time",
                    "Stop time must be greater than start time."
                )
                return

        except ValueError:

            messagebox.showwarning(
                "Invalid Time",
                "Please enter valid numeric values for start and stop time."
            )

            return

        self.status_label.config(
            text="Running simulation..."
        )

        self.run_button.config(
            state=tk.DISABLED
        )

        self.root.update_idletasks()

        try:

            # ------------------------------------------------
            # Run existing OpenModelica simulation
            # ------------------------------------------------

            result = run_simulation(
                start_time=start_time,
                stop_time=stop_time
            )

            if result.returncode != 0:

                error_message = (
                    result.stderr
                    if result.stderr
                    else "OpenModelica simulation failed."
                )

                raise RuntimeError(error_message)

            # ------------------------------------------------
            # Check result file
            # ------------------------------------------------

            if not RESULT_FILE.exists():

                raise FileNotFoundError(
                    f"Result file not found:\n{RESULT_FILE}"
                )

            # ------------------------------------------------
            # Read result
            # ------------------------------------------------

            self.status_label.config(
                text="Reading simulation results..."
            )

            self.root.update_idletasks()

            self.simulation_data = read_simulation_result(
                RESULT_FILE
            )

            # ------------------------------------------------
            # Display graph
            # ------------------------------------------------

            self.update_graph()

            self.status_label.config(
                text="Simulation completed successfully."
            )

        except Exception as e:

            self.status_label.config(
                text="Simulation failed."
            )

            messagebox.showerror(
                "Simulation Error",
                str(e)
            )

            print("Simulation Error:")
            print(e)

        finally:

            self.run_button.config(
                state=tk.NORMAL
            )

    # ========================================================
    # UPDATE GRAPH
    # ========================================================

    def update_graph(self):

        if self.simulation_data is None:
            return

        time = self.simulation_data["time"]

        tank1_h = self.simulation_data["tank1_h"]

        tank2_h = self.simulation_data["tank2_h"]

        # Remove placeholder
        if self.placeholder.winfo_exists():
            self.placeholder.destroy()

        # Remove previous canvas
        if self.canvas is not None:

            self.canvas.get_tk_widget().destroy()

            self.canvas = None

        # Create figure
        figure = Figure(
            figsize=(9, 5),
            dpi=100
        )

        ax = figure.add_subplot(111)

        plotted = False

        # Tank 1
        if self.tank1_selected.get():

            ax.plot(
                time,
                tank1_h,
                label="Tank 1 Height"
            )

            plotted = True

        # Tank 2
        if self.tank2_selected.get():

            ax.plot(
                time,
                tank2_h,
                label="Tank 2 Height"
            )

            plotted = True

        # If nothing selected
        if not plotted:

            ax.text(
                0.5,
                0.5,
                "Select at least one variable.",
                ha="center",
                va="center",
                transform=ax.transAxes,
                fontsize=12
            )

            ax.set_axis_off()

        else:

            ax.set_title(
                "Two Connected Tanks"
            )

            ax.set_xlabel(
                "Time (s)"
            )

            ax.set_ylabel(
                "Height"
            )

            ax.grid(
                True,
                alpha=0.3
            )

            ax.legend()

        figure.tight_layout()

        # Embed graph
        self.canvas = FigureCanvasTkAgg(
            figure,
            master=self.graph_frame
        )

        self.canvas.draw()

        self.canvas.get_tk_widget().pack(
            fill=tk.BOTH,
            expand=True
        )

    # ========================================================
    # CLEAR GRAPH
    # ========================================================

    def clear_graph(self):

        self.simulation_data = None

        if self.canvas is not None:

            self.canvas.get_tk_widget().destroy()

            self.canvas = None

        self.placeholder = ttk.Label(
            self.graph_frame,
            text="Run a simulation to display the results.",
            font=("Arial", 12)
        )

        self.placeholder.pack(
            expand=True
        )

        self.status_label.config(
            text="Ready"
        )


# ============================================================
# START APPLICATION
# ============================================================

def create_gui():

    root = tk.Tk()

    OpenModelicaGUI(root)

    root.mainloop()


if __name__ == "__main__":
    create_gui()