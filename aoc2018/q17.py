from aocd import data
from operator import attrgetter


test_data = """\
x=495, y=2..7
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


def dump(grid, pause=False):
    print("\33c")
    for y in grid["y-axis"]:
        line = []
        for x in grid["x-axis"]:
            line.append(grid.get(complex(x, y), "."))
        line = ''.join(line)
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
        if grid.get(pos - 1) == "|" and grid.get(pos - 1 + 1j) is None:
            next_flow.add(pos - 1)
            break
        if pos - 1 not in grid and pos - 1 +1j not in grid:
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
        if grid.get(pos + 1) == "|" and grid.get(pos + 1 + 1j) is None:
            next_flow.add(pos + 1)
            break
        if pos + 1 not in grid and pos + 1 +1j not in grid:
            next_flow.add(pos + 1)
            break
        pos += 1
        grid[pos] = "|"
    if boundL is not None and boundR is not None:
        assert not next_flow
        pos = boundL
        while True:
            grid[pos] = "~"
            pos += 1
            if pos.real > boundR.real:
                break
        next_flow.add(pos0 - 1j)
    assert len(next_flow) in {0, 1, 2}
    return next_flow


def wet(grid, tap=1j+500):
    flow = {tap}
    while flow:
        next_flow = set()
        for c in flow:
            grid[c] = "|"
            if c.imag >= grid["y-axis"].stop:
                continue
            if c + 1j not in grid:
                next_flow |= {c + 1j}
            elif grid[c+1j] == "|":
                continue
            else:
                assert grid[c+1j] in "~#"
                next_flow |= xflow(grid, c)
        flow = next_flow


def part_ab(data):
    grid = parsed(data)
    wet(grid)
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


assert part_ab(test_data) == (57, 29)

a, b = part_ab(data)
print("part a:", a)
print("part b:", b)
