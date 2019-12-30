from aocd import data, submit
from aoc_wim.zgrid import ZGrid
from aoc_wim.search import AStar
import string
from bidict import bidict


test_data = """\
                   A               
                   A               
  #################.#############  
  #.#...#...................#.#.#  
  #.#.#.###.###.###.#########.#.#  
  #.#.#.......#...#.....#.#.#...#  
  #.#########.###.#####.#.#.###.#  
  #.............#.#.....#.......#  
  ###.###########.###.#####.#.#.#  
  #.....#        A   C    #.#.#.#  
  #######        S   P    #####.#  
  #.#...#                 #......VT
  #.#.#.#                 #.#####  
  #...#.#               YN....#.#  
  #.###.#                 #####.#  
DI....#.#                 #.....#  
  #####.#                 #.###.#  
ZZ......#               QG....#..AS
  ###.###                 #######  
JO..#.#.#                 #.....#  
  #.#.#.#                 ###.#.#  
  #...#..DI             BU....#..LF
  #####.#                 #.#####  
YN......#               VT..#....QG
  #.###.#                 #.###.#  
  #.#...#                 #.....#  
  ###.###    J L     J    #.#.###  
  #.....#    O F     P    #.#...#  
  #.###.#####.#.#####.#####.###.#  
  #...#.#.#...#.....#.....#.#...#  
  #.#####.###.###.#.#.#########.#  
  #...#.#.....#...#.#.#.#.....#.#  
  #.###.#####.###.###.#.#.#######  
  #.#.........#...#.............#  
  #########.###.###.#############  
           B   J   C               
           U   P   P               """


test_data = """\
             Z L X W       C                 
             Z P Q B       K                 
  ###########.#.#.#.#######.###############  
  #...#.......#.#.......#.#.......#.#.#...#  
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  
  #.#...#.#.#...#.#.#...#...#...#.#.......#  
  #.###.#######.###.###.#.###.###.#.#######  
  #...#.......#.#...#...#.............#...#  
  #.#########.#######.#.#######.#######.###  
  #...#.#    F       R I       Z    #.#.#.#  
  #.###.#    D       E C       H    #.#.#.#  
  #.#...#                           #...#.#  
  #.###.#                           #.###.#  
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#  
CJ......#                           #.....#  
  #######                           #######  
  #.#....CK                         #......IC
  #.###.#                           #.###.#  
  #.....#                           #...#.#  
  ###.###                           #.#.#.#  
XF....#.#                         RF..#.#.#  
  #####.#                           #######  
  #......CJ                       NM..#...#  
  ###.#.#                           #.###.#  
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#  
  #.....#        F   Q       P      #.#.#.#  
  ###.###########.###.#######.#########.###  
  #.....#...#.....#.......#...#.....#.#...#  
  #####.#.###.#######.#######.###.###.#.#.#  
  #.......#.......#.#.#.#.#...#...#...#.#.#  
  #####.###.#####.#.#.#.#.###.###.#.###.###  
  #.......#.....#.#...#...............#...#  
  #############.#.#.###.###################  
               A O F   N                     
               A A D   M                     """

# data = test_data
grid = ZGrid(data)



dzs = [-1j, 1, 1j, -1]

portals = {}
for pos, c in grid.d.items():
    if c in string.ascii_uppercase:
        z0 = None
        for dz in dzs:
            z = pos + dz
            if grid.d.get(z) == ".":
                z0 = z
            if grid.d.get(z, ".") in string.ascii_uppercase:
                pos2 = z
                c2 = grid.d.get(z)
        if z0 is None:
            continue
        if pos.real < pos2.real:
            name = c + c2
        elif pos.imag < pos2.imag:
            name = c + c2
        else:
            name = c2 + c
        if name not in portals:
            portals[name] = []
        portals[name].append(z0)


warps = bidict()
for name, vals in portals.items():
    if len(vals) == 2:
        z0, z1 = vals
        warps[z0] = z1
    elif name == "AA":
        [state0] = vals
    elif name == "ZZ":
        [target] = vals
        # target -= 1j

import numpy as np
h, w = np.array(grid).shape
h //= 2
w //= 2
warps2 = bidict()
for z0, z1 in warps.items():
    z_in, z_out = sorted([z0, z1], key=lambda x: abs(x-(w+h*1j)))
    warps2[z_in] = z_out

warps = warps2

d = grid.d

class Q20AStar(AStar):

    def __init__(self):
        AStar.__init__(self, (state0, 0), (target, 0))

    def adjacent(self, state):
        z0, level = state
        if z0 in warps:
            print("warp", z0, warps[z0])
            yield warps[z0], level + 1
        if z0 in warps.inv:
            print("warp_inv", z0, warps.inv[z0])
            if level > 0:
                yield warps.inv[z0], level - 1
        for dz in dzs:
            z = z0 + dz
            if d.get(z) == ".":
                # print(z0, z)
                yield z, level

    # def heuristic(self, state0, state1):
    #     pass

astar = Q20AStar()
astar.run()
print(astar.path_length)
submit((astar.path_length))

