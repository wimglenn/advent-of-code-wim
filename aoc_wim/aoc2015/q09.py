"""
--- Day 9: All in a Single Night ---
https://adventofcode.com/2015/day/9
"""
from itertools import permutations

from aocd import data


def parsed(data):
    distances = {}
    cities = set()
    for line in data.splitlines():
        a, to, b, equals, n = line.split()
        cities |= {a, b}
        distances[(a, b)] = distances[(b, a)] = int(n)
    return cities, distances


def total_distance(route, distances):
    return sum(distances[p] for p in zip(route[:-1], route[1:]))


def get_routes(data):
    cities, distances = parsed(data)
    return {route: total_distance(route, distances) for route in permutations(cities)}


routes = get_routes(data)
print("part a:", min(routes.values()))
print("part b:", max(routes.values()))
