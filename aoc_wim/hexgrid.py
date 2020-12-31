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
o  = HexPos(0,  0,  0)
nw = HexPos(0,  1, -1)
ne = HexPos(1,  0, -1)
e  = HexPos(1, -1,  0)
sw = -ne
se = -nw
w  = -e


class HexGrid:

    def __init__(self, d=None):
        if d is None:
            d = {}
        self.d = d

    def near(self, h):
        return [h + dh for dh in (nw, ne, e, se, sw, w)]

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
