import string
from collections import ChainMap
import numpy as np
import networkx as nx


dzs = [-1j, 1, 1j, -1]


class ZGrid:

    dzs = ChainMap(
        dict(zip(dzs, dzs)),
        dict(zip("^>v<", dzs)),
        dict(zip("up right down left".split(), dzs)),
        dict(zip("up right down left".upper().split(), dzs)),
        dict(zip("URDL", dzs)),
        dict(zip("NESW", dzs)),
    )
    U = N = up = north = -1j
    R = E = right = east = 1
    D = S = down = south = 1j
    L = W = left = west = -1

    turn_right = 1j
    turn_left = -1j
    turn_around = -1

    def __init__(self, initial_data=None, on="#", off="."):
        self.on = on
        self.off = off
        self.d = d = {}
        if initial_data is not None:
            if isinstance(initial_data, str):
                for row, line in enumerate(initial_data.splitlines()):
                    for col, char in enumerate(line):
                        d[col + row*1j] = char
            if isinstance(initial_data, dict):
                self.d = initial_data

    def __setitem__(self, key, value):
        self.d[key] = value

    def __getitem__(self, key):
        return self.d[key]

    def __delitem__(self, key):
        del self.d[key]

    def __contains__(self, item):
        return item in self.d

    def __iter__(self):
        return iter(self.d)

    def __len__(self):
        return len(self.d)

    def items(self):
        return self.d.items()

    def values(self):
        return self.d.values()

    def get(self, k, default=None):
        return self.d.get(k, default)

    def near(self, z, n=4):
        if n == 4:
            return [z - 1j, z + 1, z + 1j, z - 1]
        elif n == 8:
            return [
                z - 1 - 1j, z - 1j, z + 1 - 1j,
                z - 1, z + 1,
                z - 1 + 1j, z + 1j, z + 1 + 1j,
            ]

    def draw(self, overlay=None, clear=False, pretty=True):
        d = self.d
        if overlay is not None:
            d = {**self.d, **overlay}
        dump_grid(d, clear=clear, pretty=pretty)

    def translate(self, table):
        for z in self.d:
            if self.d[z] in table:
                self.d[z] = table[self.d[z]]

    @property
    def n_on(self):
        return sum(1 for val in self.d.values() if val == self.on)

    def n_on_near(self, z0, n=4):
        return sum(1 for z in self.near(z0, n=n) if self.d.get(z) == self.on)

    def __array__(self):
        """makes np.array(zgrid) work"""
        zs = np.array(list(self.d))
        xs = zs.real.astype(int)
        ys = zs.imag.astype(int)
        vs = np.array(list(self.d.values()))
        w = xs.ptp() + 1
        h = ys.ptp() + 1
        full = np.full((h, w), fill_value=self.off, dtype=vs.dtype)
        full[ys - ys.min(), xs - xs.min()] = vs
        return full

    def graph(self, extra=()):
        """connected components"""
        node_glyphs = {self.on}.union(extra)
        g = nx.Graph()
        g.extra = {}
        for pos, glyph in self.d.items():
            if glyph in node_glyphs:
                g.add_node(pos)
                if glyph != self.on:
                    g.extra[glyph] = pos
                right = pos + 1
                down = pos + 1j
                if self.d.get(right) in node_glyphs:
                    g.add_edge(pos, right)
                if self.d.get(down) in node_glyphs:
                    g.add_edge(pos, down)
        return g


def dump_grid(g, clear=False, pretty=True):
    transform = {
        "#": "⬛",
        ".": "  ",
        "O": "🤖",
        "T": "🥇",
        ">": "➡️ ",
        "<": "⬅️ ",
        "^": "⬆️ ",
        "v": "⬇️ ",
        "@": "@️ ",
        0: "  ",
        1: "⬛",
    }
    transform.update({x: x + " " for x in string.ascii_letters})
    empty = "  " if pretty else "."
    print()
    xs = [int(z.real) for z in g]
    ys = [int(z.imag) for z in g]
    cols = range(min(xs), max(xs) + 1)
    rows = range(min(ys), max(ys) + 1)
    if clear:
        print("\033c")
    for row in rows:
        print(f"{row:>5d} ", end="")
        for col in cols:
            glyph = g.get(col + row * 1j, empty)
            if pretty:
                glyph = transform.get(glyph, glyph)
            print(glyph, end="")
        print()
    W = len(cols)
    if pretty:
        W *= 2
    footer_left = f"{cols[0]}".ljust(W)
    footer_center = f"{cols[len(cols)//2]}".center(W)
    footer_right = f"{cols[-1]}".rjust(W)
    zf = zip(footer_left, footer_center, footer_right)
    footer = [next((x for x in iter([l, c, r]) if x != " "), " ") for (l, c, r) in zf]
    footer = "".join(footer)
    print(" " * 6 + footer)
    print()


def array2txt(a):
    a = a.astype(str)
    lines = ["".join(row) for row in a]
    txt = "\n".join(lines)
    return txt


def zrange(*args):
    if len(args) == 1:
        start = 0
        (stop,) = args
        step = 1 + 1j
    elif len(args) == 2:
        start, stop = args
        step = 1 + 1j
    elif len(args) == 3:
        start, stop, step = args
    else:
        raise TypeError(f"zrange expected 1-3 arguments, got {len(args)}")
    xs = range(int(start.real), int(stop.real), int(step.real))
    ys = range(int(start.imag), int(stop.imag), int(step.imag))
    return [complex(x, y) for y in ys for x in xs]
