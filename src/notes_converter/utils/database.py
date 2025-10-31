"""
Contains query constants and one function.

Functions
---------
- save_to_database()

Constants
---------
- CREATE_TABLE
- COMMIT_NOTE
- FETCH_NOTES
"""

import sqlite3
from datetime import datetime
from typing import List

from notes_converter.utils.structures import Note

# SETUP QUERIES

CREATE_TABLE = """
    CREATE TABLE IF NOT EXISTS notes(
        type                TEXT,
        title               TEXT,
        note_text           TEXT,
        source_location     TEXT,
        tags                TEXT,
        notebooks           TEXT,
        study_set           TEXT,
        last_updated        TEXT,
        created             TEXT,
        reference           TEXT,
        chapter             INTEGER,
        verse               INTEGER,
        UNIQUE(created)
    )
"""

# COMMIT QUERIES

COMMIT_NOTE = """
    INSERT INTO notes VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

# FETCH QUERIES

FETCH_NOTES = """
    SELECT type,
        title,
        note_text,
        source_location,
        tags,
        notebooks,
        study_set,
        last_updated,
        created,
        reference,
        chapter,
        verse 
    FROM notes
    WHERE reference LIKE "{}%"
    ORDER BY chapter ASC, verse ASC, created ASC;
"""

FETCH_DATE = """
    SELECT last_updated, rowid FROM notes WHERE created LIKE "{}"
"""

UPDATE_NOTE = """
    UPDATE notes
    SET
        type = ?,
        title = ?,
        note_text = ?,
        source_location = ?,
        tags = ?,
        notebooks = ?,
        study_set = ?,
        last_updated = ?,
        created = ?,
        reference = ?,
        chapter = ?,
        verse = ?
    WHERE rowid = ?
"""


def save_to_database(connection: sqlite3.Connection, notes: List[Note]):
    """Saves the current batch of notes to a database."""
    # The method executemany() would be more efficient, but it lacks
    # needed error handling and would skip an entire batch of notes
    # if it encounters ONE duplicate note.
    latest_notes: List[List[str]] = []
    for note in notes:
        try:
            connection.execute(COMMIT_NOTE, note.values())
        except sqlite3.IntegrityError as e:

            # Test whether the duplicate's date is newer
            # than that of the existing note:
            # TODO:
            # This feature needs more testing.
            existing_note = connection.execute(
                FETCH_DATE.format(note.created)
            ).fetchone()

            existing_date = datetime.fromisoformat(existing_note[0])
            new_date = datetime.fromisoformat(note.last_updated)

            # If the date is newer, add the note to the update batch:
            if new_date > existing_date:
                row_id = [existing_note[1]]
                latest_notes.append(note.values() + row_id)
            continue

    # Update latest notes (if any) in one transaction:
    if latest_notes:
        connection.executemany(UPDATE_NOTE, latest_notes)

    connection.commit()
