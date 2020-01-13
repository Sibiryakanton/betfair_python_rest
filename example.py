import os

from managers import BetFairAPIManagerBetting, BetFairAPIManagerAccounts
from forms import (MarketFilterAndTimeGranularityForm, MarketFilterAndLocaleForm,
                   ListMarketCatalogueForm, ListMarketBookForm, ListRunnerBookForm,
                   ListMarketProfitAndLossForm, ListCurrentOrdersForm, LimitOrder,
                   ListClearedOrdersForm, PlaceOrderForm, CancelOrdersForm, ReplaceOrdersForm,
                   PlaceInstruction, CancelInstruction, ReplaceInstruction,
                   UpdateOrdersForm, UpdateInstruction)
from enums.betting import (TimeGranularity, BetStatus,
                           OrderType, PersistenceType, SideChoices,
                           MarketProjection, PriceData, MatchProjection)
from datetime import datetime, timedelta


class CustomBetFairAPIManagerBetting(BetFairAPIManagerBetting):
    crt_path = os.path.join('home', 'antonssd', 'Django-u', 'sportmind', 'client-2048.crt')
    crt_key_path = os.path.join('home', 'antonssd', 'Django-u', 'sportmind', 'client-2048.key')


class APIBettingTestCase:

    login = None
    password = None
    api_key = None

    # Examples of data
    event_types = [1]  # Soccer, Football
    competition = 7129730  # English Championship
    market_id = '1.167020296'  # Over/Under 0.5 Goals
    runners_ids = [5851482, 5851483]  # Under / Over
    event_id = 29637706  # Norwich v Bournemouth (18 Jan 2020)
    odd_over_05_price = 1.04  # Odd for Total Over 0.5 Goals (BACK)
    bet_size = 3.0
    bet_id = '191330305527'

    def __init__(self):
        self.api_manager = CustomBetFairAPIManagerBetting(self.login, self.password,
                                                          self.api_key, log_mode=True,
                                                          raise_exceptions=True)

    def test_list_event_types(self):
        market_and_locale = MarketFilterAndLocaleForm(text_query='Soccer')
        self.api_manager.list_event_types(request_class_object=market_and_locale)

    def test_list_competitions(self):
        market_and_locale = MarketFilterAndLocaleForm(text_query='English')
        self.api_manager.list_competitions(request_class_object=market_and_locale)

    def test_time_ranges(self):
        market_and_time_gran = MarketFilterAndTimeGranularityForm(text_query='Soccer',
                                                                  time_granularity=TimeGranularity.HOURS.value)
        self.api_manager.list_time_ranges(request_class_object=market_and_time_gran)

    def test_list_events(self):
        market_and_locale = MarketFilterAndLocaleForm(event_type_ids=self.event_types,
                                                      text_query='Bournemouth')
        self.api_manager.list_events(request_class_object=market_and_locale)

    def test_list_countries(self):
        market_and_locale = MarketFilterAndLocaleForm(text_query='Soccer')
        self.api_manager.list_countries(request_class_object=market_and_locale)

    def test_list_venues(self):
        market_and_locale = MarketFilterAndLocaleForm(text_query='Coffs')
        self.api_manager.list_venues(request_class_object=market_and_locale)

    def test_market_catalogue(self):
        market_projection = [MarketProjection.RUNNER_DESCRIPTION.name]
        list_market_catalogue_form = ListMarketCatalogueForm(event_type_ids=self.event_types,
                                                             market_projection=market_projection,
                                                             market_ids=[self.market_id],
                                                             max_results=500, event_ids=[self.event_id])
        self.api_manager.list_market_catalogue(request_class_object=list_market_catalogue_form)

    def test_market_book(self):
        match_proj = MatchProjection.ROLLED_UP_BY_AVG_PRICE.name
        list_market_catalogue_form = ListMarketBookForm(market_ids=[self.market_id],
                                                        price_data=[PriceData.EX_BEST_OFFERS.name],
                                                        match_projection=match_proj)
        self.api_manager.list_market_book(request_class_object=list_market_catalogue_form)

    def test_runner_book(self):
        list_runner_book_form = ListRunnerBookForm(market_id=self.market_id, selection_id=self.runners_ids[0])
        self.api_manager.list_runner_book(request_class_object=list_runner_book_form)

    def test_market_profit_loss(self):
        list_runner_book_form = ListMarketProfitAndLossForm(market_ids=[self.market_id],
                                                            include_settle_bets=True, include_bsp_bets=True,
                                                            net_of_commission=True)
        self.api_manager.list_market_profit_and_loss(request_class_object=list_runner_book_form)

    def test_list_current_orders(self):
        list_runner_book_form = ListCurrentOrdersForm()
        self.api_manager.list_current_orders(request_class_object=list_runner_book_form)

    def test_list_cleared_orders(self):
        today = datetime.now().date()
        from_date = str(today - timedelta(days=1000))
        to_date = str(today + timedelta(days=7))
        list_runner_book_form = ListClearedOrdersForm(bet_status=BetStatus.SETTLED.name,
                                                      from_date=from_date, to_date=to_date,
                                                      side=SideChoices.BACK.name)
        self.api_manager.list_cleared_orders(request_class_object=list_runner_book_form)

    def test_place_orders(self):
        limit_order = LimitOrder(persistence_type=PersistenceType.LAPSE.name,
                                 size=self.bet_size, price=self.odd_over_05_price)
        instruction_object = PlaceInstruction(order_type=OrderType.LIMIT.name,
                                              selection_id=self.runners_ids[1],
                                              side=SideChoices.BACK.name,
                                              limit_order=limit_order,
                                              )
        instructions = [instruction_object]

        list_runner_book_form = PlaceOrderForm(instructions=instructions, market_id=self.market_id)
        self.api_manager.place_orders(request_class_object=list_runner_book_form)

    def test_cancel_orders(self):
        instruction = CancelInstruction(bet_id=self.bet_id)
        list_runner_book_form = CancelOrdersForm(market_id=self.market_id,
                                                 instructions=[instruction])
        self.api_manager.cancel_orders(request_class_object=list_runner_book_form)

    def test_replace_orders(self):
        instruction = ReplaceInstruction(bet_id=self.bet_id, new_price=3.1)
        list_runner_book_form = ReplaceOrdersForm(market_id=self.market_id,
                                                  instructions=[instruction])
        self.api_manager.replace_orders(request_class_object=list_runner_book_form)

    def test_update_orders(self):
        instruction = UpdateInstruction(bet_id=self.bet_id,
                                        new_persistence_type=PersistenceType.LAPSE.name)

        list_runner_book_form = UpdateOrdersForm(market_id=self.market_id, instructions=[instruction])
        self.api_manager.update_orders(request_class_object=list_runner_book_form)


class AccountsAPITestCase:
    login = None
    password = None
    api_key = None

    def __init__(self):
        self.api_manager = BetFairAPIManagerAccounts(self.login, self.password,
                                                     self.api_key, log_mode=True,
                                                     raise_exceptions=True)

    def test_get_developer_app_keys(self):
        self.api_manager.get_developer_app_keys()

    def test_get_account_funds(self):
        self.api_manager.get_account_funds()

    def test_transfer_funds(self):
        self.api_manager.transfer_funds()

    def test_get_account_details(self):
        self.api_manager.get_account_details()

    def test_get_account_statement(self):
        self.api_manager.get_account_statement()

    def test_list_currency_rates(self):
        self.api_manager.list_currency_rates()


accounts_manager = AccountsAPITestCase()
accounts_manager.test_list_currency_rates()

test_manager = APIBettingTestCase()
test_manager.test_list_event_types()
test_manager.test_list_current_orders()
