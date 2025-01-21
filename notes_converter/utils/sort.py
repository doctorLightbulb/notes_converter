"""A module containing sorting functions."""

import re


def sort_notes_by_title_and_verse(notes, title_order):
    """Sort notes by title and verse.

    Parameters
    ----------
    notes : A list of Note objects with `.title`, `.date` and `.body`
        attributes.

    title_order : A list of strings in the desired order for the output notes.

    Returns
    -------
    A list of `Note` objects sorted by title and verse.
    """
    indexed_titles = {title: index for index, title in enumerate(title_order)}
    chapter_verse_pattern = re.compile(r"\W(\d+|\d+:\d+)|;|:.*")

    def extract_chapter_and_verse(title):
        _match = [i for i in chapter_verse_pattern.findall(title) if i.strip()]
        index = 1
        if _match:
            chapter = int(_match[0])
            verse = int(_match[index]) if index < len(_match) else 0
            return chapter, verse
        return 0, 0

    def arrange_by_title_and_verse(note):
        title_without_verse = chapter_verse_pattern.sub("", note.title)
        chapter_index = indexed_titles.get(title_without_verse, float("inf"))
        chapter, verse = extract_chapter_and_verse(note.title)
        return chapter_index, chapter, verse

    return sorted(notes, key=arrange_by_title_and_verse)
