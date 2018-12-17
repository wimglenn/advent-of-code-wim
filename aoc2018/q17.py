from aocd import data
from operator import attrgetter
import sys


test_data = """x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504"""


def parsed(data):
    grid = {}
    for line in data.splitlines():
        a, b = line.split(', ')
        a, n = a.split('=')
        if a == "x":
            xs = [int(n)]
            y, start_stop = b.split('=')
            start, stop = start_stop.split('..')
            ys = range(int(start), int(stop) + 1)
        else:
            ys = [int(n)]
            x, start_stop = b.split('=')
            start, stop = start_stop.split('..')
            xs = range(int(start), int(stop) + 1)
        for y in ys:
            for x in xs:
                grid[complex(x, y)] = '#'

    w0 = int(min(grid, key=attrgetter("real")).real) - 1
    w1 = int(max(grid, key=attrgetter("real")).real) + 2
    h0 = int(min(grid, key=attrgetter("imag")).imag)
    h1 = int(max(grid, key=attrgetter("imag")).imag) + 1
    grid["y-min"] = h0
    grid["y-axis"] = range(0, h1)
    grid["x-axis"] = range(w0, w1)
    grid[0j + 500] = "+"
    return grid


def dump(grid):
    print("\33c")
    for y in grid["y-axis"]:
        line = []
        for x in grid["x-axis"]:
            line.append(grid.get(complex(x, y), "."))
        line = ''.join(line)
        print(line)
        if set(line) & set("|~+"):
            break
    print()


class Ystream:

    def __init__(self, grid, pos):
        while pos not in grid:
            if pos.imag >= grid["y-axis"].stop:
                return
            grid[pos] = "|"
            pos += 1j
        if grid[pos] in "#~":
            Xstream(grid, pos - 1j)


class Xstream:

    def __init__(self, grid, pos):
        if grid[pos] == "~":
            return
        left_wall = right_wall = False
        left_fall = right_fall = False
        filled = [pos]
        dx = 1
        while True:
            if not right_wall and not right_fall:
                if pos + dx not in grid or grid[pos + dx] == "|":
                    grid[pos + dx] = "|"
                    filled.append(pos + dx)
                    if pos + dx + 1j not in grid:
                        right_fall = pos + dx + 1j
                elif grid[pos + dx] == "#":
                    right_wall = True
            if not left_wall and not left_fall:
                if pos - dx not in grid  or grid[pos - dx] == "|":
                    grid[pos - dx] = "|"
                    filled.append(pos - dx)
                    if pos - dx + 1j not in grid:
                        left_fall = pos - dx + 1j
                elif grid[pos - dx] == "#":
                    left_wall = True
            if (left_wall or left_fall) and (right_wall or right_fall):
                break
            dx += 1
        if left_wall and right_wall:
            for pos in filled:
                grid[pos] = "~"
            for pos in filled:
                if grid.get(pos - 1j) == "|":
                    Xstream(grid, pos - 1j)
                    break
        if left_fall:
            Ystream(grid, left_fall)
        if right_fall:
            Ystream(grid, right_fall)


def part_ab(data):
    grid = parsed(data)
    Ystream(grid, 1j + 500)
    result_a = 0
    result_b = 0
    for y in grid["y-axis"]:
        if y < grid["y-min"]:
            continue
        for x in grid["x-axis"]:
            v = grid.get(complex(x, y))
            if v == "~":
                result_a += 1
                result_b += 1
            elif v == "|":
                result_a += 1
    part_ab.grid = grid
    return result_a, result_b


sys.setrecursionlimit(3000)
assert part_ab(test_data) == (57, 29)
a, b = part_ab(data)
print(a)  # 31953
print(b)  # 26410
