"""A module containing all custom decorators for this project."""

import functools


def report_error(func):
    @functools.wraps(func)
    def wrapper_report_error(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TypeError as e:
            print(f"TypeError: {e}")
            for item in args[0]:
                try:
                    func([item])
                except TypeError:
                    print(f"Problematic item: {item.title}")
                    with open(
                        "Problematic_items_titles.txt", "a", encoding="utf-8"
                    ) as f:
                        f.write(item.title + "\n")
            raise

    return wrapper_report_error


def remove_duplicates(func):
    """Remove duplicate notes."""

    # TODO: Add more tailored duplicate removal.
    # For example, if a note is the same but the tags or notebooks are
    # different. In these cases, the note most recently updated should
    # be kept and the other discarded.

    @functools.wraps(func)
    def wrapper_remove_duplicates(*args, **kwargs):
        removed_exact_duplicates = []
        for note in func(*args, **kwargs):
            if note not in removed_exact_duplicates:
                removed_exact_duplicates.append(note)
        return removed_exact_duplicates

    return wrapper_remove_duplicates
