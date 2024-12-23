"""
--- Day 18: RAM Run ---
https://adventofcode.com/2024/day/18
"""
from aocd import data
from aocd import extra
from aoc_wim.zgrid import ZGrid
import networkx as nx


w = extra.get("width", 71)
n_bytes = extra.get("n_bytes", 1024)
grid = ZGrid.fromempty(w, w, glyph=".")
zs = [complex(*map(int, x.split(","))) for x in data.split()]

grid.update({z: "#" for z in zs[:n_bytes]})
graph = grid.graph()
path = nx.shortest_path(graph, 0, complex(w-1, w-1))
print("answer_a:", len(path) - 1)

for z in zs[n_bytes:]:
    grid[z] = "#"
    if z not in path:
        continue
    graph = grid.graph()
    try:
        path = nx.shortest_path(graph, 0, complex(w-1, w-1))
    except nx.NetworkXNoPath:
        print("answer_b:", f"{int(z.real)},{int(z.imag)}")
        break
