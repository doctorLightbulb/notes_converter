"""A module containing the `NotesConverter` engine."""

import sqlite3
from pathlib import Path
from typing import Any, Dict, List

from notes_converter.utils.checkers import SystemMemory, check_required_memory
from notes_converter.utils.constants import DATA_PATH
from notes_converter.utils.database import (
    CREATE_TABLE_QUERY,
    FETCH_NOTES,
    save_to_database,
)
from notes_converter.utils.loaders import load_csv, load_json
from notes_converter.utils.structures import Note, create_notes
from notes_converter.utils.writers import DocxWriter, write_to_txt


class NotesConverter:
    """
    Converts a `csv` file to an MS Word document.

    Attributes
    ----------
    input_paths : List[Any]
        Paths to the files to convert.
    output_path : Path
        The directory in which to save the converted document.
    template_path : None
        The path to a custom MS Word template to use. Default is `None`.
    _smu : SystemMemory
        The SystemMemory class for memory and storage inspection.

    Methods
    -------
    convert():
        Converts the given `csv` file(s) to a tidy MS Word document.
    show_saved_status():
        Returns a message that the file was saved successfully.
    """

    def __init__(self) -> None:
        self.input_paths: List[Any] = []
        self.output_path = Path()
        self.template_path = None
        self._smu = SystemMemory()

    def convert(self):
        """
        Convert the specified files.

        The conversion process used depends on whether the system has enough
        memory for the conversion. If it does, a virtual SQLite3 database is
        used. If not, a regular SQLite3 database is used.
        """
        self.output_path = Path(self.output_path)
        enough_memory = check_required_memory(self.input_paths, self._smu)

        if enough_memory:
            database_path = ":memory:"
        else:
            database_path = "some/path"

        # Process notes and load database
        mapped_names = load_json(DATA_PATH / "book_codes.json")
        book_names = load_json(DATA_PATH / "standard_works.json")

        # Word document writer
        writer = DocxWriter(self.output_path, self.template_path)

        # Due to the temporary database functionality, all database
        # execution must be done without closing the connection.
        with sqlite3.connect(database_path) as connection:

            # Database initialization.
            connection.execute(CREATE_TABLE_QUERY)

            clean_data(connection, self.input_paths, mapped_names)
            create_docx(connection, writer, book_names)

        # TODO: Add support for splitting the notes on tag or notebook.
        connection.close()

        return "".join(self.show_saved_status())

    def show_saved_status(self):
        return (
            f"{self.output_path.stem} saved successfully!\n",
            "File saved in the following location:\n",
            f"{self.output_path.parent}",
        )


def clean_data(connection, paths: List[Path], mapping: Dict[str, str]) -> None:
    # Process all given input files (either 1 or more).
    for path in paths:
        raw_notes = load_csv(path)

        # Process the notes of a given file.
        notes_segment = []
        for _tuple in raw_notes:
            note = Note(*_tuple)
            note.mapping = mapping
            note.clean_note_text()
            note.create_reference()

            notes_segment.append(note)

            # Save the notes to the database in segments
            # to minimize memory consumption.
            if len(notes_segment) == 99:
                save_to_database(connection, notes_segment)
                notes_segment.clear()


def create_docx(connection, writer: DocxWriter, books: Dict[str, str]) -> None:
    # Retrieve notes by book, sorted by chapter and verse.
    # The book can also be a General Conference address or
    # any other Church manual or book.
    for record in books.keys():
        writer.write_heading(record)
        for book in books[record]:
            retrieved_notes = connection.execute(FETCH_NOTES.format(book)).fetchall()

            # If there are no notes for a given book, skip to the next book.
            if not retrieved_notes:
                continue

            book_notes = create_notes(retrieved_notes)
            writer.write_notes(book_notes)
