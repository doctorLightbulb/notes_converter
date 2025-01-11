# Todo

## Changes

* When two or more scriptural references match exactly, the note's heading should be combined upon conversion, with the dates separating the note's body.
* Convert plain open and close quotes and apostophies to their respective fancy versions, thus eliminating inconsistencies in the notes.
* Make the open file and save file dialogs remember the last destinations they visited.
* Add allowance for paragraph ranges (i.e. =p4-p6).
* Need full support for General Conference references.

## Potential Issues

Currently, the program has no error handling for low system memory. Moreover, it would appear that `sorted()` cannot be used successfully with a generator.

The solution to a huge file:

* Load it chunk by chunk into a SQLite3 database.
* Craft a query to sort the data as desired.
* Then return the results one row at a time using a generator function.

To make sorting easier, put each chapter and verse number in its own column.

By the time the input files become too large to process at once, the output file will likely be too large, also. As `notes_converter` will already be exporting multiple files, why not separate especially large files into parts? Since we are dealing with scriptural references, we could name the different parts something like: "Gospel Library Study Notes (1 Nephi - 3 Nephi)."

## Source Link Patterns

The Scriptures and _Come, Follow Me_ have the same pattern:

* Book
* Chapter
* Paragraph

Articles from the _Ensign_, however, follow a slightly different pattern:

* Year
* Month
* Article
* Paragraph
