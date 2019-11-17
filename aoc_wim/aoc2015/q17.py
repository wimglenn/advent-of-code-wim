from collections import Counter

from aocd import data

from ..stuff import rsubset_sum
from ..stuff import subset_sum


test_data = """\
20
15
10
5
5
"""


def part_a(vals, target, impl=subset_sum):
    return sum(1 for subset in impl(vals, target))


def part_b(vals, target, impl=subset_sum):
    counter = Counter(len(subset) for subset in impl(vals, target))
    return counter[min(counter)]


test_vals = [int(n) for n in test_data.splitlines()]
for impl in rsubset_sum, subset_sum:
    assert part_a(test_vals, target=25, impl=impl) == 4
    assert part_b(test_vals, target=25, impl=impl) == 3


vals = [int(n) for n in data.splitlines()]
print(part_a(vals, target=150))
print(part_b(vals, target=150))
