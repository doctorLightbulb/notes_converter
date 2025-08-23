import re
from typing import List, Tuple

# Regular expressions:
book_pattern = re.compile(
    r"churchofjesuschrist.org/study/scriptures/(.*)/(.*).*/(\d+)\?"
)
chapter_pattern = re.compile(r".*/(\d+)\?")
verse_pattern = re.compile(r"=p(\d+)")

ruler_pattern = re.compile(r"\s\s(-){2,}\s\s")


class Note:
    """A massive class that handles data storage and cleaning."""

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

        self.mapping = None

    def create_reference(self):
        """Create the scriptural reference of the form:
        Mormon 4:10
        """
        book = get_book_name(book_pattern, self.source_location, self.mapping)
        chapter = get_chapter_number(chapter_pattern, self.source_location)
        verse = get_verse_numbers(verse_pattern, self.source_location)
        self.reference = f"{book} {chapter}:{verse}"
        self.chapter = chapter
        self.verse = verse

    def clean_note_text(self):
        """Clean the `note_text` by removing newline characters, replacing simple
        hyphens and quotation marks with fancy versions and rendering ugly
        bracketed dates into prettier, long-hand versions.
        """
        text = self.note_text.replace("\n", " ")  # Combine split lines.
        paragraphs = text.replace("   ", "\n")  # Redefine paragaphs.
        unruled = re.sub(ruler_pattern, "", paragraphs)
        self.note_text = unruled

    def values(self):
        """Return a list of all values."""
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


# HELPER FUNCTIONS FOR CLASS NOTE


def get_book_name(pattern, url, mappings) -> str:
    """Search for a book name with the given `pattern`. If one is found,
    convert it using the dictionary key-value pairs in `mappings`. If
    none is found, return `url` unmodified.

    Parameters
    ----------
    pattern : A regular expression pattern for searching.
    url : A scripture reference URL from Gospel Library Online.
    mappings : A dictionary mapping url book names to their scriptural equivalents.

    Returns
    -------
    Either the book name or the URL as a string.
    """
    record = re.search(pattern, url)
    if record is None:
        return url
    record_mapped = mappings.get(record.group(2), url)
    return record_mapped


def get_chapter_number(pattern, url: str) -> int | str:
    """Search for a chapter number with the given `pattern`. If one is found,
    convert it to an integer and return it. If none is found, return `url`
    unmodified.

    Parameters
    ----------
    pattern : A regular expression pattern for searching.
    url : A scripture reference URL from Gospel Library Online.

    Returns
    -------
    Either the chapter number as an integer or the URL as a string.
    """
    chapter = re.search(pattern, url)
    if chapter is None:
        return url
    return int(chapter.group(1))


def get_verse_numbers(pattern, url) -> int | str:
    """Search for a verse number with the given `pattern`. If one is found,
    convert it to an integer and return it. If none is found, return `url`
    unmodified.

    Parameters
    ----------
    pattern : A regular expression pattern for searching.
    url : A scripture reference URL from Gospel Library Online.

    Returns
    -------
    Either the verse number as an integer or the URL as a string.
    """
    verse = re.search(pattern, url)
    if verse is None:
        return url
    return int(verse.group(1))


class Entry:
    """A simple data storage class that does nothing else."""

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


def create_notes(notes: List[Tuple]):
    """Add all notes to an `Entry` class and return them in a list."""
    return [Entry(*i) for i in notes]
