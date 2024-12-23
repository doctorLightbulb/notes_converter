"""A module containing all the GUI elements for `notes_converter`."""

import tkinter as tk


class MainWindow(tk.Tk):
    def __init__(self, converter):
        super().__init__()
        self.converter = converter

        # Screen orientation
        center_x = self.winfo_screenwidth() // 2
        center_y = self.winfo_screenheight() // 2
        window_width = 400
        window_height = 300
        x = center_x - window_width // 2
        y = center_y - window_height // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Initialize GUI
        self.create_gui()

    def create_gui(self):
        bottom_frame = tk.Frame(self)
        bottom_frame.pack(side="bottom", expand=1)

        convert_button = tk.Button(
            bottom_frame,
            text="Convert",
            command=self.convert,
        )
        convert_button.pack()

    def convert(self):
        self.converter.convert()


# test_csvs = TEST_DATA_PATH
# notes_input_path = [test_csvs / "test_1.csv", test_csvs / "test_2.csv"]
# notes_input_path = askopenfilenames(
#     title="Open File",
#     initialdir=ROOT_PATH,
#     filetypes=[("CSV files", "*.csv")],
# )
# docx_output_path = asksaveasfilename(
#     title="Save File",
#     initialdir=ROOT_PATH,
#     defaultextension=".docx",
#     filetypes=[("Word Document", "*.docx")],
#     confirmoverwrite=True,
# )

# if not notes_input_path or not docx_output_path:
#     sys.exit(0)

# messagebox.showinfo(
#     "Info",
#     f"File {docx_output_path.split('/')[-1]} saved successfully!",
# )
