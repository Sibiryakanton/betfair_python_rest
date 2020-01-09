import json
import os
from datetime import timedelta, datetime
from .base_api_manager import BaseAPIManager
import logging
from abc import abstractmethod
log = logging.getLogger('django.parsers')


class BetfairMarketFilter:
    '''
    The MarketFilter form used in the Betfair Exchange API
    is quite common and consists of dozens of arguments.
    In this case, it would be a bad idea to copy the arguments
     from method to method along with dockstring. Instead of
     copy paste, a separate class was added, in which all the
      attributes of the form will be defined once, then an
      instance of this class will be passed to the input of
      the methods that perform http requests, and there the
      contents of the class will simply be translated into
      a dictionary format and submitted to the request.
    Let's look at an example with the BetFairAPIManager.list_event_types request
    Instead of taking dozens of MarketFilter arguments, the function always
    takes two: market_filter for the BetFairMarketFilter class and locale
    for choosing the response language. So, it would be used like that:
    ___
    market_filter = BetfairMarketFilter(text_query='Text'. 'race_types'='Chase')
    api_manager = BetFairAPIManager(login='login', password='password', api_kay='api_key')
    list_event_types_response = api_manager.list_event_types(market_filter=market_filter, locale='ru')
    ___
    '''
    def __init__(self, text_query=None, event_type_ids=None, event_ids=None,
                 competitions_ids=None, market_ids=None, venues=None,
                 bsp_only=None, in_play_enabled=None, in_play_only=None,
                 market_betting_types=None, market_countries=None,
                 market_type_codes=None, market_start_time=None,
                 with_orders=None, race_types=None):
        '''
        :param text_query: Restrict markets by any text associated
        with the market such as the Name, Event, Competition, etc.
        You can include a wildcard (*) character as long as
         it is not the first character.

        :param event_type_ids: Restrict markets by event type associated
        with the market. (i.e., Football, Hockey, etc)

        :param event_ids: Restrict markets by the event id associated
         with the market.

        :param competitions_ids: Restrict markets by the competitions
        associated with the market.

        :param market_ids: Restrict markets by the market id associated
        with the market.

        :param venues: Restrict markets by the venue associated
        with the market. Currently only Horse Racing markets have venues.

        :param bsp_only: Restrict to bsp markets only, if True or
        non-bsp markets if False. If not specified then returns both
        BSP and non-BSP markets

        :param in_play_enabled: Restrict to markets that will turn in play
        if True or will not turn in play if false. If not specified, returns both.

        :param in_play_only: Restrict to markets that are currently
        in play if True or are not currently in play if
        false. If not specified, returns both.

        :param market_betting_types: Restrict to markets that match
        the betting type of the market
         (i.e. Odds, Asian Handicap Singles, Asian Handicap Doubles or Line)

        :param market_countries: Restrict to markets that are
        in the specified country or countries

        :param market_type_codes: Restrict to markets that match the type of
        the market (i.e., MATCH_ODDS, HALF_TIME_SCORE). You should
        use this instead of relying on the market name as the market
        type codes are the same in all locales. Please note: All marketTypes
        are available via the listMarketTypes operations.

        :param market_start_time: Restrict to markets with a
        market start time before or after the specified date

        :param with_orders: Restrict to markets that I have
        one or more orders in these status.

        :param race_types: 	Restrict by race type (i.e. Hurdle, Flat, Bumper, Harness, Chase)
        '''
        self.data = {
            'textQuery': text_query, 'eventTypeIds': event_type_ids,
            'eventIds': event_ids, 'competitionIds': competitions_ids,
            'marketIds': market_ids, 'venues': venues, 'bspOnly': bsp_only,
            'turnInPlayEnabled': in_play_enabled, 'inPlayOnly': in_play_only,
            'marketBettingTypes': market_betting_types, 'marketCountries': market_countries,
            'marketTypeCodes': market_type_codes, 'marketStartTime': market_start_time,
            'withOrders': with_orders, 'raceTypes': race_types
        }
