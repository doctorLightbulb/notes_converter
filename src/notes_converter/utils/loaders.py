"""A module containing all functions that load data, along with their helper
functions.
"""

import csv
import json
from pathlib import Path


def load_json(path):
    """Load a `.json` file in `utf-8` encoding.

    Parameters
    ----------
    path : A string or Path object.

    Returns
    -------
    The contents of the `.json` file as a dictionary.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_csv(path: Path):
    """Load a `csv` file in `utf-8` encoding, skip the header line
    and return a generator object.

    Parameters
    ----------
    path : A string or Path object.

    Returns
    -------
    A `csv.generator` object containing a pointer to the `csv` file.
    """
    reader = csv.reader(open(path, encoding="utf-8"))
    next(reader)
    return reader
