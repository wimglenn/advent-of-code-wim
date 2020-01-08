from aocd import data
from aoc_wim.zgrid import ZGrid
from aoc_wim.search import AStar
from bidict import bidict
import string
import numpy as np



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


grid = ZGrid(data, on=".", off="#")
h, w = np.array(grid).shape
dzs = [-1j, 1, 1j, -1]

# parse the warps
outside = {}
inside = {}
for z, glyph in grid.items():
    if glyph in string.ascii_uppercase:
        for dz in dzs:
            if grid.get(z + dz) == ".":
                zp = z + dz  # actual position of portal
                name = glyph + grid.get(z - dz)  # add other letter
                if 3 < z.real < w - 3 and 3 < z.imag < h - 3:
                    side = inside
                else:
                    side = outside
                if zp - z in {1j, 1}:
                    name = name[::-1]  # reverse the label
                side[name] = zp
                break

state0 = outside.pop("AA")
target = outside.pop("ZZ")
assert outside.keys() == inside.keys()
warps = bidict({v: outside[k] for k, v in inside.items()})


class Q20AStar(AStar):

    def __init__(self, part="a"):
        self.d_level = 1 if part == "b" else 0
        AStar.__init__(self, (state0, 0), (target, 0))

    def adjacent(self, state):
        z0, level = state
        if z0 in warps:
            yield warps[z0], level + self.d_level
        if z0 in warps.inv:
            if level > 0 or self.d_level == 0:
                yield warps.inv[z0], level - self.d_level
        for dz in dzs:
            z = z0 + dz
            if grid.get(z) == ".":
                yield z, level

astar = Q20AStar(part="a")
astar.run()
print(astar.path_length)

astar = Q20AStar(part="b")
astar.run()
print(astar.path_length)
