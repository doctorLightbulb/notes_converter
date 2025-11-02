"""
Contains the main converter engine.

Classes
-------
- NotesConverter()
"""

import itertools
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

from notes_converter.utils.checkers import SystemMemory, check_required_memory
from notes_converter.utils.constants import DATA_PATH
from notes_converter.utils.database import (
    CREATE_TABLE,
    FETCH_NOTEBOOKS,
    FETCH_NOTES,
    FETCH_NOTES_BY_NOTEBOOK,
    save_to_database,
)
from notes_converter.utils.loaders import load_csv, load_json
from notes_converter.utils.structures import Note, create_notes
from notes_converter.utils.writers import DocxWriter


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
        self.input_paths: List[Path] = []
        self.output_path = Path()
        self.template_path = Path()
        self.database_path = Path.home() / "Downloads"
        self._smu = SystemMemory()

        self.database_is_virtual = False
        self.group_by_notebook = False

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
            self.database_is_virtual = not self.database_is_virtual
        else:
            database_path = (
                self.database_path
                / f"Temporary Gospel Library Cache ({str(datetime.now()).split()[0]}).db"
            )

        # Load reference data:
        mapped_names = load_json(DATA_PATH / "book_codes.json")
        book_names = load_json(DATA_PATH / "standard_works.json")

        # Due to the temporary database functionality, all database
        # execution must be done without closing the connection.
        with sqlite3.connect(database_path) as connection:

            # Database initialization.
            connection.execute(CREATE_TABLE)
            writer = DocxWriter(self.output_path, self.template_path)

            _clean_data(connection, self.input_paths, mapped_names)

            if self.group_by_notebook:
                notebooks = extract_notebooks(
                    connection.execute(FETCH_NOTEBOOKS).fetchall(),
                )
                for notebook in notebooks:
                    docx_name_path = build_file_name(self.output_path, notebook)
                    writer = DocxWriter(docx_name_path)
                    _create_notebook_docx(
                        connection,
                        FETCH_NOTES_BY_NOTEBOOK,
                        notebook,
                        writer,
                        book_names,
                    )
            else:
                _create_docx(connection, FETCH_NOTES, writer, book_names)

        connection.close()

        # Delete the temporary database if an on-disk one was used:
        if not self.database_is_virtual:
            database_path.unlink()

        return self.show_saved_status()

    def show_saved_status(self):
        return "".join(
            (
                f"{self.output_path.stem} saved successfully!\n",
                "File saved in the following location:\n",
                f"{self.output_path.parent}",
            )
        )


def build_file_name(path: Path, notebook) -> Path:
    parent = path.parent
    name = path.stem
    extension = path.suffix
    file_name = f"{name} ({notebook}){extension}"
    return Path(parent, file_name)


def extract_notebooks(raw_notebooks: List[Tuple[str]]):
    return {_ for i in raw_notebooks for _ in i[0].split("; ") if i[0].strip()}


def _clean_data(connection, paths: List[Path], mapping: Dict[str, str]) -> None:
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


def _create_docx(
    connection, query: str, writer: DocxWriter, books: Dict[str, str]
) -> None:
    # Retrieve notes by book, sorted by chapter and verse.
    # The book can also be a General Conference address or
    # any other Church manual or book.
    for record in books.keys():
        writer.write_heading(record)
        for book in books[record]:
            retrieved_notes = connection.execute(query.format(book)).fetchall()

            # If there are no notes for a given book, skip to the next book.
            if not retrieved_notes:
                continue

            book_notes = create_notes(retrieved_notes)
            writer.write_notes(book_notes)


def _create_notebook_docx(
    connection, query: str, notebook: str, writer: DocxWriter, books: Dict[str, str]
) -> None:
    # Retrieve notes by book, sorted by chapter and verse.
    # The book can also be a General Conference address or
    # any other Church manual or book.
    for record in books.keys():
        writer.write_heading(record)
        for book in books[record]:
            retrieved_notes = connection.execute(
                query.format(book, notebook)
            ).fetchall()

            # If there are no notes for a given book, skip to the next book.
            if not retrieved_notes:
                continue

            book_notes = create_notes(retrieved_notes)
            writer.write_notes(book_notes)
