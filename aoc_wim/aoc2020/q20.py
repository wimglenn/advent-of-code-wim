"""
--- Day 20: Jurassic Jigsaw ---
https://adventofcode.com/2020/day/20
"""
import math
from aocd import data
from aoc_wim.zgrid import ZGrid
import networkx as nx
import numpy as np
from parse import parse
from itertools import combinations


class Tile:
    def __init__(self, id, data):
        self.id = id
        self.data = data
        self.angle = 0
        self.flip = False

    @property
    def edges(self):
        U = self.data[0]
        D = self.data[-1]
        L = self.data[:,0]
        R = self.data[:,-1]
        return {(*edge,) for edge in (U, D, L, R)}

    def fits_with(self, other):
        return any({e, e[::-1]} & self.edges for e in other.edges)

    def transform(self):
        self.data = np.rot90(self.data)
        self.angle += 90
        if self.angle == 360:
            self.angle = 0
            self.data = np.flipud(self.data)
            self.flip = not self.flip

    def orient_to_left(self, other):
        # line up the left edge of this tile with the right edge of other
        edge = other.data[:, -1]
        for i in range(8):
            if (self.data[:, 0] == edge).all():
                return True
            self.transform()
        return False

    def orient_to_above(self, other):
        # line up the top edge of this tile with the bottom edge of other
        other.data = np.rot90(other.data)
        ok = self.orient_to_left(other)
        other.data = np.rot90(other.data, -1)
        self.data = np.rot90(self.data, -1)
        if ok:
            assert (self.data[0] == other.data[-1]).all()
        return ok

    def trimmed(self):
        return self.data[1:-1, 1:-1]


tiles_raw = data.split("\n\n")
tiles = {}
for tile in tiles_raw:
    pre, tile = tile.split("\n", 1)
    tile_id, = parse("Tile {:d}:", pre).fixed
    A = np.array([[*r] for r in tile.splitlines()])
    A = (A == "#").astype(int)
    tiles[tile_id] = Tile(tile_id, A)

g = nx.Graph()
for t0, t1 in combinations(tiles.values(), 2):
    if t0.fits_with(t1):
        g.add_edge(t0, t1)

corners = {t.id for t in tiles.values() if len(list(g.neighbors(t))) == 2}
a = math.prod(corners)
print("part a:", a)

# start joining from any old corner
corner_id = corners.pop()
tile00 = tiles.pop(corner_id)
# corner tiles should have two neighbors
x, y = g.neighbors(tile00)
# orient first corner so that it fits top-left
# keep poking the tile until the top and left edges can't match with neighbors
while True:
    top = (*tile00.data[0],)
    left = (*tile00.data[:,0],)
    both = {top, left, top[::-1], left[::-1]}
    if not both & (x.edges | y.edges):
        break
    tile00.transform()

n = math.isqrt(len(g))  # we have n*n square of tiles
grid = {(0,0): tile00}
for c in range(1, n):
    left = grid[0, c-1]
    for tile in {*g.neighbors(left)}.intersection(tiles.values()):
        if tile.orient_to_left(left):
            grid[0,c] = tile
            del tiles[tile.id]
            break
for r in range(1, n):
    for c in range(n):
        above = grid[r-1,c]
        for tile in {*g.neighbors(above)}.intersection(tiles.values()):
            if tile.orient_to_above(above):
                grid[r,c] = tile
                del tiles[tile.id]
                break

full_rows = [np.hstack([grid[r, c].trimmed() for c in range(n)]) for r in range(n)]
full_grid = np.vstack(full_rows)
big_tile = Tile(0, full_grid)

sea_monster_raw = """\
                  #
#    ##    ##    ###
 #  #  #  #  #  #
"""
sea_monster = (np.array(ZGrid(sea_monster_raw)) == "#").astype(int)
n = sea_monster.sum()
h, w = sea_monster.shape
H, W = big_tile.data.shape

n_monsters = 0
while n_monsters <= 0:
    big_tile.transform()
    n_monsters = 0
    for row in range(H - h):
        for col in range(W - w):
            section = big_tile.data[row:row + h, col:col + w]
            if (sea_monster * section).sum() == n:
                n_monsters += 1

print("part b:", big_tile.data.sum() - n_monsters * sea_monster.sum())
