"""
--- Day 20: Race Condition ---
https://adventofcode.com/2024/day/20
"""
from aocd import data
from aoc_wim.zgrid import ZGrid
import networkx as nx


grid = ZGrid(data, on=".", off="#")
S = grid.z("S")
E = grid.z("E")
grid[S] = grid[E] = "."
graph = grid.graph()
path = nx.shortest_path(graph, S, E)
t0 = nx.shortest_path_length(graph, S, E)
dist = {z: i for i, z in enumerate(reversed(path))}


dzs = -1j, 1, 1j, -1
p = [z] = [z_prev] = [S]
while p[-1] != E:
    for dz in dzs:
        if grid[z + dz] == "." and z != z_prev:
            z += dz
            p.append(z)
            break


def manhattan_ball(r=1, z0=0, full=False):
    x_left, *xs, x_right = range(-r, r + 1)
    result = [z0 + complex(x_left, 0)]
    for x in xs:
        y_max = r - abs(x)
        y_min = abs(x) - r
        if full:
            for y in range(y_min, y_max + 1):
                result.append(complex(x, y) + z0)
        else:
            result.append(complex(x, y_max) + z0)
            result.append(complex(x, y_min) + z0)
    result.append(z0 + complex(x_right, 0))
    return result


def n_cheats(t_cheat, dt_min):
    result = 0
    for z0 in path:
        for r in range(1, t_cheat + 1):
            for z in manhattan_ball(r, z0):
                if z in dist:
                    result += dist[z0] - r - dist[z] >= dt_min
    return result


dt_min = 100
print("answer_a:", n_cheats(2, dt_min))
print("answer_b:", n_cheats(20, dt_min))
