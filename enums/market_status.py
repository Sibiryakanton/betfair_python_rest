from enum import Enum


class MarketStatus(Enum):
    # The market has been created but isn't yet available.
    INACTIVE = 'INACTIVE'

    # The market is open for betting.
    OPEN = 'OPEN'

    # The market is suspended and not available for betting.
    SUSPENDED = 'SUSPENDED'

    # The market has been settled and is no longer available for betting.
    CLOSED = 'CLOSED'
