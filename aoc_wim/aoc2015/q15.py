"""
--- Day 15: Science for Hungry People ---
https://adventofcode.com/2015/day/15
"""
from aocd import data
from parse import parse


def parsed(data):
    template = "{name}: capacity {:d}, durability {:d}, flavor {:d}, texture {:d}, calories {:d}"
    ingredients = []
    for line in data.splitlines():
        nums = parse(template, line).fixed
        ingredients.append(nums)
    return ingredients


def divisions(n, target=100):
    # tuples of length n which sum to target
    if n == 1:
        yield target,
    else:
        for i in range(target + 1):
            yield from [(i,) + t for t in divisions(n - 1, target - i)]


def score(division, ingredients, cal_target=None):
    parts = [0] * len(ingredients[0])
    for div, ingredient in zip(division, ingredients):
        part = [n * div for n in ingredient]
        parts = [a + b for a, b in zip(parts, part)]
    result = 1
    for part in parts[:-1]:
        result *= max(0, part)
    if cal_target is not None and parts[-1] != cal_target:
        result = 0
    return result


def best_score(data, cal_target=None):
    best = 0
    ingredients = parsed(data)
    for div in divisions(len(ingredients)):
        best = max(best, score(div, ingredients, cal_target=cal_target))
    return best


print(best_score(data))
print(best_score(data, cal_target=500))
