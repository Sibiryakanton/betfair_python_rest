from enum import Enum


class MarketProjection(Enum):
    # If not selected then the competition will not be returned with marketCatalogue
    COMPETITION = 'COMPETITION'

    # If not selected then the event will not be returned with marketCatalogue
    EVENT = 'EVENT'

    # If not selected then the event type will not be returned with marketCatalogue
    EVENT_TYPE = 'EVENT_TYPE'

    # If not selected then the start time will not be returned with marketCatalogue
    MARKET_START_TIME = 'MARKET_START_TIME'

    # If not selected then the description will not be returned with marketCatalogue
    MARKET_DESCRIPTION = 'MARKET_DESCRIPTION'

    # If not selected then the runners will not be returned with marketCatalogue
    RUNNER_DESCRIPTION = 'RUNNER_DESCRIPTION'

    # If not selected then the runner metadata will not be returned with marketCatalogue.
    # If selected then RUNNER_DESCRIPTION will also be returned regardless
    # of whether it is included as a market projection.
    RUNNER_METADATA = 'RUNNER_METADATA'
