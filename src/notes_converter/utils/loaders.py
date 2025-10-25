"""
A module containing all functions that load data, along with any helper functions.

Functions
---------
- load_json()
- load_csv()
"""

import csv
import json
from pathlib import Path
from typing import Dict


def load_json(path: Path | str) -> Dict[str, str]:
    """
    Load a `.json` file in `utf-8` encoding.

    Parameters
    ----------
    path : Path
        A string or Path object.

    Returns
    -------
    Dict
        The contents of the `.json` file.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_csv(path: Path | str):
    """
    Load a `csv` file in `utf-8` encoding and skip the header line.

    Parameters
    ----------
    path : Path
        A string or Path object.

    Returns
    -------
    csv.Reader
        A `csv.generator` object containing a pointer to the `.csv` file.
    """
    reader = csv.reader(open(path, encoding="utf-8"))
    next(reader)
    return reader
