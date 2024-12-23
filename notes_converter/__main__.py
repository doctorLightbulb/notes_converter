"""`Notes Converter`

Convert a `.csv` file to a styled `.docx` file.
"""

from cli import Cli, parse_args
from gui import MainWindow

from notes_converter import NotesConverter


def main():

    converter = NotesConverter()

    # Command-line mode
    args = parse_args()
    if args.input:
        cli = Cli(args, converter)
        cli.run()
    else:
        # GUI mode
        window = MainWindow(converter)
        window.mainloop()


if __name__ == "__main__":
    main()
