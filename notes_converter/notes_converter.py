"""A module containing everything to do with the notes_converter
engine.
"""

from pathlib import Path
from typing import Any, List

from utils.check import SystemMemory, check_file_size
from utils.constants import DATA_PATH, FIELD_NAMES
from utils.convert import build_notes
from utils.load import load_csv_files, load_json
from utils.sort import sort_notes_by_title_and_verse
from utils.write import write_to_docx

# from utils import (
#     DATA_PATH,
#     FIELD_NAMES,
#     SystemMemory,
#     build_notes,
#     check_file_size,
#     load_csv_files,
#     load_json,
#     sort_notes_by_title_and_verse,
#     write_to_docx,
# )


class NotesConverter:
    def __init__(self) -> None:
        self.input_path: List[Any] = []
        self.output_path = Path()
        self.template_path = None
        self._smu = SystemMemory()

    def convert(self):
        """Convert the specified files using either
        `self.convert_with_full_memory` or `self.convert_with_limited_memory`.
        """
        self.output_path = Path(self.output_path)

        # Estimated memory needed to run the program
        overhead_memory = 10  # in megabytes

        # Estimated memory needed to convert the input file(s)
        conversion_memory = check_file_size(self.input_path)  # in megabytes
        total_memory_needed = overhead_memory + conversion_memory

        enough_memory = self._smu.check_memory(megabytes=total_memory_needed)
        if enough_memory:
            sorted_notes = self.convert_with_full_memory(self.input_path)
        else:
            sorted_notes = self.convert_with_limited_memory(self.input_path)
            # TODO: Pass the data from one generator to another. The second
            # generator must convert each note into a namedtuple object in
            # order to be used by write_to_docx()
            return  # Remove for production

        write_to_docx(
            notes=sorted_notes,
            output_path=self.output_path,
            template_path=self.template_path,
        )

        return "".join(self.show_saved_status())

    def convert_with_full_memory(self, notes_paths):
        """Convert the notes by loading them all into memory
        before writing them to a `.docx` file.

        Parameters
        ----------
        - notes_paths : The paths to the files to load.

        Returns
        -------
        A list of notes built using a `namedtuple` object.
        """

        merged_notes = load_csv_files(notes_paths, FIELD_NAMES)
        notes = build_notes(merged_notes, FIELD_NAMES)

        # TODO: Add support for splitting the notes on tag or notebook.

        title_order = load_json(DATA_PATH / "standard_works_order.json")
        sorted_notes = sort_notes_by_title_and_verse(notes, title_order)
        return sorted_notes

    def convert_with_limited_memory(self, notes_paths):
        """Convert and sort all notes using a `SQLite3` database.

        Parameters
        ----------
        - notes_paths : The paths to the notes to be loaded.

        Returns
        -------
        A generator object connected directly to the database.
        """
        print("Low system memory.")

    def show_saved_status(self):
        return (
            f"{self.output_path.stem} saved successfully!\n",
            "File saved in the following location:\n",
            f"{self.output_path.parent}",
        )
