from collections import defaultdict
from functools import reduce
from typing import Iterable, List, Any

from lib.decorators import log_invocation
from lib.utils.log_utils import get_logger

logger = get_logger(__name__)


def map_list(func: callable, i: Iterable):
    """
    Runs a map function on iterable and returns a list

    :param func:
    :param i:
    :return:
    """
    return list(map(func, i))


def filter_list(func: callable, i: Iterable) -> List[Any]:
    """
    Runs a filter function on iterable and returns a list

    :param func:
    :param i:
    :return:
    """
    return list(filter(func, i))


def reduce_items(field, items: List[Any]):
    def reducer(acc, val):
        if isinstance(acc, dict):
            acc[val[field]].append(val)

        return acc

    return reduce(reducer, items, defaultdict(list))
