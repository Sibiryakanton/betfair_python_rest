from .abstract_forms.base import BaseForm
from .abstract_forms import (MarketIdField, CustomerStrategyRefsField, PlaceInstructionsField)
from dataclasses import dataclass


@dataclass
class PlaceOrderForm(BaseForm, CustomerStrategyRefsField, MarketIdField, PlaceInstructionsField):
    '''
    Class for request method
    It should be used like that:
    ___
    market_book_form = ListRunnerBookForm(**your_data)
    api_manager = BetFairAPIManagerBetting(login='login', password='password', api_kay='api_key')
    list_event_types_response = api_manager.list_runner_book(request_class_object=market_filter)
    ___
    You can find details about params in parent classes
    :param is_async: An optional flag (not setting equates to false)
     which specifies if the orders should be placed asynchronously.
     Orders can be tracked via the Exchange Stream API or or the API-NG
     by providing a customerOrderRef for each place order.
     An order's status will be PENDING and no bet ID will be returned.
     This functionality is available for all bet types -
     including Market on Close and Limit on Close

    :param customer_ref: Optional parameter allowing the client
    to pass a unique string (up to 32 chars) that is
     used to de-dupe mistaken re-submissions.
     CustomerRef can contain: upper/lower chars, digits,
      chars : - . _ + * : ; ~ only.
      Please note: There is a time window associated
      with the de-duplication of duplicate
      submissions which is 60 seconds.

    :param market_version: Optional parameter allowing the
     client to specify which version of the market the
    orders should be placed on. If the current market
    version is higher than that sent on an order,
    the bet will be lapsed.
    '''
    is_async: bool = None
    customer_ref: str = None
    market_version: str = None

    @property
    def data(self):
        return {'marketId': self.market_id,
                'instructions': self.instructions.data,
                'customerRef': self.customer_ref,
                'marketVersion': {'version': self.market_version},
                'customerStrategyRef': self.customer_strategy_refs,
                'async': self.is_async}
