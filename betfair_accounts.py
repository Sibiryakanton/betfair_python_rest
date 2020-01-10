import json
from abc import abstractmethod
from .base_api_manager import BaseAPIManager


class BetFairAPIManagerBetting(BaseAPIManager):
    '''
    The class provides the functional of Betfair Exchange API, described by company on link below:
    https://docs.developer.betfair.com/
    '''
    # TODO Составить полную карту запросов

    root = 'https://api.betfair.com/exchange/account/rest/v1.0'

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
        Not just response.json(), because we need indents
        '''
        if self.log_mode:
            print(json.dumps(json.loads(response.text), indent=4))
