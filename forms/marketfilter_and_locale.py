from .abstract_forms import AbstractMarketFilter, AbstractLocaleField


class MarketFilterAndLocaleForm(AbstractMarketFilter, AbstractLocaleField):

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
