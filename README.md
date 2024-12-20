# README

We need to group the notes by note. Identifying features include two spaces at the head of each note. Usually a title comes next with date and the note body, which can be as little as one paragraph, though it is often more.

The paragraphs should be one line of text and must be stored in a list.

Structure a note this way:

```python
note = {
    "title": "Note's title",
    "date": "November 14, 2024",
    "note": [
        "first paragraph",
        "second paragraph",
        "third paragraph",
    ],
}
```

> ## Note
>
> Keep in mind that `notes["note"]` can also contain dates.

All note dictionaries will be stored in a list. This structure is necessary to enable sorting and convenient retrieval of notes.

Due to inconsistencies in the exported notes, regular expressions will have to be used.
