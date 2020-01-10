import requests
import json
from abc import abstractmethod
import os


class BaseAPIManager:
    '''
    Базовый класс, который нужно использовать для каждого добавляемого API-менеджера
    '''
    session = requests.Session()
    cert_login = 'https://identitysso-cert.betfair.com/api/certlogin'

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

    @property
    def root(self, value):
        '''
        Корень API
        '''
        raise AttributeError('The root is required attribute')

    @property
    @abstractmethod
    def crt_path(self, value):
        '''
        Path to certificate
        '''
        raise AttributeError('The path to certificate is required')

    @property
    @abstractmethod
    def crt_key_path(self, value):
        '''
        Path to certificate key
        '''
        raise AttributeError('The path to certificate is required')

    def print_response(self, response):
        '''
        Not just response.json(), because we need print response with indent
        '''
        if self.log_mode:
            print(json.dumps(json.loads(response.text), indent=4))

    def _make_request(self, relative_url, method_type='post', root_index=0, data=None):
        '''
        In this method we just execute requests.post or requests.get, but with some nuances, written below
        :param method_type: http request type. get for GET-request, post - for POST-requests

        :param relative_url: relative url of method. I.e. if full url looks like that:
        https://api.betfair.com/exchange/betting/rest/v1.0/listEventTypes/
        There is will be root:
        https://api.betfair.com/exchange/betting/rest/v1.0/
        And listEventTypes - relative url

        :param root_index: атрибут root класса апи-менеджера хранит список со строками, каждая из которых
        является адресом на корень API. root_index - это просто номер нужного корня с отсчетом от 0

        :param data: данные, которые нужно передать в запросе

        :return:
        '''
        url = '{}/{}/'.format(self.root, relative_url)
        data = json.dumps(data)
        if method_type == 'get':
            response = self.session.get(url, params=data)
        else:
            response = self.session.post(url, data=data)
        return response
