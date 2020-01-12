import json
import os
import requests
from datetime import timedelta, datetime
import logging
from abc import abstractmethod
from .base_api_manager import BaseAPIManager

log = logging.getLogger('django.parsers')


class BetFairAPIManagerBetting(BaseAPIManager):
    '''
    The class provides the functional of Betfair
    Exchange API, described by company on link below:
    https://docs.developer.betfair.com/
    '''

    root = 'https://api.betfair.{}/exchange/betting/rest/v1.0'

    def list_event_types(self, request_class_object):
        '''
        Returns a list of Event Types (i.e. Sports)
         associated with the markets selected by the MarketFilter.
        Get list of event types (for example, Soccer, Basketball and etc)
        :param request_class_object: The MarketFilterAndLocaleForm object
        '''
        return self.__request_with_dataclass('listEventTypes', request_class_object)

    def list_competitions(self, request_class_object):
        '''
        Returns a list of Competitions
        (i.e., World Cup 2013, Bundesliga) associated with
        the markets selected by the MarketFilter.
        Currently only Football markets have an associated competition.

        :param request_class_object: The MarketFilterAndLocaleForm object

        '''
        return self.__request_with_dataclass('listCompetitions', request_class_object)

    def list_time_ranges(self, request_class_object):
        '''
        Returns a list of time ranges in the granularity
        specified in the request (i.e. 3PM to 4PM, Aug 14th to Aug 15th)
        associated with the markets selected by the MarketFilter.
        :param request_class_object: The MarketFilterAndTimeGranularityForm object

        '''
        return self.__request_with_dataclass('listTimeRanges', request_class_object)

    def list_events(self, request_class_object):
        '''
        Returns a list of Events (i.e, Reading vs. Man United)
        associated with the markets selected by the MarketFilter.

        :param request_class_object: The MarketFilterAndLocaleForm object
        '''
        return self.__request_with_dataclass('listEvents', request_class_object)

    def list_market_types(self, request_class_object):
        '''
        Returns a list of market types (i.e. MATCH_ODDS, NEXT_GOAL)
        associated with the markets selected by the MarketFilter.
        The market types are always the same, regardless of locale.

        :param request_class_object: The MarketFilterAndLocaleForm object

        '''
        return self.__request_with_dataclass('listMarketTypes', request_class_object)

    def list_countries(self, request_class_object):
        '''
        Returns a list of Countries associated with
        the markets selected by the MarketFilter.
        :param request_class_object: The MarketFilterAndLocaleForm object

        '''
        return self.__request_with_dataclass('listCountries', request_class_object)

    def list_venues(self, request_class_object):
        '''
        Returns a list of Venues (i.e. Cheltenham, Ascot) associated
        with the markets selected by the MarketFilter. Currently,
        only Horse Racing markets are associated with a Venue.

        :param request_class_object: The MarketFilterAndLocaleForm object

        '''
        return self.__request_with_dataclass('listVenues', request_class_object)

    def list_market_catalogue(self, request_class_object):
        '''
        Returns a list of information about published (ACTIVE/SUSPENDED)
         markets that does not change (or changes very rarely). You use
         listMarketCatalogue to retrieve the name of the market, the names
          of selections and other information about markets.  Market Data
          Request Limits apply to requests made to listMarketCatalogue.

        :param request_class_object: The ListMarketCatalogueForm object
        '''
        return self.__request_with_dataclass('listMarketCatalogue', request_class_object)

    def list_market_book(self, request_class_object):
        '''
        Returns a list of dynamic data about markets.
        Dynamic data includes prices, the status of the market,
         the status of selections, the traded volume, and
         the status of any orders you have placed in the market.

        :param request_class_object: The ListMarketBookForm object
        '''
        return self.__request_with_dataclass('listMarketBook', request_class_object)

    def list_runner_book(self, request_class_object):
        '''
        Returns a list of dynamic data about a market and a specified runner.
         Dynamic data includes prices, the status of the market, the status
         of selections, the traded volume, and the status of any
         orders you have placed in the market.

        :param request_class_object: The ListRunnerBookForm object

        '''
        return self.__request_with_dataclass('listRunnerBook', request_class_object)

    def list_market_profit_and_loss(self, request_class_object):
        '''
        Retrieve profit and loss for a given list of OPEN markets.
        The values are calculated using matched bets and optionally
        settled bets. Only odds (MarketBettingType = ODDS) markets
        are implemented, markets of other types are silently ignored.
        To retrieve your profit and loss for CLOSED markets, please
        use the listClearedOrders request.

        :param request_class_object: The ListMarketProfitAndLossForm object
        '''
        return self.__request_with_dataclass('listMarketProfitAndLoss', request_class_object)

    def list_current_orders(self, request_class_object):
        '''
        Returns a list of your current orders. Optionally you can
        filter and sort your current orders using the various
         parameters, setting none of the parameters will return
         all of your current orders up to a maximum of 1000 bets,
          ordered BY_BET and sorted EARLIEST_TO_LATEST. To retrieve
           more than 1000 orders, you need to make use of the
           fromRecord and recordCount parameters.

        :param request_class_object: The [] object

        :return:
        '''
        return self.__request_with_dataclass('listCurrentOrders', request_class_object)

    def list_cleared_orders(self, request_class_object):
        '''
        Returns a list of settled bets based on the bet status,
        ordered by settled date. To retrieve more than 1000
        records, you need to make use of the fromRecord and
        recordCount parameters.
        By default the service will  return all
        available data for the last 90 days (see
        Best Practice note below).  The fields available at
        each roll-up are available here
        '''
        return self.__request_with_dataclass('listClearedOrders', request_class_object)

    def place_order(self, request_class_object):
        # TODO Доделать запрос
        '''
        Place new orders into market.
        Please note that additional bet sizing rules
        apply to bets placed into the Italian Exchange.

        In normal circumstances the placeOrders is an atomic operation.
        PLEASE NOTE: if the 'Best Execution' features is switched
        off, placeOrders can return ‘PROCESSED_WITH_ERRORS’
        meaning that some bets can be rejected and other
         placed when submitted in the same PlaceInstruction
        '''
        return self.__request_with_dataclass('placeOrders', request_class_object)

    # TODO cancelOrders
    # TODO replaceOrders
    # TODO updateOrder

    def __request_with_dataclass(self, relative_url, request_object, method_type='post'):
        '''
        Some of the requests have a common request structure,
         which can be easily put into a template function,
         substituting a relative link
        :param method_type: http request type. get for GET-request, post - for POST-requests

        :param relative_url: relative url of method. I.e. if full url looks like that:
        https://api.betfair.com/exchange/betting/rest/v1.0/listEventTypes/
        There is will be root:
        https://api.betfair.com/exchange/betting/rest/v1.0/
        And listEventTypes - relative url

        :param request_object: The form class with all request data. You can view the examples in forms directory
        :return:
        '''
        response = self._make_request(relative_url, data=request_object.data, method_type=method_type)
        self.print_response(response)
        return response.json()
