"""A module containing conversion functions and their helper functions."""

import re
from datetime import datetime
from typing import Match

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


def convert_datetime(note_time: str, timezone: bool = False) -> str:
    """
    Converts dates to a human-readable format.

    Given the date `2026-04-07T15:00:01.654Z`, the function returns
    `April 7, 2026, 8:00 a.m., Pacific Daylight Time`

    Parameters
    ----------
    note_time : str
        Date and time of the form `2026-04-07T15:00:01.654Z`.
    timezone : bool
        Whether or not to include the timezone in the output.

    Returns
    -------
    str
        Date and time of the form `April 7, 2026, 8:00 a.m.`
    """

    raw_datetime = datetime.fromisoformat(note_time)
    current_timezone = datetime.now().astimezone().tzinfo
    dt = raw_datetime.astimezone(current_timezone)

    meridian = {"PM": "p.m."}
    m = meridian.get(f"{dt:%p}", "a.m.")
    tz = f", {dt:%Z}" if timezone else ""
    return f"{dt:%B} {dt.day}, {dt:%Y}, {dt.hour%12 or 12}:{dt:%M} {m}{tz}"
