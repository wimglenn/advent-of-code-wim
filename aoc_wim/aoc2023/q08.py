"""
--- Day 8: Haunted Wasteland ---
https://adventofcode.com/2023/day/8
"""
from math import lcm

from aocd import data

path, graph = data.split("\n\n")
d = {}
for line in graph.splitlines():
    S, LR = line.split(" = ")
    d[S] = LR.strip("()").split(", ")


def sync(nodes):
    i = 0
    n = len(nodes)
    z0 = [None] * n
    while True:
        s = path[i % len(path)]
        nodes = [d[x][s == "R"] for x in nodes]
        i += 1
        for j in range(n):
            if nodes[j].endswith("Z") and z0[j] is None:
                z0[j] = i
                if all(z0):
                    return lcm(*z0)


if "AAA" in d:
    print("answer_a:", sync(["AAA"]))
print("answer_b:", sync([x for x in d if x.endswith("A")]))
