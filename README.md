[![Github All Releases](https://img.shields.io/github/downloads/doctorLightbulb/notes_converter/total.svg)]()

# README

Welcome to `notes_converter`, a simple script that converts your exported `.csv` notes from [Gospel Library Online](https://www.churchofjesuschrist.org/study?lang=eng&platform=web) of the Church of Jesus Christ of Latter-day Saints into an orderly Word document.

## What it does

* ✅ Converts one or more `.csv` files into at least one MS Word document.
* ✅ Temporarily stores all notes in a SQLite3 database during conversion (coming soon).

## What it does not do

* ❌ Allows the user to manually organize the notes.
* ❌ Permanently stores all notes for future retrieval.
* ❌ Imports `.txt` files.
* ❌ Imports handwritten notes.

> ⚠️ **Note**
>
> This project is currently under development and available only as source code. In time, however, it will be released in a more user-friendly form.

## Usage examples

### The graphical user interface (GUI)

Provide usage examples.

### The command-line interface (CLI)

To give the application a meaningful way to be harnessed by an automation script, a command-line interface has been provided.

## Creating a custom template

Any Word document can be used as a template. For the sake of order, however, I would recommend creating a special Word file solely for use as a template in a folder with other templates.

What the template contains is purely for your convenience to help in its design. It will not appear in the output file.

Add two paragraph styles with the following names:

* **Head** (used for the first paragraph)
* **Link** (used for hyperlinks)

Eventually, existing styles in a Word document will be used for increased flexibility.

> **NOTE**
>
> If you are on a Windows machine, be sure to close the template Word document *before* executing the application. It cannot use the template if it is open in another application.
