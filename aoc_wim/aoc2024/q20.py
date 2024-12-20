"""
--- Day 20: Race Condition ---
https://adventofcode.com/2024/day/20
"""
from aocd import data, extra
from aoc_wim.zgrid import ZGrid, manhattan_ball


grid = ZGrid(data)
S, E = grid.z("S"), grid.z("E")
grid[S] = "."
dzs = -1j, 1, 1j, -1
path = [z_prev] = [E]
while path[-1] != S:
    for dz in dzs:
        z = path[-1] + dz
        if grid[z] == "." and z != z_prev:
            z_prev = path[-1]
            path.append(z)
            break
path = {z: i for i, z in enumerate(path)}  # {pos: distance from goal}


def n_cheats(t_cheat, dt_min):
    result = 0
    for z0, d in path.items():
        for r in range(1, t_cheat + 1):
            for z in manhattan_ball(r, z0):
                if z in path:
                    result += d - r - path[z] >= dt_min
    return result


dt_min = extra.get("dt_min", 100)
print("answer_a:", n_cheats(2, dt_min))
print("answer_b:", n_cheats(20, dt_min))
