"""
--- Day 22: Grid Computing ---
https://adventofcode.com/2016/day/22
"""
import numpy as np
from aocd import data


def parsed(data):
    lines = [x for x in data.splitlines() if x.startswith("/dev")]
    x, y = lines[-1].split()[0].replace("/dev/grid/node-x", "").split("-y")
    shape = int(y) + 1, int(x) + 1
    used = np.zeros(shape, dtype=int)
    avail = np.zeros(shape, dtype=int)
    for line in lines:
        node, _, used_, avail_, _ = line.split()
        node = node.replace("/dev/grid/node-x", "")
        col, row = [int(n) for n in node.split("-y")]
        used[row, col] = int(used_.rstrip("T"))
        avail[row, col] = int(avail_.rstrip("T"))
    return used, avail


used, avail = parsed(data)
part_a = sum((n <= avail).sum() - 1 for n in used.ravel())

used = (used / np.median(used)).round().astype(int)
used[used > 1] = 2
[row0], [col0] = np.where(used == 0)
h, w = used.shape
goal_row, goal_col = 0, w - 1
# manhattan distance between free space and goal data
dist_0_goal = row0 + (goal_col - col0)
has_detour = (used[:row0, col0] == 2).any()
w_min = np.where(used == 2)[1].min()  # wall end
# extra steps to go around the wall
detour = (col0 - (w_min - 1)) * 2 if has_detour else 0
# -1 because in moving free space to goal position, G is offset
move_data = 5 * (goal_col - 1)
part_b = dist_0_goal + detour + move_data

print("part a:", part_a)
print("part b:", part_b)
