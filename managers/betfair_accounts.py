import json
from abc import abstractmethod
from .base_api_manager import BaseAPIManager


class BetFairAPIManagerAccounts(BaseAPIManager):
    '''
    The class provides the functional of Betfair Exchange API, described by company on link below:
    https://docs.developer.betfair.com/
    '''
    # TODO Составить полную карту запросов

    root = 'https://api.betfair.com/exchange/account/rest/v1.0'

    def create_developer_app_keys(self):
        # TODO сделать запрос
        pass

    def get_developer_app_keys(self):
        # TODO сделать запрос
        pass

    def get_account_funds(self):
        # TODO сделать запрос

        response = self._make_request('getAccountFunds', data={})
        return response

    def transfer_funds(self):
        # TODO сделать запрос
        pass

    def get_account_details(self):
        # TODO сделать запрос

        response = self._make_request('getAccountDetails', data={})
        self.print_response(response)
        return response

    def get_account_statement(self):
        # TODO сделать запрос
        response = self._make_request('getAccountStatement', data={})
        return response

    def list_currency_rates(self):
        # TODO сделать запрос
        pass
