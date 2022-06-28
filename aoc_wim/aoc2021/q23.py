"""
--- Day 23: Amphipod ---
https://adventofcode.com/2021/day/23
"""
from aocd import data
from aoc_wim.search import AStar
import networkx as nx
from aoc_wim.zgrid import ZGrid
from aoc_wim.zgrid import manhattan_distance


class Q23AStar(AStar):
    def __init__(self, data):
        grid = ZGrid(data, on=".", off="#")
        graph = grid.graph(extra="ABCD")
        hall = self.hall = [z for z in graph if z.imag == 1]
        rooms = self.rooms = [z for z in graph if z.imag != 1]
        # Amphipods will never stop on the space immediately outside any room
        hall[:] = [z for z in hall if z + ZGrid.down not in rooms]
        obstructions = self.obstructions = {}
        for r in rooms:
            for h in hall:
                path = nx.shortest_path(graph, r, h)
                assert path[0] == r
                assert path[-1] == h
                assert len(path) == manhattan_distance(r, h) + 1
                obs = [z for z in path[1:-1] if z in rooms + hall]
                obstructions[r, h] = obstructions[h, r] = frozenset(obs)

        state0 = {c: [] for c in "ABCD"}
        for z, glyph in grid.items():
            if glyph in "ABCD":
                state0[glyph].append(z)
        state0 = tuple(frozenset(v) for v in state0.values())
        target = tuple(frozenset(rooms[i::4]) for i in range(4))
        AStar.__init__(self, state0, target)

    def adjacent(self, state):
        occupied = frozenset.union(*state)
        for i, ps in enumerate(state):
            target_rooms = self.rooms[i::4]
            for p in ps:
                if p.imag != 1:
                    # amphipod is in a side room
                    if p in target_rooms:
                        t = target_rooms.index(p)
                        others = frozenset(target_rooms[t:])
                        if others <= ps:
                            # this amphipod is already home - it shouldn't move again
                            continue
                    # it can move into a hallway position if not obstructed
                    for h in self.hall:
                        if h not in occupied:
                            if not self.obstructions[h, p].intersection(occupied):
                                new_ps = ps - {p} | {h}
                                yield *state[:i], new_ps, *state[i + 1 :]
                else:
                    # amphipod is in hallway
                    # it can move into target room if unobstructed
                    for j, t in enumerate(target_rooms):
                        if t not in occupied:
                            if ps.issuperset(target_rooms[j + 1 :]):
                                if not self.obstructions[p, t].intersection(occupied):
                                    new_ps = ps - {p} | {t}
                                    yield *state[:i], new_ps, *state[i + 1 :]
                                    break

    def cost(self, current_state, next_state):
        # find who has moved
        for g, s0, s1 in zip("ABCD", current_state, next_state):
            diff = s0 ^ s1
            if diff:
                return manhattan_distance(*diff) * 10 ** "ABCD".index(g)
        return 0


def render(state):
    g = ZGrid(data, transform=dict.fromkeys("ABCD", "."))
    overlay = {z: g for g, zs in zip("ABCD", state) for z in zs}
    g.draw(overlay=overlay)


def total_energy(data):
    astar = Q23AStar(data)
    astar.run()
    return astar.gscore[astar.target]


print("part a:", total_energy(data))
extra = """\
  #D#C#B#A#
  #D#B#A#C#
"""
lines = data.splitlines()
data = "\n".join(lines[:-2] + extra.splitlines() + lines[-2:])
print("part b:", total_energy(data))
