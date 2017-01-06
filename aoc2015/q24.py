from aocd import data
from functools import reduce
from operator import mul
from itertools import combinations
from collections import Counter


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


def parse_data(data, n_groups):
    vals = [int(n)for n in data.strip().split()]
    total = sum(vals)
    if total % n_groups != 0:
        raise Exception
    return vals, total//n_groups


def bag_sub(list_big, sublist):
    counter = Counter(sublist)
    result = []
    for k in list_big:
        counter[k] -= 1
        if counter[k] < 0:
            result.append(k)
    return result


def partitions(vals, target):
    for group in subset_sum(vals, target):
        remaining = bag_sub(vals, group)
        groups = partitions(remaining, target) if sum(remaining) > target else (remaining,)
        yield from ((group, group_) for group_ in groups)


def prod(vals):
    return reduce(mul, vals)


def get_shortest_sums(vals, target):
    results = []
    for i in range(len(vals)):
        for comb in combinations(vals, i):
            if sum(comb) == target:
                results.append(comb)
        if results:
            return results
        del results[:]


def solve(data, n_groups):
    vals, target = parse_data(data, n_groups=n_groups)
    group1s = get_shortest_sums(vals, target)
    group1s.sort(key=prod)

    for group1 in group1s:
        remaining = bag_sub(vals, group1)
        gen = partitions(remaining, target)
        try:
            next(gen)
        except StopIteration:
            continue
        return prod(group1)


test_data = '1 2 3 4 5 7 8 9 10 11'

assert solve(test_data, n_groups=3) == 99
assert solve(test_data, n_groups=4) == 44

print(solve(data, n_groups=3))  # part a: 11846773891
print(solve(data, n_groups=4))  # part b: 80393059
