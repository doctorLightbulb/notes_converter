"""
A module containing data structure classes for cleaning and storing the notes
along with helper functions.

Classes
-------
- Note
- Entry

Functions
---------
- get_book_name()
- get_chapter_number()
- get_verse_numbers()
- create_notes()
"""

import re
from typing import Dict, List, Tuple

from notes_converter.utils.converters import replace_quotes

# REGULAR EXPRESSIONS:
book_pattern = re.compile(
    r"churchofjesuschrist.org/study/scriptures/(.*)/(.*).*/(\d+)\?"
)
chapter_pattern = re.compile(r".*/(\d+)\?")
verse_pattern = re.compile(r"=p(\d+)")

ruler_pattern = re.compile(r"\s\s(-){2,}\s\s")


# NOTE CLASS
# The Note class processes the information stored in it (pre-database storage).
class Note:
    """
    Represents a single note.

    Attributes
    ----------
    _type : str
        The kind of note (usually "highlight").
    title : str
        The title of the note.
    note_text : str
        The actual text of the note.
    source_location : str
        A URL to the note's source at Gospel Library Online.
    tags : str
        A tag category of the form `tag 1;tag 2`. (Used for grouping.)
    notebooks : str
        The notebook(s) to which the note belongs. (Used for grouping.)
    study_set : str
        The study set to which the note belongs. (Used for grouping.)
    last_updated : str
        The date when the note was last edited.
    created : str
        The date when the note was first created.

    Methods
    -------
    create_reference():
        Creates a scriptural reference of the form Mormon: 4:10.
    clean_note_text():
        Cleans the body of the note by removing artifacts.
    resolve_titles():
        Assigns the reference to notes with no titles ("undefined").
        Call _after_ calling `create_reference()`.
    values():
        Returns all attribute values as a list.
    """

    def __init__(
        self,
        type_: str,
        title: str,
        note_text: str,
        source_location: str,
        tags: str,
        notebooks: str,
        study_set: str,
        last_updated: str,
        created: str,
    ) -> None:
        self.type_ = type_
        self.title = title
        self.note_text = note_text
        self.source_location = source_location
        self.tags = tags
        self.notebooks = notebooks
        self.study_set = study_set
        self.last_updated = last_updated
        self.created = created
        self.reference = None
        self.chapter = None  # Needed for sorting.
        self.verse = None  # Needed for sorting.

        self.mapping: Dict[str, str] = dict()

    def create_reference(self):
        """Creates the scriptural reference of the form `Mormon 4:10`."""
        book = get_book_name(book_pattern, self.source_location, self.mapping)
        chapter = get_chapter_number(chapter_pattern, self.source_location)
        verse = get_verse_numbers(verse_pattern, self.source_location)
        self.reference = f"{book} {chapter}:{verse}"
        self.chapter = chapter
        self.verse = verse

    def clean_note_text(self):
        """
        Cleans the `note_text` by removing  unwanted artifacts.

        Removes newline characters and replaces simple hyphens and quotation
        marks with fancy versions and renders ugly bracketed dates into prettier,
        long-hand versions.
        """
        text = self.note_text.replace("\n", " ")  # Combine split lines.
        paragraphs = text.replace("   ", "\n")  # Redefine paragaphs.
        unruled = re.sub(ruler_pattern, "", paragraphs)
        replaced_quotes = replace_quotes(unruled)

        self.note_text = replaced_quotes

    def resolve_titles(self, substitute=True):
        """
        Assigns the reference as a title to notes without titles.
        This method should be called after calling `create_references()`.
        """
        if self.title == "undefined":
            if substitute:
                self.title = self.reference
            else:
                self.title = ""

    def values(self):
        """Returns a list of all note values."""
        return [
            self.type_,
            self.title,
            self.note_text,
            self.source_location,
            self.tags,
            self.notebooks,
            self.study_set,
            self.last_updated,
            self.created,
            self.reference,
            self.chapter,
            self.verse,
        ]

    def __str__(self):
        return (
            f"Note(type_={self.type_!r}, title={self.title!r}, note_text={self.note_text!r}, "
            f"source_location={self.source_location!r}, tags={self.tags!r}, "
            f"notebooks={self.notebooks!r}, study_set={self.study_set!r}, last_updated={self.last_updated!r}, "
            f"created={self.created!r}, reference={self.reference!r})"
        )


# HELPER FUNCTIONS FOR THE NOTE CLASS


def get_book_name(pattern: re.Pattern, url: str, mappings: Dict[str, str]) -> str:
    """
    Searches for a book name with the given `pattern`.

    If one is found, convert it using the dictionary key-value pairs in
    `mappings`. If none is found, return `url` unmodified.

    Parameters
    ----------
    pattern : re.Pattern
        A regular expression pattern for searching.
    url : str
        A scriptural reference URL from Gospel Library Online.
    mappings : Dict[str, str]
        A dictionary mapping url book names to their scriptural equivalents.

    Returns
    -------
    str
        Either the book name or the URL as a string.
    """
    record = re.search(pattern, url)
    if record is None:
        return url
    record_mapped = mappings.get(record.group(2), url)
    return record_mapped


def get_chapter_number(pattern: re.Pattern, url: str) -> int | str:
    """
    Searches for a chapter number with the given `pattern`.

    If one is found, convert it to an integer and return it. If none is
    found, return `url` unmodified.

    Parameters
    ----------
    pattern : re.Pattern
        A regular expression pattern for searching.
    url : str
        A scriptural reference URL from Gospel Library Online.

    Returns
    -------
    str | int
        Either the chapter number as an integer or the URL as a string.
    """
    chapter = re.search(pattern, url)
    if chapter is None:
        return url
    return int(chapter.group(1))


def get_verse_numbers(pattern: re.Pattern, url: str) -> int | str:
    """
    Searches for a verse number with the given `pattern`.

    If one is found, convert it to an integer and return it. If none is found,
    return `url` unmodified.

    Parameters
    ----------
    pattern : re.Pattern
        A regular expression pattern for searching.
    url : str
        A scriptural reference URL from Gospel Library Online.

    Returns
    -------
    str | int
        Either the verse number as an integer or the URL as a string.
    """
    verse = re.search(pattern, url)
    if verse is None:
        return url
    return int(verse.group(1))


# ENTRY CLASS
# The Entry class stores a single note retrieved from the database (post database).
class Entry:
    """
    Represents a single note.

    Attributes
    ----------
    _type : str
        The kind of note (usually "highlight").
    title : str
        The title of the note.
    note_text : str
        The actual text of the note.
    source_location : str
        A URL to the note's source at Gospel Library Online.
    tags : str
        A tag category of the form `tag 1;tag 2`. (Used for grouping.)
    notebooks : str
        The notebook(s) to which the note belongs. (Used for grouping.)
    study_set : str
        The study set to which the note belongs. (Used for grouping.)
    last_updated : str
        The date when the note was last edited.
    created : str
        The date when the note was first created.
    reference : str
        The scriptural reference of the form: Mormon 4:10.
    chapter : int
        The chapter number.
    verse : int
        The verse number.
    """

    __slots__ = (
        "type_",
        "title",
        "note_text",
        "source_location",
        "tags",
        "notebooks",
        "study_set",
        "last_updated",
        "created",
        "reference",
        "chapter",
        "verse",
    )

    def __init__(
        self,
        type_: str,
        title: str,
        note_text: str,
        source_location: str,
        tags: str,
        notebooks: str,
        study_set: str,
        last_updated: str,
        created: str,
        reference: str,
        chapter: int,
        verse: int,
    ):
        self.type_ = type_
        self.title = title
        self.note_text = note_text
        self.source_location = source_location
        self.tags = tags
        self.notebooks = notebooks
        self.study_set = study_set
        self.last_updated = last_updated
        self.created = created
        self.reference = reference
        self.chapter = chapter
        self.verse = verse


# OTHER FUNCTIONS


def create_notes(notes: List[Tuple]) -> List[Entry]:
    """Adds each note to an `Entry` class and returns the entries in a list."""
    return [Entry(*i) for i in notes]
