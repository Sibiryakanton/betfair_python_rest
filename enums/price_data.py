from enum import Enum


class PriceData(Enum):
    # Amount available for the BSP auction.
    SP_AVAILABLE = 'SP_AVAILABLE'

    # Amount traded in the BSP auction.
    SP_TRADED = 'SP_TRADED'

    # Amount traded on the exchange.
    EX_TRADED = 'EX_TRADED'

    # EX_ALL_OFFERS trumps EX_BEST_OFFERS if both settings are present
    EX_ALL_OFFERS = 'EX_ALL_OFFERS'

    # Only the best prices available for each runner, to requested price depth.
    EX_BEST_OFFERS = 'EX_BEST_OFFERS'
