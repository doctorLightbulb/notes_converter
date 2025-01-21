"""A module containing all functions that load data, along with their helper
functions.
"""

import csv
import json
from pathlib import Path
from typing import List, Sequence, Union

from utils.decorators import remove_duplicates


def load_json(path):
    """Load a `.json` file in `utf-8` encoding.

    Parameters
    ----------
    path : A string or Path object.

    Returns
    -------
    The contents of the `.json` file.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_csv_as_dict(
    path: Union[Path, str],
    field_names: List[str],
) -> csv.DictReader:
    """Load a CSV into a `csv.DictReader` iterable.

    Parameters
    ----------
    path : A string or Path object to the file.
    field_names : A list of strings mapping to the csv fields.

    Returns
    -------
    A `csv.DictReader` iterable.
    """
    return csv.DictReader(open(path, encoding="utf-8"), fieldnames=field_names)


@remove_duplicates
def load_csv_files(files: Sequence[Union[Path, str]], field_names: List[str]):
    """Load multiple `csv` files and return a merged list.

    Parameters
    ----------
    files : A list containing the paths to the files.
        These can be either `str` or `Path` objects.
    field_names : A list of strings
        Containing the fields to which to map the csv columns.

    Returns
    -------
    A merged list of `dict`s.
    """
    notes = []
    for file in files:
        reader = load_csv_as_dict(file, field_names=field_names)
        next(reader)  # Skip titles (first line)
        notes += [note for note in reader]
    return notes
