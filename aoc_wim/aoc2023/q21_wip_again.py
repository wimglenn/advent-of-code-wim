"""
--- Day 21: Step Counter ---
https://adventofcode.com/2023/day/21
"""
from aocd import data
from aoc_wim.zgrid import manhattan_distance
from aoc_wim.zgrid import ZGrid


# __import__("logging").basicConfig(level=logging.DEBUG)


grid = ZGrid(data)
z0 = grid.z("S")
grid[z0] = "."
state0 = z0, 0
d0 = manhattan_distance(z0)

# plug holes
for z in grid:
    if grid.count_near(z, "#") == 4:
        grid[z] = "#"


def n_garden_plots(n_steps):
    parity = n_steps % 2
    result = 0
    for z, g in grid.items():
        d = manhattan_distance(z, z0)
        result += d <= n_steps and g == "." and d % 2 == parity
    return result


a = n_garden_plots(64)
print("answer_a:", a)
p_even = n_garden_plots(d0)     # 130: 7424
p_odd = n_garden_plots(d0 - 1)  # 129: 7388

n_steps = 26501365
parity = n_steps % 2

n_plots = grid.count(".")
n, rem = divmod(n_steps, grid.height)

b = n * n * n_plots


def c4(n):
    # https://en.wikipedia.org/wiki/Centered_square_number
    return n**2 + (n - 1)**2
