"""
--- Day 17: No Such Thing as Too Much ---
https://adventofcode.com/2015/day/17
"""
from collections import Counter

from aocd import data

from aoc_wim.stuff import subset_sum


def part_a(vals, target, impl=subset_sum):
    return sum(1 for subset in impl(vals, target))


def part_b(vals, target, impl=subset_sum):
    counter = Counter(len(subset) for subset in impl(vals, target))
    return counter[min(counter)]


if __name__ == "__main__":
    vals = [int(n) for n in data.splitlines()]
    print(part_a(vals, target=150))
    print(part_b(vals, target=150))
