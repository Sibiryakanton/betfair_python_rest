from .abstract_forms import AbstractMarketFilter, AbstractLocaleField


class MarketFilterAndLocaleForm(AbstractMarketFilter, AbstractLocaleField):
    '''
    Class for combining MarketFilter object and 'locale' field.
    The MarketFilter form used in the Betfair Exchange API
    is quite common and consists of dozens of arguments.
    In this case, it would be a bad idea to copy the arguments
     from method to method along with docstring. Instead of
     copy paste, a separate class was added, in which all the
      attributes of the form will be defined once, then an
      instance of this class will be passed to the input of
      the methods that perform http requests, and there the
      contents of the class will simply be translated into
      a dictionary format and submitted to the request.
    Let's look at an example with the BetFairAPIManager.list_event_types request
    Instead of taking dozens of MarketFilter arguments, the function always
    takes two: market_filter for the BetFairMarketFilter class and locale
    for choosing the response language. So, it should be used like that:
    ___
    market_filter = MarketFilterAndLocaleForm(text_query='Text'. race_types='Chase')
    api_manager = BetFairAPIManagerBetting(login='login', password='password', api_kay='api_key')
    list_event_types_response = api_manager.list_event_types(market_filter=market_filter)
    ___
    Details about params you can find in parent classes
    '''
    @property
    def data(self):
        data = {'filter': {
            'textQuery': self.text_query, 'eventTypeIds': self.event_type_ids,
            'eventIds': self.event_ids, 'competitionIds': self.competitions_ids,
            'marketIds': self.market_ids, 'venues': self.venues, 'bspOnly': self.bsp_only,
            'turnInPlayEnabled': self.in_play_enabled, 'inPlayOnly': self.in_play_only,
            'marketBettingTypes': self.market_betting_types, 'marketCountries': self.market_countries,
            'marketTypeCodes': self.market_type_codes, 'marketStartTime': self.market_start_time,
            'withOrders': self.with_orders, 'raceTypes': self.race_types
        }, 'locale': self.locale}
        return data
