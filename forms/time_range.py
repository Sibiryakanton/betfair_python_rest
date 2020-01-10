

class TimeRange:
    '''
    The TimeRange can be useful in listClearedOrders request.
    Let's look at an example of using:
    ___
    time_range_obj = TimeRange(from_date='YOUR_DATETIME', to_date-'YOUR_DATETIME')
    api_manager = BetFairAPIManagerBetting(login='login', password='password', api_kay='api_key')
    list_current_orders_response = api_manager.list_current_orders(time_range=time_range_obj)
    ___
    '''
    def __init__(self, from_date, to_date):
        '''
        :param from_date: datetime-object.
        :param to_date: datetime-object

        '''
        self.data = {
            'from': from_date,
            'to': to_date
        }