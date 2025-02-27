"""A module containing all the GUI elements for `notes_converter`."""

import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.filedialog import askopenfilenames, asksaveasfilename

from notes_converter.utils.constants import ROOT_PATH


class MainWindow(tk.Tk):
    def __init__(self, converter):
        super().__init__()
        self.converter = converter
        self.input_paths = []
        self.input_value = tk.StringVar(self, value="")
        self.output_path = tk.StringVar(self)

        # Screen orientation
        center_x = self.winfo_screenwidth() // 2
        center_y = self.winfo_screenheight() // 2
        window_width = 400
        window_height = 90
        x = center_x - window_width // 2
        y = center_y - window_height // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Window settings:
        self.title("Notes Converter")

        # Widgets' defaults:
        self.xy_padding = {"padx": 5, "pady": 5}

        # Initialize GUI
        self.create_gui()

    def create_gui(self):
        # Root top frame
        top_frame = tk.Frame(self, cnf=self.xy_padding)
        top_frame.pack(fill="both", expand=1)

        input_button = ttk.Button(
            top_frame,
            text="Select file(s)",
            command=self.get_input_paths,
        )
        input_button.grid(column=0, row=0)

        output_button = ttk.Button(
            top_frame,
            text="Save file(s)",
            command=self.get_output_path,
        )
        output_button.grid(column=0, row=1)

        input_label = tk.Label(
            top_frame,
            textvariable=self.input_value,
            wraplength=300,
            justify="left",
        )
        input_label.grid(
            cnf=self.xy_padding,
            column=1,
            row=0,
            columnspan=2,
            rowspan=2,
        )

        bottom_frame = tk.Frame(self, height=20)
        bottom_frame.pack(fill="x", expand=1)

        self.progressbar = ttk.Progressbar(
            bottom_frame,
            orient="horizontal",
            mode="indeterminate",
            length=400,
        )

    def convert(self):
        """Convert the given `.csv` files into one or more
        `docx` files.
        """
        # Execution setup:
        self.converter.input_path = self.input_paths
        self.converter.output_path = self.output_path.get()

        self.start_progressbar()

        # Execution:
        self.converter.convert()

        self.stop_progressbar()

        # Execution completion:
        messagebox.showinfo(
            "Info",
            self.converter.show_saved_status(),
        )
        self.reset_values()

    def get_input_paths(self):
        input_path = askopenfilenames(
            title="Open File(s)",
            initialdir=ROOT_PATH,
            filetypes=[("CSV files", "*.csv")],
        )
        if input_path:
            self.input_paths = input_path
            self.input_value.set(value="\n".join(self.input_paths))

    def get_output_path(self):
        if self.input_paths:
            docx_output_path = asksaveasfilename(
                title="Save File",
                initialdir=ROOT_PATH,
                defaultextension=".docx",
                filetypes=[("Word Document", "*.docx")],
                confirmoverwrite=True,
            )
            if docx_output_path:
                self.output_path.set(docx_output_path)
                self.convert()
        else:
            self.get_input_paths()

    def start_progressbar(self):
        self.progressbar.pack()
        self.progressbar.start()

    def stop_progressbar(self):
        self.progressbar.stop()
        self.progressbar.pack_forget()

    def reset_values(self):
        """Reset program to start state."""
        self.input_paths = []
        self.input_value.set(value="")
