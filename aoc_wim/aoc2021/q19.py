"""
--- Day 19: Beacon Scanner ---
https://adventofcode.com/2021/day/19
"""
from aocd import data
from parse import parse
import numpy as np
from itertools import combinations
import heapq
import networkx as nx
from scipy.spatial.transform import Rotation as R

Rx = R.from_rotvec([np.pi/2, 0, 0]).as_matrix().astype(int)
Ry = R.from_rotvec([0, np.pi/2, 0]).as_matrix().astype(int)
Rz = R.from_rotvec([0, 0, np.pi/2]).as_matrix().astype(int)
T6 = [np.eye(3, dtype=int)]
for _ in range(3):
    T6.append(np.dot(T6[-1], Rz))
T6.append(Ry)
T6.append(np.linalg.inv(Ry).astype(int))
Ts = []
for T in T6:
    Ts.append(T)
    for _ in range(3):
        Ts.append(np.dot(Ts[-1], Rx))


class Scanner:

    graph = nx.Graph()

    def __init__(self, id, beacons):
        self.id = id
        self.beacons = beacons
        self.transformed = [np.dot(beacons, T) for T in Ts]
        # set of distances between pairs of beacons - this should be invariant under
        # rotations and translations, allows to pair scanners with unknown orientations
        # self.fingerprint = {tuple(abs(x - y)) for x, y in combinations(beacons.T, 2)}
        self.fingerprint = {tuple(sorted(abs(x - y))) for x, y in combinations(beacons, 2)}
        self.transforms = {
            # beacon_id: pose, offset
            self.id: (np.eye(3, dtype=int), np.zeros(3, dtype=int)),
        }

    def __and__(self, other):
        """returns the number of beacons in common (if >= 12, None otherwise)"""
        if not isinstance(other, Scanner):
            return NotImplemented
        for i, other_beacons in enumerate(other.transformed):
            for other_beacon in other_beacons:
                for self_beacon in self.beacons:
                    dt = self_beacon - other_beacon
                    n = len({tuple(b) for b in self.beacons} & {tuple(b) for b in (other_beacons + dt)})
                    assert n >= 1
                    if n >= 12:
                        print(f"scanner {self.id} & {other.id}: {n} common beacons, offset={dt.tolist()}, pose={Ts[i].tolist()}")
                        self.transforms[other.id] = Ts[i], np.dot(Ts[i], -dt)
                        other.transforms[self.id] = np.linalg.inv(Ts[i]).astype(int), dt
                        Scanner.graph.add_edge(self.id, other.id)
                        return n


scanners = {}
for chunk in data.split("\n\n"):
    header, *lines = chunk.splitlines()
    [i] = parse("--- scanner {:d} ---", header).fixed
    numbers = sorted(parse("{:d},{:d},{:d}", line).fixed for line in lines)
    scanner = Scanner(id=i, beacons=np.array(numbers))
    scanners[i] = scanner
    Scanner.graph.add_node(i)

pq = []
for i, (s1, s2) in enumerate(combinations(scanners.values(), 2)):
    # queue pairs of scanners in order of how well their fingerprints matched
    n = len(s1.fingerprint & s2.fingerprint)
    if n >= 12:
        heapq.heappush(pq, (-n, i, s1, s2))
while pq:
    _, _, s1, s2 = heapq.heappop(pq)
    n = s1 & s2
    if n is not None:
        if [*nx.connected_components(Scanner.graph)] == [scanners.keys()]:
            # graph is completely connected: the beacons detected by each scanner may
            # now be transformed into the coordinate system of any other scanner
            break

global_beacons = set()
for i, scanner in scanners.items():
    # transform beacons from this scanner into coordinate system of scanner0
    # note: t0 will also represent this scanner position relative to scanner0
    path = nx.shortest_path(Scanner.graph, scanner.id, 0)
    assert path[0] == i and path[-1] == 0
    beacons = scanner.beacons
    t0 = np.array([0, 0, 0])
    for id0, id1 in zip(path, path[1:]):
        T, dt = scanners[id1].transforms[id0]
        beacons = np.dot(beacons - dt, T)
        t0 = np.dot(t0 - dt, T)
    global_beacons.update({tuple(b) for b in beacons})
    scanner.t0 = t0

print("part a:", len(global_beacons))
print("part b:", max(abs(s0.t0 - s1.t0).sum() for s0, s1 in combinations(scanners.values(), 2)))
