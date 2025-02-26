"""A module containing convenience paths."""

from pathlib import Path

# ############ PATHS #############

ROOT_PATH = Path.home()
CWD = Path.cwd()

TEST_DATA_PATH = CWD / "tests"

DATA_PATH = CWD / "data"
TEMPLATE_PATH = CWD / "templates"

# ######## OTHER CONSTANTS #########

FIELD_NAMES = [
    "type",
    "title",
    "note_text",
    "source_location",
    "tags",
    "notebooks",
    "study_set",
    "last_updated",
    "created",
    "highlight",
]
