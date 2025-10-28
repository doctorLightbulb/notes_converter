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


def save_to_database(connection: sqlite3.Connection, notes: List[Note]):
    """Saves the current batch of notes to a database."""
    listed_notes = [i.values() for i in notes]
    connection.executemany(COMMIT_NOTE, listed_notes)
    connection.commit()
