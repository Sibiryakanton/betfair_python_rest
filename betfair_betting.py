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

    root = 'https://api.betfair.com/exchange/betting/rest/v1.0'

    def list_event_types(self, market_filter, locale=None):
        # TODO протестировать

        '''
        Returns a list of Event Types (i.e. Sports) associated with the markets selected by the MarketFilter.
        Get list of event types (for example, Soccer, Basketball and etc)
        :param market_filter: The filter class to select desired markets. All markets that match the
        criteria in the filter are selected.
        :param locale: string. The language used for the response. If not specified, the default is returned.

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

        :param locale: string. The language used for the response. If not specified, the default is returned.
        '''
        return self.__request_with_market_filter('listCompetitions', market_filter, locale=locale)

    def list_time_ranges(self, market_filter, granularity):
        # TODO протестировать
        '''
        :param market_filter: The filter class to select desired markets. All markets that match the
        criteria in the filter are selected.

        :param granularity: string. The granularity of time periods that correspond
         to markets selected by the market filter. (possible values listed in TimeGranularity

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

        :param locale: string. The language used for the response.
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

        :param locale: string. The language used for the response.
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

        :param locale: string. The language used for the response. If not specified, the default is returned.
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

        :param locale: string. The language used for the response. If not specified, the default is returned.
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

        :param market_filter: The filter class to select desired
        markets. All markets that match the
        criteria in the filter are selected.

        :param market_projection: list of strings. The type and
        amount of data returned about the market.

        :param max_results: integer. limit on the total number of results
        returned, must be greater than 0 and less than or equal to 1000

        :param sort: string. The order of the results. Will default to
        RANK if not passed. RANK is an assigned priority that is
        determined by our Market Operations team in our back-end system.
        A result's overall rank is derived from the ranking given to
         the flowing attributes for the result. EventType, Competition,
          StartTime, MarketType, MarketId. For example, EventType
           is ranked by the most popular sports types and marketTypes
           are ranked in the following order: ODDS ASIAN LINE RANGE If
            all other dimensions of the result are equal, then the
            results are ranked in MarketId order.

        :param locale: string. The language used for the response.
         If not specified, the default is returned.
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

        :param market_ids: list of strings, one or more market ids.
         The number of markets returned depends on the amount
         of data you request via the price projection.
        :param book_form: The BetFairBookForm object
        '''
        data = {'marketIds': market_ids}
        data.update(book_form.data)

        response = self._make_request('listMarketBook', data=data)
        self.print_response(response)
        return response.json()

    def list_runner_book(self, market_id, selection_id, handicap=None, book_form=None):
        # TODO протестировать
        '''
        Returns a list of dynamic data about a market and a specified runner.
         Dynamic data includes prices, the status of the market, the status
         of selections, the traded volume, and the status of any
         orders you have placed in the market.
        :param selection_id: The unique id for the selection in the market.
        :param market_id: The unique id for the market.
        :param handicap: The projection of price data you want to
        receive in the response.
        :param book_form: The BetFairBookForm object
        '''
        data = {'marketId': market_id, 'selectionId': selection_id,
                'handicap': handicap}
        data.update(book_form.data)

        response = self._make_request('listRunnerBook', data=data)
        self.print_response(response)
        return response.json()

    def list_market_profit_and_loss(self, market_ids, include_settled_bets,
                                    include_bsp_bets, net_of_commission):
        # TODO протестировать
        '''
        Retrieve profit and loss for a given list of OPEN markets.
        The values are calculated using matched bets and optionally
        settled bets. Only odds (MarketBettingType = ODDS) markets
        are implemented, markets of other types are silently ignored.
        To retrieve your profit and loss for CLOSED markets, please
        use the listClearedOrders request.

        :param market_ids: List of markets to calculate profit and loss

        :param include_settled_bets: boolean. Option to include settled bets
        (partially settled markets only). Defaults to false if not specified.

        :param include_bsp_bets: boolean. Option to include BSP bets.
        Defaults to false if not specified.

        :param net_of_commission: boolean. Option to return profit and
        loss net of users current commission rate for this
         market including any special tariffs. Defaults
         to false if not specified.
        :return:
        '''
        data = {'marketIds': market_ids, 'includeSettledBets': include_settled_bets,
                'includeBspBets': include_bsp_bets, 'netOfCommission': net_of_commission}
        response = self._make_request('listMarketProfitAndLoss', data=data)
        self.print_response(response)
        return response

    def list_current_orders(self, bet_ids=None, market_ids=None,
                            order_projection=None, customer_order_refs=None,
                            customer_strategy_refs=None, date_range=None,
                            order_by=None, sort_dir=None,
                            from_record=None, record_count=None):
        '''
        Returns a list of your current orders. Optionally you can
        filter and sort your current orders using the various
         parameters, setting none of the parameters will return
         all of your current orders up to a maximum of 1000 bets,
          ordered BY_BET and sorted EARLIEST_TO_LATEST. To retrieve
           more than 1000 orders, you need to make use of the
           fromRecord and recordCount parameters.

        :param bet_ids: Optionally restricts the results to the
        specified bet IDs. A maximum of 250 betId's, or a combination
        of 250 betId's & marketId's are permitted.

        :param market_ids: Optionally restricts the results to
         the specified market IDs. A maximum of 250 marketId's, or
         a combination of 250 marketId's & betId's are permitted.

        :param order_projection: Optionally restricts the results
         to the specified order status.

        :param customer_order_refs: Optionally restricts the results
        to the specified customer order references.

        :param customer_strategy_refs: Optionally restricts the
        results to the specified customer strategy references.

        :param date_range: TimeRange object. Optionally restricts
        the results to be from/to the specified date, these dates
         are contextual to the orders being returned and therefore
         the dates used to filter on will change to placed,
         matched, voided or settled dates depending on the
         orderBy. This date is inclusive, i.e. if an order
          was placed on exactly this date (to the millisecond)
          then it will be included in the results. If the from
           is later than the to, no results will be returned.

        :param order_by: the string from OrderBy enum. Specifies
        how the results will be ordered. If no value is passed in,
        it defaults to BY_BET.  Also acts as a filter such that
         only orders with a valid value in the field being ordered
         by will be returned (i.e. BY_VOID_TIME returns only voided
         orders, BY_SETTLED_TIME (applies to partially settled markets)
         returns only settled orders and BY_MATCH_TIME returns only orders
         with a matched date (voided, settled, matched orders)). Note that
         specifying an orderBy parameter defines the context of the
         date filter applied by the dateRange parameter (placed,
         matched, voided or settled date) - see the dateRange
         parameter description (above) for more information.

        :param sort_dir: the string from SortDir enum. Specifies the
        direction the results will be sorted in. If no value
        is passed in, it defaults to EARLIEST_TO_LATEST.

        :param from_record: integer. Specifies the first record
        that will be returned. Records start at index zero, not at index one.
        :param record_count: integer. Specifies how many records
        will be returned from the index position 'fromRecord'. Note
        that there is a page size limit of 1000. A value of zero
        indicates that you would like all records (including and
        from 'fromRecord') up to the limit.
        :return:
        '''
        data = {'betIds': bet_ids, 'marketIds': market_ids,
                'orderProjection': order_projection,
                'customerOrderRefs': customer_order_refs,
                'customerStrategyRefs': customer_strategy_refs,
                'dateRange': date_range.data, 'orderBy': order_by, 'sortDir': sort_dir,
                'fromRecord': from_record, 'recordCount': record_count}
        response = self._make_request('listCurrentOrders', data=data)
        self.print_response(response)
        return response

    def list_cleared_orders(self, bet_status, event_type_ids=None,
                            event_ids=None, market_ids=None, runner_ids=None,
                            bet_ids=None, customer_order_refs=None,
                            customer_strategy_refs=None, side=None,
                            settled_date_range=None, group_by=None,
                            include_item_descr=None, locale=None,
                            from_record=None, record_count=None):
        '''
        Returns a list of settled bets based on the bet status,
        ordered by settled date. To retrieve more than 1000
        records, you need to make use of the fromRecord and
        recordCount parameters. By default the service will
        return all available data for the last 90 days (see
        Best Practice note below).  The fields available at
        each roll-up are available here

        :param bet_status: Optionally restricts the results
        :param event_type_ids: Optionally restricts the results
        :param event_ids: Optionally restricts the results
        :param market_ids: Optionally restricts the results
        :param runner_ids: Optionally restricts the results
        :param bet_ids: Optionally restricts the results
        :param side: Optionally restricts the results
        :param group_by: Optionally restricts the results
        :param include_item_descr: Optionally restricts the results
        :param locale: Optionally restricts the results
        :param from_record: Optionally restricts the results
        :param record_count: Optionally restricts the results

        :param customer_order_refs: Optionally restricts the results
        to the specified customer order references.

        :param customer_strategy_refs: Optionally restricts the
        results to the specified customer strategy references.


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
