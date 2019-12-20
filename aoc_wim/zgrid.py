import string
from collections import ChainMap
from bidict import bidict
import numpy as np


class ZGrid:

    dzs = bidict(zip("^>v<", [-1j, 1, 1j, -1]))

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

    def __contains__(self, item):
        return item in self.d

    def draw(self, overlay=None, clear=False, pretty=True):
        d = self.d
        if overlay is not None:
            d = {**self.d, **overlay}
        dump_grid(d, clear=clear, pretty=pretty)

    def translate(self, table):
        for z in self.d:
            if self.d[z] in table:
                self.d[z] = table[self.d[z]]

    def __array__(self):
        zs = np.array(list(self.d))
        xs = zs.real.astype(int)
        ys = zs.imag.astype(int)
        vs = np.array(list(self.d.values()))
        w = xs.ptp() + 1
        h = ys.ptp() + 1
        full = np.full((h, w), fill_value=self.off, dtype=vs.dtype)
        full[ys - ys.min(), xs - xs.min()] = vs
        return full


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
