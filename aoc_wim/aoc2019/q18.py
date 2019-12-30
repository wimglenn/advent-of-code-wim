from aocd import data
from aoc_wim.zgrid import ZGrid
from aoc_wim.search import AStar


class Q18AStar(AStar):

    def __init__(self, data):
        self.g = g = ZGrid(data)
        z0 = next(z for z in g.d if g.d[z] == "@")

        g.d[z0] = "#"
        g.d[z0+1] = "#"
        g.d[z0-1] = "#"
        g.d[z0+1j] = "#"
        g.d[z0-1j] = "#"
        g.d[z0 -1 - 1j] = "@"
        g.d[z0 +1 - 1j] = "@"
        g.d[z0 -1 + 1j] = "@"
        g.d[z0 +1 + 1j] = "@"

        self.keyorder = "mlrpoheqcwdsnfgxivkajtyubz"
        z0s = tuple(z for z in g.d if g.d[z] == "@")
        self.keyfinder = {}
        for z, c in g.d.items():
            if c in self.keyorder:
                i = min(range(len(z0s)), key=lambda i: abs(z - z0s[i]))
                self.keyfinder[c] = i

        # bot positions, keys collected, who is allowed to move
        state0 = z0s, "", 0
        AStar.__init__(self, state0, target=None)

    def adjacent(self, state):
        z0s, keys, i = state
        z0 = z0s[i]
        for dz in [-1j, 1, 1j, -1]:
            z = z0 + dz
            v = self.g.d.get(z)
            if v in ".@":
                z0s_ = z0s[:i] + (z,) + z0s[i + 1:]
                yield z0s_, keys, i
            elif v in self.keyorder:
                if v in keys:
                    z0s_ = z0s[:i] + (z,) + z0s[i + 1:]
                    yield z0s_, keys, i
                else:
                    if v != self.keyorder[len(keys)]:
                        continue
                    z0s_ = z0s[:i] + (z,) + z0s[i + 1:]
                    newkeys = keys + v
                    try:
                        newi = self.keyfinder[self.keyorder[len(newkeys)]]
                    except IndexError:
                        newi = i
                    yield z0s_, newkeys, newi
            elif v in self.keyorder.upper():
                if v.lower() in keys:
                    z0s_ = z0s[:i] + (z,) + z0s[i + 1:]
                    yield z0s_, keys, i

    def target_reached(self, current_state, target):
        zs, keys, i = current_state
        return keys == self.keyorder


4248
1878

astar = Q18AStar(data)
astar.run()
print(astar.path_length)
