import requests
import json
from abc import abstractmethod
import os


class BaseAPIManager:
    '''
    Base class for each adding api manager
    '''
    session = requests.Session()
    cert_login = 'https://identitysso-cert.betfair.{}/api/certlogin'

    def __init__(self, login, password, api_key, log_mode=False, session_token=None, domain_area='com'):
        '''
        :param login:
        :param password:
        :param api_key:
        :param log_mode: Set True, if you need print all responses of requests
        :param session_token:
        :param domain_area: string for domain area
        (possible values: com, es (for Spanish Exchange) and it (for Italian Exchange))
        '''
        self.log_mode = log_mode
        self.session_token = session_token
        self.domain_area = domain_area
        cert_auth_link = self.cert_login.format(domain_area)
        if session_token is None:
            cert_login_command = 'curl -q -k --cert /{} --key /{} {} -d "username={}&password={}" ' \
                                 '-H "X-Application: {}"'.format(self.crt_path, self.crt_key_path, cert_auth_link,
                                                                 login, password, api_key)
            response = os.popen(cert_login_command).read()
            json_response = json.loads(response)
            self.session_token = json_response['sessionToken']
        self.session.headers = {'X-Application': api_key, 'X-Authentication': self.session_token,
                                'Content-Type': 'application/json', 'Accept': 'application/json'}

    @property
    def root(self, value):
        '''
        API root
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

    def _make_request(self, relative_url, method_type='post', data=None):
        '''
        In this method we just execute requests.post or requests.get, but with some nuances, written below
        :param method_type: http request type. get for GET-request, post - for POST-requests

        :param relative_url: relative url of method. I.e. if full url looks like that:
        https://api.betfair.com/exchange/betting/rest/v1.0/listEventTypes/
        There is will be root:
        https://api.betfair.com/exchange/betting/rest/v1.0/
        And listEventTypes - relative url

        :param data: data, which need to send with request
        :return:
        '''
        root = self.root.format(self.domain_area)
        url = '{}/{}/'.format(root, relative_url)
        from datetime import datetime, timedelta
        today = datetime.now().date()

        data = {'betStatus': 'SETTLED',
                'settledDateRange': {'from': str(today-timedelta(days=1000)),
                                     'to': str(today+timedelta(days=7))}
                }
        data = json.dumps(data)
        print(data)
        if method_type == 'get':
            response = self.session.get(url, params=data)
        else:
            response = self.session.post(url, data=data)
        return response
