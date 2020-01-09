import requests
import json
from apps.data_collectors.collectors import BaseServiceConnector
import logging
log = logging.getLogger('django.parsers')


class BaseAPIManager(BaseServiceConnector):
    '''
    Базовый класс, который нужно использовать для каждого добавляемого API-менеджера
    '''
    @property
    def root(self, value):
        '''
        root - это список строк, каждая из которых является корнем API
        (используется именно список, т.к. тот же BetFair для
         взаимодействия со своей БД предоставляет несколько API:
         один для ставок, другой - для аккаунта.
        :param value:
        :return:
        '''
        if type(value) not in [str, list]:
            raise AttributeError('The root is required attribute')
        elif isinstance(value, str):
            value = list(value)
        return value

    session = requests.Session()

    def _make_request(self, method_type, relative_url, root_index=0, data=None):
        '''
        По сути, в этом методе мы просто выполняем стандартный requests.post или requests.get, но с некоторыми нюансами:
        :param method_type: тип запрос. get для GET-запросов, post - для POST
        :param relative_url: относительная ссылка метода. То есть если это полный адрес запроса:
        https://api.betfair.com/exchange/betting/rest/v1.0/listEventTypes/
        А это - корень:
        https://api.betfair.com/exchange/betting/rest/v1.0/
        То относительной ссылкой будет считаться listEventTypes/
        :param root_index: атрибут root класса апи-менеджера хранит список со строками, каждая из которых
        является адресом на корень API. root_index - это просто номер нужного корня с отсчетом от 0
        :param data: данные, которые нужно передать в запросе

        :return:
        '''
        url = self.root[root_index] + relative_url
        data = json.dumps(data)
        if method_type == 'get':
            response = self.session.get(url, params=data)
        elif method_type == 'post':
            response = self.session.post(url, data=data)
        else:
            raise AttributeError('Unacceptable method type')
        return response
