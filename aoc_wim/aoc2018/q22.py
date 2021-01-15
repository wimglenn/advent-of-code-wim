"""
--- Day 22: Mode Maze ---
https://adventofcode.com/2018/day/22
"""
from aocd import data
from parse import parse
from aoc_wim.search import AStar
from aoc_wim.zgrid import zrange
from aoc_wim.zgrid import manhattan_distance


# TODO: use zgrid


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
                self._gi[pos] = self.el(pos - 1) * self.el(pos - 1j)
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


class Q22AStar(AStar):

    tools = {None, "🔦", "🧗"}

    valid_tools = {
        ".": tools - {None},  # you'll likely slip and fall
        "=": tools - {"🔦"},  # if it gets wet, you won't have a light source
        "|": tools - {"🧗"},  # it's too bulky to fit
    }

    def __init__(self, state0, target, grid):
        super().__init__(state0, target)
        self.grid = grid

    def heuristic(self, state0, state1):
        z0, tool0 = state0
        z1, tool1 = state1
        result = manhattan_distance(z1, z0)
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
            assert abs(z1 - z0) == 1
            return 1

    def adjacent(self, state):
        # 012   .=|   rocky, wet, narrow   no neither, no torch, no climbing gear
        # None, "🔦", "🧗"
        z_here, tool = state
        current_terain = Grid.glyph[self.grid.t(z_here)]
        assert tool in self.valid_tools[current_terain]
        zs = [z_here + 1, z_here + 1j]
        if z_here.real > 0:
            zs.append(z_here - 1)
        if z_here.imag > 0:
            zs.append(z_here - 1j)
        terrains = [Grid.glyph[self.grid.t(z)] for z in zs]
        zs = [z for z, t in zip(zs, terrains) if tool in self.valid_tools[t]]
        zs = [(z, tool) for z in zs]
        tools = Q22AStar.tools - {tool}
        zs.extend([(z_here, t) for t in tools if t in self.valid_tools[current_terain]])
        return zs


grid = parsed(data)
print("part a:", sum(grid.t(z) for z in zrange(0, grid.target + 1 + 1j)))

state0 = (grid.pos, "🔦")
target = (grid.target, "🔦")
a_star = Q22AStar(state0=state0, target=target, grid=grid)
a_star.run()
print("part b:", a_star.gscore[target])
