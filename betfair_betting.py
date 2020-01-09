import json
import os
import requests
from datetime import timedelta, datetime
import logging
from abc import abstractmethod
from .base_api_manager import BaseAPIManager

log = logging.getLogger('django.parsers')


class BetFairAPIManager(BaseAPIManager):
    '''
    The class provides the functional of Betfair Exchange API, described by company on link below:
    https://docs.developer.betfair.com/
    '''
    # TODO Составить полную карту запросов

    cert_login = 'https://identitysso-cert.betfair.com/api/certlogin'
    session = requests.Session()
    root = 'https://api.betfair.com/exchange/betting/rest/v1.0'

    @abstractmethod
    @property
    def crt_path(self, value):
        '''
        Path to certificate
        '''
        raise AttributeError('The path to certificate is required')

    @abstractmethod
    @property
    def crt_key_path(self, value):
        '''
        Path to certificate key
        '''
        raise AttributeError('The path to certificate is required')

    def __init__(self, login, password, api_key, log_mode=False, session_token=None):
        # TODO протестировать авторизацию

        self.log_mode = log_mode
        self.session_token = session_token

        if session_token is None:
            cert_login_command = 'curl -q -k --cert /{} --key /{} {} -d "username={}&password={}" ' \
                                 '-H "X-Application: {}"'.format(self.crt_path, self.crt_key_path, self.cert_login,
                                                                 login, password, api_key)
            response = os.popen(cert_login_command).read()
            json_response = json.loads(response)
            self.session_token = json_response['sessionToken']
        self.session.headers = {'X-Application': api_key, 'X-Authentication': self.session_token,
                                'Content-Type': 'application/json', 'Accept': 'application/json'}

    def list_event_types(self, market_filter, locale=None):
        # TODO протестировать

        '''
        Returns a list of Event Types (i.e. Sports) associated with the markets selected by the MarketFilter.
        Get list of event types (for example, Soccer, Basketball and etc)
        :param market_filter: The filter class to select desired markets. All markets that match the
        criteria in the filter are selected.
        :param locale: The language used for the response. If not specified, the default is returned.

        '''
        return self.__request_with_market_filter('listEventTypes', market_filter, locale=locale)

    def list_competitions(self, market_filter, locale=None):
        # TODO протестировать
        '''
        Returns a list of Competitions (i.e., World Cup 2013, Bundesliga) associated with
        the markets selected by the MarketFilter.
        Currently only Football markets have an associated competition.

        :param market_filter: The filter class to select desired markets. All markets that match the
        criteria in the filter are selected.

        :param locale: The language used for the response. If not specified, the default is returned.
        '''
        return self.__request_with_market_filter('listCompetitions', market_filter, locale=locale)

    def list_time_ranges(self, market_filter, granularity):
        # TODO протестировать
        '''
        :param market_filter: The filter class to select desired markets. All markets that match the
        criteria in the filter are selected.

        :param granularity: The granularity of time periods that correspond
         to markets selected by the market filter. (possible values: DAYS, HOURS, MINUTES

        '''

        data = {'filter': market_filter.data, 'granularity': granularity}
        response = self._make_request('listTimeRanges', data=data)
        self.print_response(response)
        return response.json()

    def list_events(self, market_filter, locale=None):
        '''
        Returns a list of Events (i.e, Reading vs. Man United)
        associated with the markets selected by the MarketFilter.

        :param market_filter: The filter class to select desired
        markets. All markets that match the
        criteria in the filter are selected.

        :param locale: The language used for the response.
         If not specified, the default is returned.
        :return:
        '''
        return self.__request_with_market_filter('listEvents', market_filter, locale=locale)

    def list_market_types(self, market_filter, locale=None):
        '''
        Returns a list of market types (i.e. MATCH_ODDS, NEXT_GOAL)
        associated with the markets selected by the MarketFilter.
        The market types are always the same, regardless of locale.

        :param market_filter: The filter class to select desired
        markets. All markets that match the
        criteria in the filter are selected.

        :param locale: The language used for the response.
         If not specified, the default is returned.
        :return:
        :return:
        '''
        return self.__request_with_market_filter('listMarketTypes', market_filter, locale=locale)

    def list_countries(self, market_filter, locale=None):
        # TODO протестировать
        '''
        Returns a list of Countries associated with the markets selected by the MarketFilter.
        :param market_filter: The filter class to select desired markets. All markets that match the
        criteria in the filter are selected.

        :param locale: The language used for the response. If not specified, the default is returned.
        :return:
        '''
        return self.__request_with_market_filter('listCountries', market_filter, locale=locale)

    def list_venues(self, market_filter, locale=None):
        # TODO протестировать
        '''
        Returns a list of Venues (i.e. Cheltenham, Ascot) associated
        with the markets selected by the MarketFilter. Currently,
        only Horse Racing markets are associated with a Venue.

        :param market_filter: The filter class to select desired markets. All markets that match the
        criteria in the filter are selected.

        :param locale: The language used for the response. If not specified, the default is returned.
        :return:
        '''
        return self.__request_with_market_filter('listVenues', market_filter, locale=locale)

    def list_market_catalogue(self, market_filter, market_projection, max_results, sort=None, locale=None):
        # TODO Протестировать
        '''
        Returns a list of information about published (ACTIVE/SUSPENDED)
         markets that does not change (or changes very rarely). You use
         listMarketCatalogue to retrieve the name of the market, the names
          of selections and other information about markets.  Market Data
          Request Limits apply to requests made to listMarketCatalogue.

        :param market_filter: The filter class to select desired markets. All markets that match the
        criteria in the filter are selected.

        :param market_projection: The type and amount of data returned about the market.

        :param max_results: limit on the total number of results
        returned, must be greater than 0 and less than or equal to 1000

        :param sort: The order of the results. Will default to
        RANK if not passed. RANK is an assigned priority that is
        determined by our Market Operations team in our back-end system.
        A result's overall rank is derived from the ranking given to
         the flowing attributes for the result. EventType, Competition,
          StartTime, MarketType, MarketId. For example, EventType
           is ranked by the most popular sports types and marketTypes
           are ranked in the following order: ODDS ASIAN LINE RANGE If
            all other dimensions of the result are equal, then the
            results are ranked in MarketId order.

        :param locale: The language used for the response. If not specified, the default is returned.
        '''
        data = {
            'filter': market_filter.data, 'marketProjection': market_projection,
            'maxResults': max_results, 'sort': sort, 'locale': locale}
        response = self._make_request('listMarketCatalogue', data=data)
        self.print_response(response)
        return response.json()

    def list_market_book(self, market_ids, book_form=None):
        # TODO Протестировать
        '''
        Returns a list of dynamic data about markets.
        Dynamic data includes prices, the status of the market,
         the status of selections, the traded volume, and
         the status of any orders you have placed in the market.

        :param market_ids: One or more market ids. The number of markets
        returned depends on the amount of data you request via
        the price projection.
        :param book_form: The BetFairBookForm object
        '''
        data = {'marketIds': market_ids}
        data.update(book_form.data)

        response = self._make_request('listMarketBook', data=data)
        self.print_response(response)
        return response.json()

    def list_runner_book(self, market_id, selection_id, handicap=None, book_form=None):
        '''
        Returns a list of dynamic data about a market and a specified runner.
         Dynamic data includes prices, the status of the market, the status
         of selections, the traded volume, and the status of any orders you have placed in the market..
        :param selection_id: The unique id for the selection in the market.
        :param market_id: The unique id for the market.
        :param handicap: The projection of price data you want to receive in the response.
        :param book_form: The BetFairBookForm object
        '''
        data = {'marketId': market_id, 'selectionId': selection_id,
                'handicap': handicap}
        data.update(book_form.data)

        response = self._make_request('listRunnerBook', data=data)
        self.print_response(response)
        return response.json()

    # TODO listMarketProfitAndLoss

    def list_current_orders(self):
        '''
        Получить список заказов по еще не начавшимся матчам
        :return:
        '''
        data = {}
        response = self._make_request('listCurrentOrders', data=data)
        self.print_response(response)
        return response

    def list_cleared_orders(self):
        '''
        Запросить список уже проставленых ставок
        :return:
        '''
        today = datetime.today()
        data = {'betStatus': 'SETTLED',
                'settledDateRange': {'from': str(today-timedelta(days=1000)),
                                     'to': str(today+timedelta(days=7))}
                }
        response = self._make_request('listClearedOrders', data=data)
        self.print_response(response)
        return response

    def place_order(self, market_id, selection_id, last_back_price, bet_amount):
        '''
        :param market_id:
        :param selection_id:
        :param last_back_price: last info about runner odd
        :param bet_amount: the amount of money for bet
        :return:
        '''
        min_price = round(float(last_back_price), 2)

        data = {'marketId': market_id,
                'instructions': [
                    {'orderType': 'LIMIT',
                     'handicap': "0",
                     "limitOrder": {"size": bet_amount, "price": min_price,
                                    "persistenceType": "LAPSE"},
                     'selectionId': selection_id,
                     'side': 'BACK',
                     'limitOnCloseOrder': {'liability': 3, 'price': min_price}
                     }
                ],
                }
        response = self._make_request('placeOrders', data=data)
        self.print_response(response)
        return response

    # TODO cancelOrders
    # TODO replaceOrders
    # TODO updateOrder
    #
    # Accounts API
    def get_account_details(self):
        response = self._make_request('getAccountDetails', root_index=1, data={})
        self.print_response(response)
        return response

    def get_account_funds(self):
        response = self._make_request('getAccountFunds', root_index=1, data={})
        return response

    def get_account_statement(self):
        response = self._make_request('getAccountStatement', root_index=1, data={})
        return response

    def print_response(self, response):
        '''
        Not just response.json(), because we need print response with indent
        '''
        if self.log_mode:
            print(json.dumps(json.loads(response.text), indent=4))

    def __request_with_market_filter(self, relative_url, market_filter, locale=None, method_type='post'):
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

        :param market_filter: The filter class to select desired markets. All markets that match the
        criteria in the filter are selected.

        :param locale: The language used for the response. If not specified, the default is returned.
        :return:
        '''
        data = {'filter': market_filter.data, 'locale': locale}
        response = self._make_request(relative_url, data=data, method_type=method_type)
        self.print_response(response)
        return response.json()
