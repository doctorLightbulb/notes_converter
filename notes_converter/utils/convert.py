"""A module containing conversion functions and their helper functions."""

import re
from collections import namedtuple
from typing import Dict, List, Union

TAGS: set[str] = set()
NOTEBOOKS: set[str] = set()


def build_notes(
    notes_list: List[Dict[str, Union[str, List[str]]]], field_names: List[str]
):
    """Build a list of notes using a `namedtuple` object.

    Parameters
    ----------
    notes_list : A `list` of dictionaries.

    Returns
    -------
    A list of `namedtuple` objects.
    """

    Note = namedtuple("Note", field_names=field_names)

    notes = []
    for n in notes_list:
        n = process_note(n)
        values = [value if value else "" for value in n.values()]
        note = Note(*values)
        notes.append(note)
    return notes


def process_note(note):
    """Convert a note's `note_text`, `tags` and `notebooks` to lists,
    and remove the date and ruler, and update the `TAGS` and `NOTEBOOKS`
    constants.
    """
    n = convert_note_text_to_list(note)
    _n = convert_note_identifiers_to_list(n)
    cleaned_n = remove_headers(_n)

    add_tags(TAGS, cleaned_n["tags"])
    add_tags(NOTEBOOKS, cleaned_n["notebooks"])

    return cleaned_n


# process_note() helper functions


def add_tags(tags_set, new_tags) -> None:
    tags_set.update(new_tags)


def strip_artifacts(line: str) -> Union[str, None]:
    """Strip unwanted parts of a list."""
    if line.startswith("[") or line.startswith("-----"):
        return ""
    return line


def remove_headers(note):
    """Remove unwanted text at the head of a list."""
    n = [strip_artifacts(_) for _ in note["note_text"]]
    cleaned_n = [_ for _ in n if _.strip()]  # Remove empty values
    note["note_text"] = cleaned_n
    return note


def convert_note_text_to_list(note):
    """Convert `note`'s `note_text` value to a list using `re.findall()`.

    Parameters
    ----------
    note : A `dict` object.

    Returns
    -------
    A `dict` object with only its `["note_text"]` value changed.
    """
    paragraphs = re.compile(r"([^\n]+(?:\n(?!\n)[^\n]+)*)")
    p = paragraphs.findall(note["note_text"])
    text = [i.replace("\n", " ") for i in p]
    note["note_text"] = text
    return note


def convert_note_identifiers_to_list(note: Dict) -> Dict:
    """Convert a note's `["tags"]` and `["notebooks"]` values to lists.

    Parameters
    ----------
    note : A `dict` object.

    Returns
    -------
    A `dict` object with only its `["tags"]` and `["notebooks"]` values
    changed.
    """
    tags: List[str] = note["tags"].split("; ")
    note["tags"] = tags
    notebooks: List[str] = note["notebooks"].split("; ")
    note["notebooks"] = notebooks

    return note


# Functions to build references using the URL under note.source_location.


def extract_study_data(raw_data, name_maps):
    """Extract scriptures' record, book, chapter and verse names and numbers
    and return a dict."""

    # TODO: Add allowance for paragraph ranges (i.e. =p4-p6).
    # TODO: Need full support for General Conference references.

    def process_scriptures(raw_data):
        """Extract book name, chapter and verse from `raw_data`.

        Parameters
        ----------
        - raw_data : A list containing url elements.

        Returns
        -------
        A list of keys and the book name, chapter and verse.
        """
        p_num = raw_data[-1:][0].split("=p")[-1:]  # Get paragraph number
        c_num = raw_data[-1:][0].split("?")[0:1]  # Get chapter number
        b_name = raw_data[-2:-1]  # Get book name

        # Mapping for the opening and closing pages, such as title, references
        # pronunciation, etc.
        opening_closing_pages = ["three", "js", "eight", "introduction"]
        if c_num[0] in opening_closing_pages:
            data = raw_data[1:2] + c_num + p_num
            keys = ["book", "sub_book", "verse"]
            return keys, data

        # Mapping for the main books.
        data = raw_data[1:2] + b_name + c_num + p_num
        keys = ["book", "sub_book", "chapter", "verse"]
        return keys, data

    def process_manuals(raw_data):
        p_num = raw_data[-1:][0].split("=p")[-1:]  # Get paragraph number
        c_num = raw_data[-1:][0].split("?")[0:1]  # Get chapter number
        b_name = raw_data[1:2]  # Get book name

        data = b_name + c_num + p_num
        keys = ["manual", "chapter", "verse"]
        return keys, data

    def process_ensigns(raw_data):
        p_num = raw_data[-1:][0].split("=p")[-1:]  # Get paragraph number
        a_name = raw_data[-1:][0].split("?")[0:1]  # Get article name
        e_month = raw_data[2:3]  # Get month
        e_year = raw_data[1:2]  # Get Ensign year

        data = e_year + e_month + a_name + p_num
        keys = ["ensign", "month", "article", "verse"]
        return keys, data

    versions = {
        "scriptures": process_scriptures,
        "manual": process_manuals,
        "ensign": process_ensigns,
    }
    data = raw_data.split("/")
    record = data[4:5][0]
    x = versions.get(record, process_scriptures)
    key_maps, groups = x(data[4:])

    # Map shorthand names to long-hand names.
    values = [name_maps.get(i, i) for i in groups]

    return dict(zip(key_maps, values))


def build_study_references(data):
    reference_numbers = f"{data["verse"]}"
    books = ""
    if "chapter" in data.keys():
        reference_numbers = f"{data["chapter"]}:{data["verse"]}"
    if "ensign" in data.keys():
        books = f"Ensign, {data["month"]} {data["ensign"]}, {data["article"]}, "
    if "manual" in data.keys():
        books = f"{data["manual"]}, "
    if "book" and "sub_book" in data.keys():
        books = f"{data["book"]}, {data["sub_book"]} "
    reference = books + reference_numbers

    return reference
