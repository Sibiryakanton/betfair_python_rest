from enum import Enum


class SortDir(Enum):
    # Order from earliest value to latest e.g. lowest betId is first in the results.
    EARLIEST_TO_LATEST = 'EARLIEST_TO_LATEST'

    # Order from the latest value to the earliest e.g. highest betId is first in the results.
    LATEST_TO_EARLIEST = 'LATEST_TO_EARLIEST'
