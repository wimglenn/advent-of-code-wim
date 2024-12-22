"""
--- Day 21: Keypad Conundrum ---
https://adventofcode.com/2024/day/21
"""
from aocd import data
from aoc_wim.zgrid import ZGrid
import networkx as nx
import itertools as it
from functools import cache


tdata = """\
029A
980A
179A
456A
379A
"""
# data = tdata

kn = """\
789
456
123
 0A
"""

kd = """\
 ^A
<v>
"""

dzs = dict(zip([1, 1j, -1, -1j], ">v<^"))

extra = "0123456789<^>vA"
grid0 = ZGrid(kn)
grid1 = grid2 = ZGrid(kd)
graph0 = grid0.graph(extra=extra)
graph1 = graph2 = grid1.graph(extra=extra)


code0s = data.split()
# code0s = ["379A"]


@cache
def paths(z0, z1, graph_id):
    graph = graph1 if graph_id else graph0
    results = []
    for path in nx.all_shortest_paths(graph, z0, z1):
        result = []
        for prev, current in zip(path, path[1:]):
            dz = current - prev
            result.append(dzs[dz])
        result = "".join(result) + "A"
        results.append(result)
    return results


def keep_shortest(L):
    assert all(isinstance(x, str) for x in L)
    m = len(min(L, key=len))
    # print("-"*80)
    # for x in L:
    #     if len(x) == m:
    #         print("keep", x)
    #     else:
    #         print("drop", x)
    # print("-" * 80)
    L[:] = [x for x in L if len(x) == m]


code1s = []
for code0 in code0s:
    z0 = grid0.z("A")
    code1 = []
    for char in code0:
        z1 = grid0.z(char)
        code1.append(paths(z0, z1, 0))
        z0 = z1
    code1s.append(["".join(p) for p in it.product(*code1)])

code2s = []
for code1_paths in code1s:
    code2_paths = []
    for code1_path in code1_paths:
        z0 = grid1.z("A")
        code2 = []
        for char in code1_path:
            z1 = grid1.z(char)
            code2.append(paths(z0, z1, 1))
            z0 = z1
        code2_paths.extend(["".join(p) for p in it.product(*code2)])
    keep_shortest(code2_paths)
    code2s.append(code2_paths)

code3s = []
for code2_paths in code2s:
    code3_paths = []
    for code2_path in code2_paths:
        z0 = grid2.z("A")
        code3 = []
        for char in code2_path:
            z1 = grid2.z(char)
            code3.append(paths(z0, z1, 1))
            z0 = z1
        code3_paths.extend(["".join(p) for p in it.product(*code3)])
    keep_shortest(code3_paths)
    code3s.append(code3_paths)


a = 0
for c, c3 in zip(code0s, code3s):
    a += int(c.rstrip("A")) * len(c3[0])

print("answer_a:", a)
print("answer_b:", )

# from aocd import submit; submit(a)
