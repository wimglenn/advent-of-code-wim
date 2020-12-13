from collections import Counter
from functools import lru_cache
from math import sqrt


def rsubset_sum(vals, target=0):
    # recursion impl

    @lru_cache(maxsize=None)
    def worker(hand=frozenset()):
        sum_ = sum(vals[i] for i in hand)
        if sum_ == target:
            result = {hand}
        elif sum_ > target:
            result = set()
        else:
            choices = set(range(len(vals))) - hand
            hands = (worker(hand | {choice}) for choice in choices)
            result = set().union(*hands)
        return result

    result = [[vals[i] for i in way] for way in set(worker())]
    return result


def subset_sum(vals, target=0):
    # dynamic programming impl
    sums = {0: [()]}  # key=sum, value=list of subsets for the sum
    if target in sums:
        yield from sums[target]  # annoying base case
    for val in vals:
        items = sums.items()  # don't change dict size during iteration
        sums = dict(items)
        for prev_sum, prev_subsets in items:
            sum_ = prev_sum + val
            subsets = [s + (val,) for s in prev_subsets]
            sums[sum_] = sums.get(sum_, []) + subsets
            if sum_ == target:
                yield from subsets


def ways(total, coins=(1, 2, 5, 10, 20, 50, 100)):
    ways = [[Counter()]] + [[] for _ in range(total)]
    for coin in coins:
        for i in range(coin, total + 1):
            ways[i] += [way + Counter({coin: 1}) for way in ways[i - coin]]
    return ways[total]


class Tribonacci(dict):
    """https://oeis.org/A000073"""

    def __init__(self):
        self[0] = self[1] = 0
        self[2] = 1

    def __missing__(self, key):
        val = self[key - 1] + self[key - 2] + self[key - 3]
        self[key] = val
        return val


def factorise(n):
    """returns the sorted prime factors of natural number n

    >>> factorise(12)
    [2, 2, 3]
    >>> factorise(4998)
    [2, 3, 7, 7, 17]
    >>> factorise(4999)
    [4999]"""
    if n < 0:
        result = factorise(-n)
        result[0] *= -1
        return result
    for i in range(2, int(1 + sqrt(n))):
        if n % i == 0:
            return [i] + factorise(n // i)
    else:
        return [n]


def extended_euclidean(a, b):
    # find m1, m2 such that a*m1 + b*m2 = gcd(a, b)
    r_prev, r = a, b
    s_prev, s = 1, 0
    t_prev, t = 0, 1
    while r:
        q = r_prev // r
        r_prev, r = r, r_prev - q * r
        s_prev, s = s, s_prev - q * s
        t_prev, t = t, t_prev - q * t
    if s_prev < 0:
        s_prev += a
    if t_prev < 0:
        t_prev += b
    return s_prev, t_prev
