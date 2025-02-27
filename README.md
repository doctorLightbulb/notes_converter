# Notes Converter

![Github All Releases](https://img.shields.io/github/downloads/doctorLightbulb/notes_converter/total.svg)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
![Contributors](https://img.shields.io/github/contributors/doctorLightbulb/notes_converter)
[![Clones](https://img.shields.io/badge/clones-unknown-lightgrey?style=flat-square)](https://github.com/doctorLightbulb/notes_converter/graphs/traffic)
[![Open Issues](https://img.shields.io/github/issues/doctorLightbulb/notes_converter)](https://github.com/doctorLightbulb/notes_converter/issues)

Welcome to `notes_converter`, a simple script that converts our exported `.csv` notes from [Gospel Library Online](https://www.churchofjesuschrist.org/study?lang=eng&platform=web) of the Church of Jesus Christ of Latter-day Saints to an orderly Word document.

## What it does

* ✅ Converts one or more `.csv` files into at least one MS Word document.
* ✅ Temporarily stores all notes in a SQLite3 database during conversion (coming soon).

## What it does not do

* ❌ Allows the user to manually organize the notes.
* ❌ Permanently stores all notes for future retrieval.
* ❌ Imports `.txt` files.
* ❌ Imports handwritten notes.

> 🔧 **Note**
>
> This project is currently under development and available only as source code. In time, however, it will be released in a more user-friendly form.

## Usage examples

### The graphical user interface (GUI)

Provide usage examples.

### The command-line interface (CLI)

_To give the application a meaningful way to be harnessed by an automation script, a command-line interface has been provided._

To convert a file, you will need to specify an input (the file to convert) and an output (the name of the Word document and where to save it).

Here is an example:

```powershell
converter -i path/to/notes.csv -o path/to/folder/notes.docx
```

> 🔧 **NOTE**
>
> Currently, the virtual environment must be activated for this example to work.

#### Currently supported commands

| Flag | Action |
| ---- | ------ |
| `--input`   | Used to specify an input file. |
| `-i`   | A shorthand version of `--input`. |
| `--output`   | Used to specify an output file's path, name and file extension. |
| `-o`   | A shorthand version of `--output`. |
| `--template` | Used to specify a Word file to use as a template |
| `-t` | A shorthand version of `--template`. |

## Creating a custom template

Any Word document can be used as a template. For the sake of order, however, I would recommend creating a special Word file solely for use as a template in a folder with other templates.

What the template contains is purely for your convenience to help in its design. It will not appear in the output file.

Add two paragraph styles with the following names:

* **Head** (used for the first paragraph)
* **Link** (used for hyperlinks)

Eventually, existing styles in a Word document will be used for increased flexibility.

> **NOTE**
>
> If you are on a Windows machine, be sure to close the template Word document _before_ executing the application. It cannot use the template if it is open in another application.

## Development: Getting started

To get started, follow these steps:

### Step 1: Clone this repository to your computer

From the repositoriy's main page, click the green `code` button. Here, you can clone (copy) the repository via HTTPS, SSH or GitHub CLI. Additionally, you can open it with GitHub Desktop or download a zip file of the repository.

Optionally, scan the cloned repository with your anti-malware software.

### Step 2: Install dependencies

After placing your copy of the repository in a folder, open the folder in a terminal window and create a virtual environment:

```powershell
python -m venv venv --prompt="notes"
```

Activate the virtual environment. Which command you use will depend on your operating system.

**Windows:**

```powershell
venv\Scripts\activate
```

**Linux:**

```bash
. venv/bin/activate
```

Next, install the dependencies:

```powershell
pip install -e .
```

Alternatively, install the optional development dependencies:

```powershell
pip install -e ".[dev]"
```

Once the dependencies have finished installing, the project is ready for development.
