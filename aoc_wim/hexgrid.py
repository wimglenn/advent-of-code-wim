# See https://www.redblobgames.com/grids/hexagons/


class HexError(Exception):
    pass


class HexPos:

    def __init__(self, x, y, z=None):
        if z is None:
            z = -y - x
        if x + y + z != 0:
            raise HexError("cube coordinates must sum to zero")
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def from_steps(cls, steps, reorient=False):
        if reorient:
            # rotate to convert convert pointy topped hexagon orientation into flat topped
            # (flat topped is better for ascii drawing)
            # see https://www.redblobgames.com/grids/hexagons/#basics
            rot = {
                "nw": "n",
                "w": "nw",
                "sw": "sw",
                "se": "s",
                "e": "se",
                "ne": "ne",
            }
            steps = [rot[s] for s in steps]
        return sum(dhs[s] for s in steps)

    def __add__(self, other):
        if not isinstance(other, HexPos):
            if other == 0:
                return self
            return NotImplemented
        return HexPos(self.x + other.x, self.y + other.y, self.z + other.z)

    __radd__ = __add__

    def __sub__(self, other):
        if not isinstance(other, HexPos):
            if other == 0:
                return self
            return NotImplemented
        return HexPos(self.x - other.x, self.y - other.y, self.z - other.z)

    def __pos__(self):
        return self

    def __neg__(self):
        return HexPos(-self.x, -self.y, -self.z)

    def __repr__(self):
        return f"HexPos({self.x}, {self.y}, {self.z})"

    def __mul__(self, other):
        if not isinstance(other, int):
            return NotImplemented
        return HexPos(other * self.x, other * self.y, other * self.z)

    __rmul__ = __mul__

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __iter__(self):
        return iter((self.x, self.y, self.z))

    def __eq__(self, other):
        if not isinstance(other, HexPos):
            return NotImplemented
        return (self.x, self.y, self.z) == (other.x, other.y, other.z)


# See https://www.redblobgames.com/grids/hexagons/#coordinates-cube
n  = HexPos( 0,  1, -1)
ne = HexPos( 1,  0, -1)
nw = HexPos(-1,  1,  0)
se = -nw
sw = -ne
s  = -n


dhs = {
    "n": n,
    "ne": ne,
    "nw": nw,
    "se": se,
    "sw": sw,
    "s": s,
}


def dist(h, h0=HexPos(0, 0, 0)):
    # See https://www.redblobgames.com/grids/hexagons/#distances-cube
    dh = h - h0
    d2 = abs(dh.x) + abs(dh.y) + abs(dh.z)
    return d2 // 2


class HexGrid:

    def __init__(self, d=None):
        if d is None:
            d = {}
        self.d = d

    def near(self, h):
        return [h + dh for dh in (nw, n, ne, se, s, sw)]

    def count_near(self, h0, val, *, include_h0=False, default=None):
        vals = [self.get(h, default) for h in self.near(h0)]
        result = vals.count(val)
        if include_h0:
            result += self.get(h0, default) == val
        return result

    def get(self, h, default=None):
        return self.d.get(h, default)

    def __contains__(self, h):
        return h in self.d

    def __getitem__(self, h):
        return self.d[h]

    def __setitem__(self, h, val):
        self.d[h] = val

    def items(self):
        return self.d.items()

    def values(self):
        return self.d.values()

    def update(self, other):
        self.d.update(other)

    def count(self, val):
        return sum([v == val for v in self.values()])
