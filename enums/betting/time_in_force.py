from ..base import BaseEnum


class TimeInForce(BaseEnum):
    FILL_OR_KILL = '''Execute the transaction 
    immediately and completely (filled to size 
    or between minFillSize and size) or not 
    at all (cancelled).
    For LINE markets 
    Volume Weighted Average Price (VWAP) 
    functionality is disabled'''
