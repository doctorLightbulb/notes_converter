"""A module containing all functions and classes pertaining to the database."""

import sqlite3
from pathlib import Path
from typing import List, Sequence, Union

from utils.load import load_csv_as_dict


def open_database(database):
    pass


def commit_to_database(
    database, files: Sequence[Union[Path, str]], field_names: List[str]
):
    for file in files:
        reader = load_csv_as_dict(file, field_names=field_names)
        next(reader)  # Skip titles (first line)
        with sqlite3.connect(database) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT into VALUES(?, ?, ?)")
