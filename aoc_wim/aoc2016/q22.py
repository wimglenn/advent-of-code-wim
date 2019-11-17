import numpy as np
from aocd import data


test_data = """\
Filesystem            Size  Used  Avail  Use%
/dev/grid/node-x0-y0   10T    8T     2T   80%
/dev/grid/node-x0-y1   11T    6T     5T   54%
/dev/grid/node-x0-y2   32T   28T     4T   87%
/dev/grid/node-x1-y0    9T    7T     2T   77%
/dev/grid/node-x1-y1    8T    0T     8T    0%
/dev/grid/node-x1-y2   11T    7T     4T   63%
/dev/grid/node-x2-y0   10T    6T     4T   60%
/dev/grid/node-x2-y1    9T    8T     1T   88%
/dev/grid/node-x2-y2    9T    6T     3T   66%
"""


def parse(data):
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


def part_a(data):
    used, avail = parse(data)
    return sum((n <= avail).sum() - 1 for n in used.ravel())


def part_b(data):
    used, _ = parse(data)
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
    steps = dist_0_goal + detour + move_data
    return steps


assert part_b(test_data) == 7
print("part a:", part_a(data))
print("part b:", part_b(data))
