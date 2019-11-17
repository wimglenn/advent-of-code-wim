import numpy as np
from aocd import data


def part_ab(data):
    A = np.zeros((1000, 1000), dtype=bool)
    B = np.zeros((1000, 1000), dtype=int)

    for line in data.splitlines():
        action, p1, _, p2 = line.rsplit(None, 3)
        x1, y1 = [int(n) for n in p1.split(",")]
        x2, y2 = [int(n) for n in p2.split(",")]
        t = slice(x1, x2 + 1), slice(y1, y2 + 1)
        if action == "toggle":
            A[t] = ~A[t]
            B[t] += 2
        elif action == "turn on":
            A[t] = True
            B[t] += 1
        elif action == "turn off":
            A[t] = False
            B[t] -= 1
            B = B.clip(min=0)
        else:
            raise Exception

    return A.sum(), B.sum()


assert part_ab("turn on 0,0 through 999,999")[0] == 1000 ** 2
assert part_ab("toggle 0,0 through 999,0")[0] == 1000
assert part_ab("turn off 499,499 through 500,500")[0] == 0
assert part_ab("turn on 0,0 through 0,0")[1] == 1
assert part_ab("toggle 0,0 through 999,999")[1] == 2000000


a, b = part_ab(data)
print("part a:", a)
print("part b:", b)
