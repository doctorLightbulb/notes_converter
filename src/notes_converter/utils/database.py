"""Contains the Database class and related query constants."""

import sqlite3
from pathlib import Path

# SETUP QUERIES

CREATE_TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS notes(
        type,
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
        verse,
        UNIQUE(created)
    )
"""

# COMMIT QUERIES

COMMIT_NOTE_QUERY = """
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
    ORDER BY COALESCE(chapter, verse, created)
"""


class Database:
    """A class for committing data to and fetching data from a SQLite3
    database.
    """

    def __init__(self, path):
        virtual_database = path == ":memory:"
        if virtual_database:
            self.db_path = path
            self.create_empty_table(CREATE_TABLE_QUERY)
            return

        self.db_path = Path(path)

        database_exists = self.db_path.exists()
        database_dir_exists = self.db_path.parent.parent.exists()

        if not database_exists and database_dir_exists:
            self.db_path.parent.mkdir(exist_ok=True)
            self.create_empty_table(CREATE_TABLE_QUERY)

    @property
    def db_path(self):
        return self._db_path

    @db_path.setter
    def db_path(self, path):
        self._db_path = path

    def create_empty_table(self, query: str):
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute(query)

    def commit(self, query, data):
        """Commit data to the selected database."""
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute(query, data)
            connection.commit()

    def commit_many(self, query, data):
        """Commit data to the selected database."""
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.executemany(query, data)

    def update(self, query):
        """Commit data to the selected database."""
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()

    def fetch_matches(self, query, word):
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            results = cursor.execute(query.format(word))
            return results.fetchall()


def save_to_database(connection, notes):
    """Save the current batch of notes to a temporary database."""
    listed_notes = [i.values() for i in notes]
    connection.executemany(COMMIT_NOTE_QUERY, listed_notes)
    connection.commit()
