"""
--- Day 14: Space Stoichiometry ---
https://adventofcode.com/2019/day/14
"""
from aocd import data
from collections import Counter
from aoc_wim.search import Bisect
import networkx as nx


def parsed(data):
    digraph = nx.DiGraph()
    for line in data.splitlines():
        sources, dest = line.split(" => ")
        n0, elem0 = dest.split()
        for source in sources.split(", "):
            n1, elem1 = source.split()
            digraph.add_edge(elem0, elem1, ratio=(int(n0), int(n1)))
    return digraph


def part_a(data, fuel=1):
    elems = Counter({"FUEL": fuel})
    digraph = parsed(data)
    for elem0 in nx.topological_sort(digraph):
        amount = elems.pop(elem0)
        if elem0 == "ORE":
            assert not elems
            return amount
        for elem1, edge_data in digraph[elem0].items():
            n0, n1 = edge_data["ratio"]
            r = -(amount // -n0)  # ceiling division
            elems[elem1] += r * n1


def part_b(data):
    n_ore = 1000000000000
    bisect = Bisect(lambda fuel: part_a(data, fuel), val=n_ore, lo=1)
    return bisect.run()


print("part a:", part_a(data))
print("part b:", part_b(data))
