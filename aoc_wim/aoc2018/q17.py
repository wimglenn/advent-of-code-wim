"""
--- Day 17: Reservoir Research ---
https://adventofcode.com/2018/day/17
"""
from aocd import data


def parsed(data):
    grid = {}
    for line in data.splitlines():
        a, b = line.split(", ")
        a, n = a.split("=")
        if a == "x":
            xs = [int(n)]
            y, start_stop = b.split("=")
            start, stop = start_stop.split("..")
            ys = range(int(start), int(stop) + 1)
        else:
            ys = [int(n)]
            x, start_stop = b.split("=")
            start, stop = start_stop.split("..")
            xs = range(int(start), int(stop) + 1)
        for y in ys:
            for x in xs:
                grid[complex(x, y)] = "#"
    ys = [z.imag for z in grid]
    ymin, ymax = int(min(ys)), int(max(ys))
    grid[0j + 500] = "+"
    return grid, ymin, ymax


def draw(grid, pause=False):
    print("\33c")
    xs = [int(z.real) for z in grid]
    xrange = range(min(xs) - 1, max(xs) + 2)
    yrange = range(0, int(max(z.imag for z in grid)) + 1)
    for y in yrange:
        line = []
        for x in xrange:
            line.append(grid.get(complex(x, y), "."))
        line = "".join(line)
        print(line)
        if not set(line).intersection("|+~"):
            break
    print()
    if pause:
        input("Press enter to continue...")


def xflow(grid, pos0):
    # find bounds left and right
    pos = pos0
    boundL = boundR = None
    next_flow = set()
    while True:
        if grid.get(pos - 1) == "#":
            boundL = pos
            break
        if grid.get(pos - 1 + 1j) == "|":
            break
        if grid.get(pos - 1, "|") == "|" and pos - 1 + 1j not in grid:
            next_flow.add(pos - 1)
            break
        pos -= 1
        grid[pos] = "|"
    pos = pos0
    while True:
        if grid.get(pos + 1) == "#":
            boundR = pos
            break
        if grid.get(pos + 1 + 1j) == "|":
            break
        if grid.get(pos + 1, "|") == "|" and pos + 1 + 1j not in grid:
            next_flow.add(pos + 1)
            break
        pos += 1
        grid[pos] = "|"
    if boundL is not None and boundR is not None:
        pos = boundL
        while True:
            grid[pos] = "~"
            pos += 1
            if pos.real > boundR.real:
                break
        next_flow.add(pos0 - 1j)
    return next_flow


def wet(grid, ymax, tap=1j + 500):
    flow = {tap}
    while flow:
        next_flow = set()
        for c in flow:
            grid[c] = "|"
            if c.imag >= ymax:
                continue
            if c + 1j not in grid:
                next_flow |= {c + 1j}
            elif grid[c + 1j] == "|":
                continue
            else:
                next_flow |= xflow(grid, c)
        flow = next_flow


grid, ymin, ymax = parsed(data)
wet(grid, ymax)
s = "".join(grid.values())
b = s.count("~")
a = s.count("|") + b - ymin + 1
print("part a:", a)
print("part b:", b)
