class HexGrid:

    def __init__(self, d=None):
        if d is None:
            d = {}
        self.d = d

    @staticmethod
    def _normalize(h):
        m = min(h)
        return h[0] - m, h[1] - m, h[2] - m

    def near(self, h):
        x, y, z = h
        adjacent = (
            (x+1, y, z),
            (x-1, y, z),
            (x, y+1, z),
            (x, y-1, z),
            (x, y, z+1),
            (x, y, z-1),
        )
        adjacent = [self._normalize(a) for a in adjacent]
        return adjacent

    def count_near(self, h0, val, *, include_h0=False, default=None):
        vals = [self.get(h, default) for h in self.near(h0)]
        result = vals.count(val)
        if include_h0:
            result += self.get(h0, default) == val
        return result

    def get(self, h, default=None):
        h = self._normalize(h)
        return self.d.get(h, default)

    def __contains__(self, h):
        h = self._normalize(h)
        return h in self.d

    def __getitem__(self, h):
        h = self._normalize(h)
        return self.d[h]

    def __setitem__(self, h, val):
        h = self._normalize(h)
        self.d[h] = val

    def items(self):
        return self.d.items()

    def values(self):
        return self.d.values()

    def update(self, other):
        self.d.update(other)

    def count(self, val):
        return sum([v == val for v in self.values()])
