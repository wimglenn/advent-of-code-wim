"""
--- Day 11: Reactor ---
https://adventofcode.com/2025/day/11
"""

from aocd import data
from functools import cache

graph = {}
for line in data.splitlines():
    x, ys = line.split(": ")
    graph[x] = ys.split()


@cache
def n_paths(src, dst):
    return src == dst or sum(n_paths(x, dst) for x in graph.get(src, []))


if "you" in graph:
    print("answer_a:", n_paths("you", "out"))

if "svr" in graph:
    b0 = n_paths("svr", "fft") * n_paths("fft", "dac") * n_paths("dac", "out")
    b1 = n_paths("svr", "dac") * n_paths("dac", "fft") * n_paths("fft", "out")
    print("answer_b:", b0 + b1)
