from enum import Enum


class MarketSort(Enum):
    # Minimum traded volume
    MINIMUM_TRADED = 'MINIMUM_TRADED'

    # Maximum traded volume
    MAXIMUM_TRADED = 'MAXIMUM_TRADED'

    # Minimum available to match
    MINIMUM_AVAILABLE = 'MINIMUM_AVAILABLE'

    # Maximum available to match
    MAXIMUM_AVAILABLE = 'MAXIMUM_AVAILABLE'

    # The closest markets based on their expected start time
    FIRST_TO_START = 'FIRST_TO_START'

    # The most distant markets based on their expected start time
    LAST_TO_START = 'LAST_TO_START'
