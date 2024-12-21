# Converter Pseudo Code

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

* Step 1:
Load the file.

* Step 2:
Process the file. Group by notes. Either a dict or a `namedtuple` can be used.

* Step 3:
Sort notes by a given order. In this case, we need a list containing the order by which to sort.

The sorting algorithm must take (1) the note title (if any) and (2) the sort-order list.

* Step 4:
Iterate over each note (a generator would be useful at this point) and add them to the Word document.

Currently, the program has no error handling for low system memory. Moreover, it would appear that `sorted()` cannot be used successfully with a generator. The solution to a huge file: Load it chunk by chunk into a sqlite3 database. Craft a query to sort the data as desired. Then return the results one row at a time using a generator function.

To make sorting easier, put each chapter and verse number in its own column.

By the time the input files become too large to process at once, the output file will likely be too large, also. As `notes_converter` will already be exporting multiple files, why not separate especially large files into parts? Since we are dealing with scriptural references, we could name the different parts something like: "Gospel Library Study Notes (1 Nephi - 3 Nephi)."
