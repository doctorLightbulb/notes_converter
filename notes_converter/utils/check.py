"""A module containing functions and classes for memory and file size
inspection.
"""

from pathlib import Path

import psutil


class SystemMemory:
    """A convenience class enabling cross-platform memory and storage
    checking."""

    def __init__(self) -> None:
        self._memory_info = psutil.virtual_memory()
        self._current_memory = self._memory_info.available
        self._current_storage = self._memory_info.total

    def check_memory(self, megabytes) -> bool:
        """Check the available system memory (RAM) against `megabytes`.

        Parameters
        ----------
        megabytes : An estimated amount of required memory in megabytes.

        Returns
        -------
        A boolean value: `True` or `False`.
        """
        # Convert to megabytes:
        needed_memory = megabytes
        current_memory = self._current_memory / (1024 * 1024)

        return True if needed_memory < current_memory else False

    def check_storage(self, megabytes) -> bool:
        """Check the available system storage (disk space) against
        `megabytes`.

        Parameters
        ----------
        megabytes : An estimated amount of required storage
            in megabytes.

        Returns
        -------
        A boolean value: `True` or `False`.
        """
        # Convert to megabytes:
        needed_storage = megabytes
        current_storage = self._current_storage / (1024 * 1024)
        return True if needed_storage < current_storage else False


def check_file_size(paths):
    """Tally the size of all provided files, in bytes, and
    return the sum in megabytes."""
    return sum([Path(path).stat().st_size / (1024 * 1024) for path in paths])
