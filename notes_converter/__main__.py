"""`Notes Converter`

Convert a `.csv` file to a styled `.docx` file.
"""

import sys
from tkinter import messagebox
from tkinter.filedialog import askopenfilenames, asksaveasfilename

from utils import (
    CSV_PATH,
    DATA_PATH,
    FIELD_NAMES,
    NOTEBOOKS,
    ROOT_PATH,
    TAGS,
    TEST_DATA_PATH,
    build_notes,
    load_csv_files,
    load_json,
    sort_notes_by_title_and_verse,
    write_to_docx,
)


def main():
    notes_input_path = [CSV_PATH]
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

    merged_notes = load_csv_files(notes_input_path, FIELD_NAMES)
    notes = build_notes(merged_notes, FIELD_NAMES)

    # TODO: Add support for splitting the notes on tag or notebook.

    title_order = load_json(DATA_PATH / "standard_works_order.json")
    sorted_notes = sort_notes_by_title_and_verse(notes, title_order)

    write_to_docx(sorted_notes, "Gospel Library Notes.docx")

    # messagebox.showinfo(
    #     "Info",
    #     f"File {docx_output_path.split('/')[-1]} saved successfully!",
    # )


if __name__ == "__main__":
    main()
