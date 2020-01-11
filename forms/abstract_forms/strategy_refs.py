from dataclasses import dataclass
from datetime import datetime


@dataclass
class StrategyRefs:
    '''
    :param partition_matched_by_strategy_ref: If you ask for orders,
     returns the breakdown of matches by strategy for
     each selection. Defaults to false if unspecified.
    :param custom_strategy_refs: If you ask for orders, restricts
    the results to orders matching any of the specified set of
     customer defined strategies. Also filters which matches by
     strategy for selections are returned, if
     partitionMatchedByStrategyRef is true. An empty set will
     be treated as if the parameter has been omitted (or null passed).
    '''

    partition_matched_by_strategy_ref: bool = None
    custom_strategy_refs: list = None
