"""A module containing conversion functions and their helper functions."""

import re
from typing import Match

MAPPING = {
    ' "': " “",  # Beginning quotation (e.g.,
    '" ': "” ",  # Ending quotation
    '."': ".”",  # Ending quotation
    '"\n': "”\n",  # Ending quotation
    '"': "“",  # Default Quote (e.g.,
    '\n"': "\n“",  # Needed for raw strings only (e.g., \n"Good morning...").
    "'": "’",  # Default apostrophie (e.g., I'm).
    " '": " ‘",  # Beginning apostrophie (e.g., 'tis).
    "\n'": "\n‘",
}


def replace(m: Match) -> str:
    return MAPPING[m.group(0)]


def replace_quotes(text: str) -> str:
    """Replaces plain quotation marks and apostrophies with fancy ones."""
    pattern = re.compile(
        r"""
        (\s\"|\"\s|\.\"|\"|\s\'|\n\'|\')
    """,
        re.VERBOSE,
    )
    return pattern.sub(replace, text)
