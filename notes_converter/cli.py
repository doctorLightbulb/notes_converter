"""A module containing all CLI elements and functions for `notes_converter`."""

import argparse
from pathlib import Path


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
        help="Input file names",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="The path to the target file.",
    )
    return parser.parse_args()


class Cli:
    """Initialize a simple command-line interface for program
    execution."""

    def __init__(self, args, converter) -> None:
        self.args = args
        self.converter = converter

    def run(self):
        notes_input_path = [Path(i) for i in self.args.input]
        output_path = Path(self.args.output)

        self.converter.input_path = notes_input_path
        self.converter.output_path = output_path

        status = self.converter.convert()
        print(status)
