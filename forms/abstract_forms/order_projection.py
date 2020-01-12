from dataclasses import dataclass


@dataclass
class OrderProjectionField:
    '''
    Optionally restricts the results to the specified order
     status. Allowed variables listed in OrderProjection enum.

    List of params:
    :param order_projection:  Optionally restricts the results to the specified order

    '''
    order_projection: str = None

    @property
    def price_projection_data(self):
        return {
            'priceData': self.price_data,
            'exBestOffersOverrides': self.ex_best_offers_overrides_data,
            'virtualise': self.virtualise,
            'rolloverStakes': self.rollover_stakes,
        }
