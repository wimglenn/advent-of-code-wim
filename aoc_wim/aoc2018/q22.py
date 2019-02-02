from aocd import data
from parse import parse
from ..astar import AStar


def zrange(*args):
    if len(args) == 1:
        start = 0
        stop, = args
        step = 1 + 1j
    elif len(args) == 2:
        start, stop = args
        step = 1 + 1j
    elif len(args) == 3:
        start, stop, step = args
    else:
        raise TypeError(f"zrange expected 1-3 arguments, got {len(args)}")
    ys = range(int(start.imag), int(stop.imag), int(step.imag))
    xs = range(int(start.real), int(stop.real), int(step.real))
    return (complex(x, y) for y in ys for x in xs)


class Grid:

    glyph = dict(enumerate(".=|"))  # rocky, wet, narrow

    def __init__(self, depth, tx, ty):
        self.depth = depth
        self.pos = 0
        self.target = complex(tx, ty)
        self._gi = {self.pos: 0, self.target: 0}

    def el(self, pos):
        return (self.gi(pos) + self.depth) % 20183

    def t(self, pos):
        return self.el(pos) % 3

    def gi(self, pos):
        if pos not in self._gi:
            if pos.imag == 0:
                self._gi[pos] = 16807 * int(pos.real)
            elif pos.real == 0:
                self._gi[pos] = 48271 * int(pos.imag)
            else:
                self._gi[pos] = self.el(pos-1) * self.el(pos-1j)
        return self._gi[pos]


def parsed(data):
    template = "depth: {:d}\ntarget: {:d},{:d}"
    d, x, y = parse(template, data)
    grid = Grid(d, x, y)
    return grid


def draw(grid, z0=0, z1=None):
    if z1 is None:
        z1 = grid.target + 6 + 6j
    for z in zrange(z0, z1):
        if z == grid.pos:
            g = "M"
        elif z == grid.target:
            g = "T"
        else:
            g = Grid.glyph[grid.t(z)]
        print(g, end="")
        if z.real + 1 == z1.real:
            print()


def part_a(data):
    grid = parsed(data)
    result = sum(grid.t(z) for z in zrange(0, grid.target + 1 + 1j))
    return result


class Q22AStar(AStar):

    tools = {None, "🔦", "🧗"}

    valid_tools = {
        '.': tools - {None},  # you'll likely slip and fall
        '=': tools - {"🔦"},  # if it gets wet, you won't have a light source
        '|': tools - {"🧗"},  # it's too bulky to fit
    }

    def __init__(self, state0, target, grid):
        super().__init__(state0, target)
        self.grid = grid

    def heuristic(self, state0, state1):
        z0, tool0 = state0
        z1, tool1 = state1
        delta = z1 - z0
        result = int(abs(delta.real) + abs(delta.imag))
        if tool0 != tool1:
            result += 7
        return result

    def cost(self, current_state, next_state):
        z0, tool0 = current_state
        z1, tool1 = next_state
        if z0 == z1:
            assert tool0 != tool1
            return 7
        else:
            assert abs(z1-z0) == 1
            return 1

    def adjacent(self, state):
        # 012   .=|   rocky, wet, narrow   no neither, no torch, no climbing gear
        # None, "🔦", "🧗"
        z_here, tool = state
        current_terain = Grid.glyph[self.grid.t(z_here)]
        assert tool in self.valid_tools[current_terain]
        candidates = [z_here + 1, z_here + 1j]
        if z_here.real > 0:
            candidates.append(z_here - 1)
        if z_here.imag > 0:
            candidates.append(z_here - 1j)
        terrains = [Grid.glyph[self.grid.t(z)] for z in candidates]
        candidates = [z for z, t in zip(candidates, terrains) if tool in self.valid_tools[t]]
        candidates = [(z, tool) for z in candidates]
        candidates.extend([(z_here, t) for t in Q22AStar.tools - {tool} if t in self.valid_tools[current_terain]])
        return candidates


def part_b(data):
    grid = parsed(data)
    state0 = (grid.pos, "🔦")
    target = (grid.target, "🔦")
    a_star = Q22AStar(state0=state0, target=target, grid=grid)
    a_star.run()
    result = a_star.gscore[target]
    return result


test_data = """\
depth: 510
target: 10,10"""


assert part_a(test_data) == 114
assert part_b(test_data) == 45

print("part a:", part_a(data))
print("part b:", part_b(data))
