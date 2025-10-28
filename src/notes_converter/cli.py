"""
A module containing all CLI elements and functions for `notes_converter`.

Classes
-------
- Cli()

Functions
---------
- parse_args()
"""

import argparse
from pathlib import Path

from notes_converter.converter import NotesConverter

# TODO:
# Transition from argsparse to click.


def parse_args():
    """Parse command line inputs."""

    parser = argparse.ArgumentParser(
        description="A Tkinter application with command-line arguments.",
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        action="append",
        help="Input file names.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="The path to the target file.",
    )
    parser.add_argument(
        "-t",
        "--template",
        type=str,
        help="The path to a custom template.",
    )
    return parser.parse_args()


class Cli:
    """
    A simple command-line interface for program execution.

    Attributes
    ----------
    args : argsparse.Namespace
        An `argsparse` namespace object.
    converter : NotesConverter
        The `NotesConverter` class.

    Methods
    -------
    run():
        Convert with the provided arguments.
    """

    def __init__(self, args: argparse.Namespace, converter: NotesConverter) -> None:
        self.args = args
        self.converter = converter

    def run(self):
        """Read all inputs and assign them to `self.converter`."""
        input_path = [Path(i) for i in self.args.input]
        output_path = Path(self.args.output)

        # Required values:
        self.converter.input_paths = input_path
        self.converter.output_path = output_path

        # Optional values:
        if self.args.template:
            self.converter.template_path = Path(self.args.template)

        status = self.converter.convert()
        print(status)
