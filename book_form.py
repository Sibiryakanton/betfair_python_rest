import logging
log = logging.getLogger('django.parsers')


class BetFairBookForm:
    '''
    The listRunnerBook and listMarketBook have the almost same input fields,
     so the common argument was moved to new class object. The logic of using same as BetfairMarketFilter:
    Let's look at an example with the listMarketBook.:
    ___
    book_form = BetFairBookForm('marketProjection'=['RUNNER_DESCRIPTION'])
    api_manager = BetFairAPIManager(login='login', password='password', api_kay='api_key')
    list_event_types_response = api_manager.list_event_types(market_filter=market_filter, locale='ru')
    ___
    '''
    def __init__(self, price_projection=None, order_projection=None,
                 match_projection=None, include_overall_position=None,
                 part_matches_by_strategy=None, customer_strategy=None,
                 currency_code=None, locale=None, matched_since=None, bet_ids=None):
        '''
        :param price_projection: The projection of price data you
        want to receive in the response.

        :param order_projection: The orders you want to receive in the response.

        :param match_projection: If you ask for orders, specifies
        the representation of matches.

        :param include_overall_position: If you ask for orders,
        returns matches for each selection. Defaults to true if unspecified.

        :param part_matches_by_strategy: If you ask for orders, returns
        the breakdown of matches by strategy for each selection.
        Defaults to false if unspecified.

        :param customer_strategy: If you ask for orders, restricts the results
         to orders matching any of the specified set of customer defined strategies.
         Also filters which matches by strategy for selections are returned,
         if partitionMatchedByStrategyRef is true.
         An empty set will be treated as if the parameter has
          been omitted (or null passed).

        :param currency_code: A Betfair standard currency code.
        If not specified, the default currency code is used.

        :param locale: The language used for the response.
        If not specified, the default is returned.

        :param matched_since: If you ask for orders, restricts the results to
        orders that have at least one fragment matched since
        the specified date (all matched fragments of such an order
        will be returned even if some were matched before the specified date).
        All EXECUTABLE orders will be returned regardless of matched date.

        :param bet_ids: The orders you want to receive in the response.

        '''
        self.data = {
            'priceProjection': price_projection,
            'orderProjection': order_projection, 'matchProjection': match_projection,
            'includeOverallPosition': include_overall_position,
            'partitionMatchedByStrategyRef': part_matches_by_strategy,
            'customerStrategyRefs': customer_strategy, 'currencyCode': currency_code,
            'locale': locale, 'matchedSince': matched_since, 'betIds': bet_ids
        }
