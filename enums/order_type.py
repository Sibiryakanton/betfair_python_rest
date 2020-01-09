from enum import Enum


class OrderType(Enum):
    # A normal exchange limit order for immediate execution
    LIMIT = 'LIMIT'

    # Limit order for the auction (SP)
    LIMIT_ON_CLOSE = 'LIMIT_ON_CLOSE'

    # Market order for the auction (SP)
    MARKET_ON_CLOSE = 'MARKET_ON_CLOSE'
