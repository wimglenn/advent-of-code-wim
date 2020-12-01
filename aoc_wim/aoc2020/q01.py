from math import prod
from aocd import data
from aoc_wim.stuff import subset_sum

numbers = sorted(int(x) for x in data.splitlines())

a = b = None
for subset in subset_sum(numbers, target=2020):
    if len(subset) == 2:
        a = prod(subset)
        print("part a:", a)
        if b is not None:
            break
    elif len(subset) == 3:
        b = prod(subset)
        print("part b:", b)
        if a is not None:
            break
