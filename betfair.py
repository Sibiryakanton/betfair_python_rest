import json
import os
from datetime import timedelta, datetime
import logging
from abc import abstractmethod

from .base_api_manager import BaseAPIManager
from .market_filter import BetfairMarketFilter

log = logging.getLogger('django.parsers')


class BetFairAPIManager(BaseAPIManager):
    '''
    The class realize the functional of Betfair Exchange API, described by company on link below:
    https://docs.developer.betfair.com/
    '''
    # TODO Составить полную карту запросов

    cert_login = 'https://identitysso-cert.betfair.com/api/certlogin'

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

    root = ['https://api.betfair.com/exchange/betting/rest/v1.0/',
            'https://api.betfair.com/exchange/account/rest/v1.0/']

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
        data = {'filter': market_filter.data, 'locale': locale}
        response = self._make_request('post', 'listEventTypes/', data=data)
        self.print_response(response)
        return response.json()

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
        data = {'filter': market_filter.data, 'locale': locale}
        response = self._make_request('post', 'listCompetitions/', data=data)
        self.print_response(response)
        return response.json()

    def list_time_ranges(self, market_filter, granularity):
        '''
        :param market_filter: The filter class to select desired markets. All markets that match the
        criteria in the filter are selected.

        :param granularity: The granularity of time periods that correspond
         to markets selected by the market filter. (possible values: HOURS<

        '''
        data = {'filter': market_filter.data, 'granularity': locale}
        response = self._make_request('post', 'listCountries/', data=data)
        self.print_response(response)
        return response.json()
    def list_countries(self, market_filter, locale=None):
        # TODO протестировать
        '''
        Returns a list of Countries associated with the markets selected by the MarketFilter.
        :param market_filter: The filter class to select desired markets. All markets that match the
        criteria in the filter are selected.

        :param locale: The language used for the response. If not specified, the default is returned.
        :return:
        '''
        data = {'filter': market_filter.data, 'locale': locale}
        response = self._make_request('post', 'listCountries/', data=data)
        self.print_response(response)
        return response.json()

    def list_events(self, text_query=None, competition_ids=None, turn_in_play_enabled=True, event_ids=None):
        '''
        Получить список событий (матчей)
        :param text_query:
        :param competition_ids:
        :param turn_in_play_enabled: True, если надо выцепить только грядущие матчи
        :param event_ids:
        :return:
        '''
        data = {'filter': {'competitionIds': competition_ids, 'turnInPlayEnabled': turn_in_play_enabled,
                           'textQuery': text_query, 'eventIds': event_ids}}
        response = self._make_request('post', 'listEvents/', data=data)
        self.print_response(response)
        return response.json()

    def list_market_types(self, text_query=None, event_ids=None):
        '''
        Вернуть список типов ставок (OVER_UNDER_45, HALF_TIME_FULL_TIME, DRAW_NO_BETб CORRECT_SCORE). типы присылаются
        без вложенных опций: к примеру, ставка CORRECT_SCORE подразумевает список возможных счетов матча, но здесь
        вместо этого будет только такое: {"marketCount": 1, "marketType": "CORRECT_SCORE"}
        :param text_query:
        :param event_ids:
        :return:
        '''
        data = {'filter': {'textQuery': text_query, 'eventIds': event_ids}}
        response = self._make_request('post', 'listMarketTypes/', data=data)
        self.print_response(response)
        return response.json()

    def list_market_catalogue(self, text_query=None, event_ids=None):
        '''
        Вернуть список типов ставок (OVER_UNDER_45, HALF_TIME_FULL_TIME, DRAW_NO_BETб CORRECT_SCORE). типы присылаются
        без вложенных опций: к примеру, ставка CORRECT_SCORE подразумевает список возможных счетов матча, но здесь
        вместо этого будет только такое: {"marketCount": 1, "marketType": "CORRECT_SCORE"}
        :param text_query:
        :param event_ids:
        :return: список объектов предложений в маркете в контексте конкретных матчей со списком селекторов (runners)
        '''
        data = {'filter': {'textQuery': text_query, 'eventIds': event_ids, 'eventTypeIds': ['1']}, 'maxResults': 900,
                'marketProjection': ['RUNNER_DESCRIPTION']}
        response = self._make_request('post', 'listMarketCatalogue/', data=data)
        self.print_response(response)
        return response.json()

    def list_market_book(self, market_ids):
        '''
        '''
        data = {'marketIds': market_ids, 'priceProjection': {'priceData': ['EX_BEST_OFFERS']},
                'matchProjection': 'ROLLED_UP_BY_AVG_PRICE'}
        response = self._make_request('post', 'listMarketBook/', data=data)
        self.print_response(response)
        return response.json()

    def list_runners(self, market_id, selection_id):
        '''
        Вернуть детальную информацию о конкретной опции ставки (к примеру, есть
        :param selection_id: id опции выбора
        :param market_id: id маркета (типа ставки)
        :return: список объектов предложений в маркете в контексте конкретных матчей со списком селекторов (runners)
        '''
        data = {'marketId': market_id, 'selectionId': selection_id,
                'priceProjection': {'priceData': ['EX_BEST_OFFERS']}}
        response = self._make_request('post', 'listRunnerBook/', data=data)
        self.print_response(response)
        return response.json()

    def list_current_orders(self):
        '''
        Получить список заказов по еще не начавшимся матчам
        :return:
        '''
        data = {}
        response = self._make_request('post', 'listCurrentOrders/', data=data)
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
        response = self._make_request('post', 'listClearedOrders/', data=data)
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
        response = self._make_request('post', 'placeOrders/', data=data)
        self.print_response(response)
        return response

    # Accounts API
    def get_account_details(self):
        response = self._make_request('post', 'getAccountDetails/', 1, data={})
        self.print_response(response)
        return response

    def get_account_funds(self):
        response = self._make_request('post', 'getAccountFunds/', 1, data={})
        return response

    def get_account_statement(self):
        response = self._make_request('post', 'getAccountStatement/', 1, data={})
        return response

    def print_response(self, response):
        '''
        Not just response.json(), because we need print response with indent
        '''
        if self.log_mode:
            print(json.dumps(json.loads(response.text), indent=4))
