"""
A module containing functions and classes for memory and file size inspection.

Classes
-------
- SystemMemory()

Functions
---------
- check_file_size()
- check_required_memory()
"""

from pathlib import Path
from typing import List

import psutil


class SystemMemory:
    """
    Represents the system memory.

    Methods
    -------
    check_memory():
        Checks available system memory (RAM) against needed memory.
    check_storage():

    """

    def __init__(self) -> None:
        self._memory_info = psutil.virtual_memory()
        self._current_memory = self._memory_info.available
        self._current_storage = self._memory_info.total

    def check_memory(self, megabytes: float) -> bool:
        """Checks the available system memory (RAM) against `megabytes`.

        Parameters
        ----------
        megabytes : float
            An estimated amount of required memory in megabytes.

        Returns
        -------
        bool
            Either `True` or `False`.
        """
        # Convert to megabytes:
        needed_memory = megabytes
        current_memory = self._current_memory / (1024 * 1024)

        return True if needed_memory < current_memory else False

    def check_storage(self, megabytes: float) -> bool:
        """
        Checks the available system storage (disk space) against `megabytes`.

        Parameters
        ----------
        megabytes : int
            An estimated amount of required storage in megabytes.

        Returns
        -------
        bool
            Either `True` or `False`.
        """
        # Convert to megabytes:
        needed_storage = megabytes
        current_storage = self._current_storage / (1024 * 1024)
        return True if needed_storage < current_storage else False


def check_file_size(paths: List[Path]) -> float:
    """
    Tallies file sizes in bytes and returns the sum in megabytes.

    Parameters
    ----------
    paths : List[Path]
        A list of file paths.

    Returns
    -------
    float
        The total size of all files supplied in `paths`.
    """
    return sum([Path(path).stat().st_size / (1024 * 1024) for path in paths])


def check_required_memory(
    file_paths: List[Path], smu: SystemMemory, overhead: float = 10
) -> bool:
    """
    Checks available memory against required memory for the task.

    Parameters
    ----------
    file_paths : List[Path]
        Contains one or more paths as `str`.
    smu : SystemMemory
        The SystemMemory class for the memory check.
    overhead : float
        The estimated memory Notes Converter requires to run.

    Returns
    -------
    bool
        Either `True` or `False`.
    """
    # Estimated memory needed to run the program
    overhead_memory = overhead  # in megabytes

    # Estimated memory needed to convert the input file(s)
    conversion_memory = check_file_size(file_paths)  # in megabytes
    total_memory_needed = overhead_memory + conversion_memory

    return smu.check_memory(megabytes=total_memory_needed)
