"""
--- Day 21: Step Counter ---
https://adventofcode.com/2023/day/21
"""
from aocd import data
from aoc_wim.zgrid import manhattan_distance
from aoc_wim.zgrid import ZGrid


# __import__("logging").basicConfig(level=logging.DEBUG)


data = """\
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""
from aocd import data


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



overlay = {}

def n_garden_plots_out(n_steps):
    parity = n_steps % 2
    result = 0
    for z, g in grid.items():
        d = manhattan_distance(z, z0)
        result += d > n_steps and g == "." and d % 2 == parity
        if d > n_steps and g == "." and d % 2 == parity:
            overlay[z] = "O"
    return result


a = n_garden_plots(64)
print("answer_a:", a)

p_even = n_garden_plots(d0)     # 130: 7424
p_odd = n_garden_plots(d0 - 1)  # 129: 7388

n_steps = 26501365
n, rem = divmod(n_steps, grid.height)

p = p_even + p_odd
assert p == grid.count(".")


def c4(n):
    # https://en.wikipedia.org/wiki/Centered_square_number
    return (n + 1)**2 + n**2


t = n_garden_plots_out(63)
d = c4(n)
b = d * a + (d - 1) * t
print("answer_b:", b)

# from aocd import submit; submit(b)


# b0 = n_garden_plots(65)
#
# # for n_steps in (6, 10, 50, 100, 500, 1000, 5000):
# for n_steps in (26501365,):
#     parity = n_steps % 2
#
#     n, rem = divmod(n_steps, grid.height)
#
#     b = 0
#     for i in range(1, n+1):
#         if i == 1:
#             b += p_odd
#         elif i % 2 == 0:
#             b += p_even * 4 * (i - 1)
#         else:
#             assert i % 2 == 1
#             b += p_odd * 4 * (i - 1)
#
#     print(f"answer_b ({n_steps}):", b)
