# README

Welcome to `notes_converter`, a simple script that converts your exported `.csv` notes from the website version of the Gospel Library of the Church of Jesus Christ of Latter-day Saints into an orderly Word document.

## What it does

* ✅ Converts one or more `.csv` files into at least one MS Word document.
* ✅ Temporarily stores all notes in a SQLite3 database during conversion (coming soon).

## What it does not do

* ❌ Allows the user to manually organize the notes.
* ❌ Permanently stores all notes for future retrieval.
* ❌ Imports `.txt` files.
* ❌ Imports handwritten notes.

## Usage examples

### The graphical user interface (GUI)

Provide usage examples.

### The command-line interface (CLI)

To give the application a meaningful way to be harnessed by an automation script, a command-line interface has been provided.

## Creating a custom template

Any Word document can be used as a template. For the sake of order, however, I would recommend creating a special Word file solely for use as a template in a folder with other templates.

What the template contains is purely for your convenience to help in its design. It will not appear in the output file.

> **NOTE**
>
> Be sure to close the template Word document *before* executing the application. It cannot use the template if it is open in another application.
