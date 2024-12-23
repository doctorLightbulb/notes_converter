"""`Notes Converter`

Convert a `.csv` file to a styled `.docx` file.
"""

import argparse
import sys
from pathlib import Path
from tkinter import messagebox
from tkinter.filedialog import askopenfilenames, asksaveasfilename

from gui import MainWindow

from notes_converter import NotesConverter


def parse_args():
    parser = argparse.ArgumentParser(
        description="A Tkinter application with command-line arguments.",
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        action="append",
        help="Input file names",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="The path to the target file.",
    )
    return parser.parse_args()


def main():

    converter = NotesConverter()

    # Command-line mode
    args = parse_args()
    if args.input:
        notes_input_path = [Path(i) for i in args.input]
        converter.notes_path = notes_input_path
        converter.convert()
    else:
        # GUI mode
        window = MainWindow(converter)
        window.mainloop()


if __name__ == "__main__":
    main()
