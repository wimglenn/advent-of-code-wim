from aocd import data
from collections import Counter
from functools import lru_cache


test_data = '''
20
15
10
5
5
'''.strip()


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
            result = set.union(*hands)
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


def part_a(vals, target, impl=subset_sum):
    return sum(1 for subset in impl(vals, target))

def part_b(vals, target, impl=subset_sum):
    counter = Counter(len(subset) for subset in impl(vals, target))
    return counter[min(counter)]


test_vals = [int(n) for n in test_data.splitlines()]
vals = [int(n) for n in data.splitlines()]

for impl in rsubset_sum, subset_sum:
    assert part_a(test_vals, target=25, impl=impl) == 4
    assert part_b(test_vals, target=25, impl=impl) == 3

print(part_a(vals, target=150))  # 1638
print(part_b(vals, target=150))  # 17
