"""
--- Day 21: Keypad Conundrum ---
https://adventofcode.com/2024/day/21
"""
from aocd import data
from aoc_wim.zgrid import ZGrid
import networkx as nx
from collections import Counter


keypad_numeric = """\
789
456
123
 0A
"""
keypad_directional = """\
 ^A
<v>
"""
dzs = dict(zip([1, 1j, -1, -1j], ">v<^"))
glyph0 = "0123456789A"
glyph1 = "<^v>A"
grid0 = ZGrid(keypad_numeric)
grid1 = ZGrid(keypad_directional)
graph0 = grid0.graph(extra=glyph0)
graph1 = grid1.graph(extra=glyph1)


def step_counts(z0, z1, graph):
    paths = []
    for path in nx.all_shortest_paths(graph, z0, z1):
        d_path = "".join(dzs[b - a] for a, b in zip(path, path[1:])) + "A"
        paths.append(d_path)
    seq = [sum(x == y for x, y in zip(p, p[1:])) for p in paths]
    max_seq = max(seq)
    paths = [p for s, p in zip(seq, paths) if s == max_seq]
    path = min(paths, key=lambda p: glyph1.index(p[0]))
    counts = Counter(c0 + c1 for c0, c1 in zip("A" + path, path))
    return counts


steps = {}
for src in glyph0:
    for dst in glyph0:
        steps[src + dst] = step_counts(grid0.z(src), grid0.z(dst), graph0)
for src in glyph1:
    for dst in glyph1:
        steps[src + dst] = step_counts(grid1.z(src), grid1.z(dst), graph1)


def complexity(code, n):
    tz0 = sum([steps[c0 + c1] for c0, c1 in zip("A" + code, code)], Counter())
    for i in range(n):
        tz = Counter()
        for k0, n0 in tz0.items():
            ck = steps[k0]
            tz += Counter({k1: n0 * n1 for k1, n1 in ck.items()})
        tz0 = tz
    path_length = sum(tz0.values())
    result = int(code[:-1]) * path_length
    return result


a = sum([complexity(code, n=2) for code in data.split()])
b = sum([complexity(code, n=25) for code in data.split()])
print("answer_a:", a)
print("answer_b:", b)
