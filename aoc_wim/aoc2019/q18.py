"""
--- Day 18: Many-Worlds Interpretation ---
https://adventofcode.com/2019/day/18
"""
import string
from itertools import combinations
from aocd import data
from aoc_wim.zgrid import ZGrid
from aoc_wim.search import AStar
import networkx as nx


class Q18AStar(AStar):

    def __init__(self, data, part="a"):
        grid = ZGrid(data, on=".", off="#")
        pos = ("@",)
        if part == "b":
            [z0] = [z for z, v in grid.items() if v == "@"]
            if grid.count_near(z0, val=".", n=8, default=".") == 8:
                pos = ("@0", "@1", "@2", "@3")
                for z in grid.near(z0, n=5):
                    grid[z] = grid.off
                for p, dz in zip(pos, [-1 - 1j, 1 - 1j,  1 + 1j, -1 + 1j]):
                    grid[z0 + dz] = p
        graph = grid.graph(extra=frozenset(string.ascii_letters).union(pos))
        self.all_keys = {k for k in graph.extra if k in string.ascii_lowercase}

        # map of the other keys that must be acquired before each key is acquired
        self.obstructions = {k: set() for k in self.all_keys}
        # precached distances between points of interest
        self.kdist = {}
        for k0 in self.all_keys:
            for p in pos:
                try:
                    path = nx.shortest_path(graph, graph.extra[p], graph.extra[k0])
                except nx.NetworkXNoPath:
                    pass
                else:
                    break
            else:
                raise Exception("nothing possible to do")
            self.kdist[k0, p] = self.kdist[p, k0] = len(path) - 1
            assert path[0] == graph.extra[p]
            assert path[-1] == graph.extra[k0]
            for p in path[1:-1]:
                if p in graph.extra.values():
                    k1 = grid[p].lower()
                    self.obstructions[k0].add(k1)

        for k1, k2 in combinations(self.all_keys, 2):
            z1 = graph.extra[k1]
            z2 = graph.extra[k2]
            try:
                d = nx.shortest_path_length(graph, z1, z2)
            except nx.NetworkXNoPath:
                continue
            self.kdist[k1, k2] = self.kdist[k2, k1] = d

        state0 = pos, frozenset()
        AStar.__init__(self, state0, target=None)

    def cost(self, state0, state1):
        if state1 is None:
            return 0
        pos0, keys0 = state0
        pos1, keys1 = state1
        [(k0, k1)] = [(k0, k1) for k0, k1 in zip(pos0, pos1) if k0 != k1]
        return self.kdist[k0, k1]

    heuristic = cost

    def target_reached(self, current_state, target):
        _, keys = current_state
        return keys == self.all_keys

    def adjacent(self, state):
        pos, keys = state
        for i, p in enumerate(pos):
            for key, obstruction in self.obstructions.items():
                if key not in keys and keys >= obstruction and (p, key) in self.kdist:
                    yield pos[:i] + (key,) + pos[i+1:], keys.union(key)


astar = Q18AStar(data, part="a")
path_a = astar.run()
print("part a:", astar.gscore[astar.target])

astar = Q18AStar(data, part="b")
path_b = astar.run()
print("part b:", astar.gscore[astar.target])
