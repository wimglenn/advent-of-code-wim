import logging
import string
from collections import ChainMap
from collections import deque
import numpy as np
import networkx as nx


log = logging.getLogger(__name__)


def manhattan_distance(z1, z0=0):
    dz = z1 - z0
    return abs(int(dz.real)) + abs(int(dz.imag))


def hexagonal_distance(z1, z0=0):
    dz = z1 - z0
    return int(max(abs(dz.real), abs(dz.imag), abs(dz.real - dz.imag)))


class ZDict(dict):

    def __init__(self, func):
        self.func = func

    def __missing__(self, z):
        if not isinstance(z, (int, complex, float)):
            log.error("ZDict does not support key %r", z)
            raise NotImplementedError
        self[z] = self.func(z)
        return self[z]


class ZGrid:

    _dzs = [-1j, 1, 1j, -1]
    dzs = ChainMap(
        dict(zip(_dzs, _dzs)),
        dict(zip("^>v<", _dzs)),
        dict(zip("up right down left".split(), _dzs)),
        dict(zip("up right down left".upper().split(), _dzs)),
        dict(zip("URDL", _dzs)),
        dict(zip("NESW", _dzs)),
    )
    U = N = up = north = -1j
    R = E = right = east = 1
    D = S = down = south = 1j
    L = W = left = west = -1
    UR = NE = N + E
    UL = NW = N + W
    DL = SW = S + W
    DR = SE = S + E

    turn_right = turnR = 1j
    turn_left = turnL = -1j
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
            elif callable(initial_data):
                self.d = ZDict(func=initial_data)
            elif isinstance(initial_data, dict):
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

    def count(self, val):
        return sum([1 for v in self.values() if v == val])

    def count_near(self, z0, val, *, n=4, default=None):
        vals = [self.get(z, default) for z in self.near(z0, n=n)]
        result = vals.count(val)
        return result

    def get(self, k, default=None):
        return self.d.get(k, default)

    def z(self, val, first=True):
        zs = []
        for k, v in self.items():
            if v == val:
                if first:
                    return k
                zs.append(k)
        return zs

    def near(self, z, n=4):
        if n == 4:
            return [
                        z-1j,
                z-1,             z+1,
                        z+1j,
            ]
        if n == 5:
            return [
                        z-1j,
                z-1,    z,       z+1,
                        z+1j,
            ]
        elif n == 6:  # hexgrid w/ skewed coordinate system
            return [
                z-1-1j, z-1j,
                z-1,             z+1,
                        z+1j, z+1+1j,
            ]
        elif n == 7:
            return [
                z-1-1j, z-1j,
                z-1,    z,       z+1,
                        z+1j, z+1+1j,
            ]
        elif n == 8:
            return [
                z-1-1j, z-1j, z+1-1j,
                z-1,             z+1,
                z-1+1j, z+1j, z+1+1j,
            ]
        elif n == 9:
            return [
                z-1-1j, z-1j, z+1-1j,
                z-1,    z,       z+1,
                z-1+1j, z+1j, z+1+1j,
            ]

    def draw(self, overlay=None, window=None, clear=False, pretty=False, transform=None):
        if window is None:
            d = self.d
        else:
            if isinstance(window, complex):
                window = zrange(window + 1 + 1j)
            d = {z: self[z] for z in window}
        if overlay is not None:
            d = {**self.d, **overlay}
        dump_grid(d, clear=clear, pretty=pretty, transform=transform)

    def drawVhex(self, clear=True, side_length=2, labels=False):
        cell = HexCell(side_length)
        plane = Plane()
        label = ""
        for z, val in self.items():
            row, col = transform(z)
            if labels:
                label = f"{col},{row}"
            draw_cell(plane, cell, row, col, val, label=label)
        plane.draw(clear=clear, xscale=cell.dx, yscale=cell.dy, cellwidth=cell.w)
        return plane

    def translate(self, table):
        for z in self.d:
            if self.d[z] in table:
                self.d[z] = table[self.d[z]]

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

    def path(self, z, z0=0):
        g = self.graph()
        return nx.shortest_path(g, z0, z)

    def path_length(self, z, z0=0):
        g = self.graph()
        return nx.shortest_path_length(g, z0, z)

    def draw_path(self, z, z0=0, glyph="x", clear=False, pretty=True):
        path = self.path(z, z0)
        overlay = {}.fromkeys(path, glyph)
        overlay[path[0]] = "O"
        overlay[path[-1]] = "T"
        self.draw(overlay=overlay, clear=clear, pretty=pretty)

    def bfs(self, target=None, z0=0, max_depth=None):
        """returns a dict of connected nodes vs depth up to max_depth"""
        g0 = self[z0]
        if g0 != self.on:
            log.error("Expected initial glyph %r, got %r", self.on, g0)
            raise NotImplementedError
        seen = {}
        queue = deque([(z0, 0)])
        while queue:
            z0, depth = queue.popleft()
            if max_depth is not None and depth > max_depth:
                return seen
            if z0 not in seen:
                seen[z0] = depth
                if target is not None and z0 == target:
                    return seen
                for z in self.near(z0):
                    if z in seen:
                        continue
                    try:
                        g = self[z]
                    except KeyError:
                        continue
                    if g == self.on:
                        queue.append((z, depth + 1))
        return seen

    @property
    def top_left(self):
        return min(self.d, key=lambda z: (z.imag, z.real))

    @property
    def left_bottom(self):
        return min(self.d, key=lambda z: (z.real, -z.imag))

    @property
    def bottom_right(self):
        return max(self.d, key=lambda z: (z.imag, z.real))

    @property
    def right_top(self):
        return max(self.d, key=lambda z: (z.real, -z.imag))

    @property
    def width(self):
        return int(self.right_top.real - self.left_bottom.real) + 1

    @property
    def height(self):
        return int(self.bottom_right.imag - self.top_left.imag) + 1


def dump_grid(g, clear=False, pretty=True, transform=None):
    if transform is None:
        transform = {
            "#": "⬛",
            ".": "  ",
            "O": "🤖",
            "T": "🥇",
            "x": "👣",
            ">": "➡️ ",
            "<": "⬅️ ",
            "^": "⬆️ ",
            "v": "⬇️ ",
            "@": "@️ ",
            0: "  ",
            1: "⬛",
        }
    empty = "."
    if pretty:
        transform.update({x: x + " " for x in string.ascii_letters if x not in transform})
        empty = "  "
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


# axes unit vectors for hexagonal grid with skewed coordinate system - flat-topped
hexV = dict(zip("n ne nw se sw s".split(), ZGrid().near(0, n=6)))

# hexgrid - pointy-topped
hexH = dict(zip("w nw sw ne se e".split(), ZGrid().near(0, n=6)))


def hex_glyph_gen(n):
    #   ⬡ -> ⎔
    #   ⬢ -> ⬣
    if n == 0:
        return "⎔"
    first = " "*n + "__"*n
    last = " "*(n - 1) + "\\" + "__"*n + "/"
    lines = [first, last]
    for i in range(n):
        center = ".."*(n + i)
        left = " "*(n - 1 - i)
        top = left + "/" + center + "\\"
        bottom = left + "\\" + center + "/"
        mid = len(lines) // 2
        lines[mid:mid] = [top, bottom]
    del lines[-2]
    return "\n".join(lines)


class HexCell:

    def __init__(self, glyph, dy=None, dx=None, fill="."):
        if isinstance(glyph, int):
            glyph = hex_glyph_gen(glyph)
        self.glyph = glyph.strip("\n")
        lines = self.glyph.splitlines()
        self.h = len(lines)
        self.w = max([len(x) for x in lines])
        if dy is None:
            for dy, line in enumerate(lines):
                if line.strip().startswith("\\"):
                    dy -= 1
                    break
        self.dy = dy or 1
        if dx is None and len(lines) > 1:
            for dx, char in enumerate(lines[1]):
                if char == "\\":
                    break
        self.dx = dx or 1
        self.blanked = self.glyph.replace(fill, " ")
        if self.glyph == "⬣":
            self.blanked = "⎔"
            self.dx = 2


class Plane:
    """Unbounded 2D rectangular space of values that automatically grows as needed"""
    def __init__(self, left=0, right=0, top=0, bottom=0, fill=" "):
        if left > right or top > bottom:
            raise ValueError(f"invalid initial: {left},{right},{top},{bottom}")
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.lines = {}
        self.fill = fill
        w = self.width
        self.lines = {y: deque([fill]*w) for y in range(self.top, self.bottom + 1)}

    def __getitem__(self, item):
        row, col = item
        col -= self.left
        return self.lines[row][col]

    def __setitem__(self, item, val):
        row, col = item
        while row < self.top:
            self.top -= 1
            self.lines[self.top] = deque([self.fill]*self.width)
        while row > self.bottom:
            self.bottom += 1
            self.lines[self.bottom] = deque([self.fill]*self.width)
        if col < self.left:
            grow = [self.fill] * (self.left - col)
            for line in self.lines.values():
                line.extendleft(grow)
            self.left = col
        if col > self.right:
            grow = [self.fill] * (col - self.right)
            for line in self.lines.values():
                line.extend(grow)
            self.right = col
        col -= self.left
        self.lines[row][col] = val

    @property
    def width(self):
        return self.right - self.left + 1

    @property
    def height(self):
        return self.bottom - self.top + 1

    def draw(self, clear=True, xscale=1, yscale=1, cellwidth=4):
        if clear:
            print("\033c")
        y_pad = max([len(str(r//yscale)) for r in self.lines])
        print(" "*y_pad + "┌" + "─"*self.width + "┐")
        prev_tick = None
        for row in range(self.top, self.bottom + 1):
            line = self.lines[row]
            tick = str(row//yscale)
            if tick == prev_tick:
                # don't write it again
                tick = ""
            else:
                prev_tick = tick
            print(tick.rjust(y_pad) + "│" + "".join(line) + "│")
        print(" "*y_pad + "└" + "─"*self.width + "┘")
        footer = [" "] * self.width
        for i, char in enumerate(str((self.left + cellwidth//2)//xscale)):
            footer[i] = char
        for i, char in enumerate(reversed(str(self.right//xscale))):
            footer[~i] = char
        if self.left <= 0 <= self.right:
            i0 = -self.left - 1
            footer[i0] = "0"
        else:
            mid = self.left + self.width//2
            imid = sorted(self.lines).index(mid)
            mid_label = str(mid)
            imidl = imid - 1
            imidr = imid + len(mid_label) + 1
            if imidl > 0 and footer[imidl] == " ":
                if imidr < len(footer) and footer[imidr] == " ":
                    for char in mid_label:
                        footer[imid] = char
                        imid += 1
        print(" "*(y_pad + 1) + "".join(footer))


def draw_cell(plane, cell, r, c, val=False, label=""):
    glyph = cell.glyph if val else cell.blanked
    r *= cell.dy
    c *= cell.dx
    for i, row in enumerate(glyph.splitlines(), start=-cell.dy):
        for j, char in enumerate(row, start=(-cell.w//2)):
            if char == " ":
                continue
            plane[r + i, c + j] = char
    if label and cell.w > 4:
        c = c - cell.w//2 + 1
        for char in label:
            plane[r, c] = char
            c += 1


def transform(z):
    # change of coordinate system: axial to offset
    #   1  --> (1, 1)
    #   1j --> (1, -1)
    real, imag = int(z.real), int(z.imag)
    row = real + imag
    col = real - imag
    return row, col
