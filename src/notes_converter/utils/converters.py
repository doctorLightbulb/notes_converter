"""A module containing conversion functions and their helper functions."""

import re
from datetime import datetime
from typing import Match

import pytz

MAPPING = {
    ' "': " “",  # Beginning quotation (e.g.,
    '" ': "” ",  # Ending quotation
    '."': ".”",  # Ending quotation
    '"\n': "”\n",  # Ending quotation
    '"': "“",  # Default Quote (e.g.,
    '\n"': "\n“",  # Needed for raw strings (e.g., \n"Good morning...").
    "'": "’",  # Default apostrophie (e.g., I'm).
    " '": " ‘",  # Beginning apostrophie (e.g., 'tis).
    "\n'": "\n‘",  # Needed for raw strings (e.g., \n"Good morning...").
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


def convert_datetime(note_time: str) -> str:
    """Converts dates of the form `2026-04-07T15:00:01.654Z` to `April 7, 2026, 08:00 AM PDT`"""
    default_time = datetime.fromisoformat(note_time.replace("Z", "+00:00"))
    dt = default_time.replace(tzinfo=pytz.utc)
    pacific_tz = pytz.timezone("America/Los_Angeles")
    dt_pacific = dt.astimezone(pacific_tz)
    return dt_pacific.strftime("%B %e, %Y, %I:%M %p %Z").replace("  ", " ")
