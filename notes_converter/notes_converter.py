"""A module containing everything to do with the notes_converter
engine.
"""

from pathlib import Path

from utils import (
    DATA_PATH,
    FIELD_NAMES,
    build_notes,
    load_csv_files,
    load_json,
    sort_notes_by_title_and_verse,
    write_to_docx,
)


class NotesConverter:
    def __init__(self) -> None:
        self.input_path = []
        self.output_path = ""

    def convert(self):
        self.output_path = Path(self.output_path)

        merged_notes = load_csv_files(self.input_path, FIELD_NAMES)
        notes = build_notes(merged_notes, FIELD_NAMES)

        # TODO: Add support for splitting the notes on tag or notebook.

        title_order = load_json(DATA_PATH / "standard_works_order.json")
        sorted_notes = sort_notes_by_title_and_verse(notes, title_order)

        write_to_docx(sorted_notes, self.output_path)

        return "".join(self.show_saved_status())

    def show_saved_status(self):
        return (
            f"{self.output_path.stem} saved successfully!\n",
            "File saved in the following location:\n",
            f"{self.output_path.parent}",
        )
