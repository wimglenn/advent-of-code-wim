import numpy as np
from termcolor import cprint
from aoc_wim.zgrid import ZGrid
from aoc_wim.zgrid import array2txt


glyphs = """
.##.
#..#
#..#
####
#..#
#..#


..##..
.#..#.
#....#
#....#
#....#
######
#....#
#....#
#....#
#....#


###.
#..#
###.
#..#
#..#
###.


#####.
#....#
#....#
#....#
#####.
#....#
#....#
#....#
#....#
#####.


.##.
#..#
#...
#...
#..#
.##.


.####.
#....#
#.....
#.....
#.....
#.....
#.....
#.....
#....#
.####.


####
#...
###.
#...
#...
####


######
#.....
#.....
#.....
#####.
#.....
#.....
#.....
#.....
######


####
#...
###.
#...
#...
#...


######
#.....
#.....
#.....
#####.
#.....
#.....
#.....
#.....
#.....


.##.
#..#
#...
#.##
#..#
.###


.####.
#....#
#.....
#.....
#.....
#..###
#....#
#....#
#...##
.###.#


#..#
#..#
####
#..#
#..#
#..#


#....#
#....#
#....#
#....#
######
#....#
#....#
#....#
#....#
#....#


#...#
#...#
#...#
#####
#...#
#...#
#...#
#...#


###
.#.
.#.
.#.
.#.
###


###
.#.
.#.
.#.
.#.
.#.
.#.
###


..##
...#
...#
...#
#..#
.##.


...###
....#.
....#.
....#.
....#.
....#.
....#.
#...#.
#...#.
.###..


#....#
#...#.
#..#..
#.#...
##....
##....
#.#...
#..#..
#...#.
#....#


#..#
#.#.
##..
#.#.
#.#.
#..#


#...
#...
#...
#...
#...
####


#.....
#.....
#.....
#.....
#.....
#.....
#.....
#.....
#.....
######


#....#
##...#
##...#
#.#..#
#.#..#
#..#.#
#..#.#
#...##
#...##
#....#


.##.
#..#
#..#
#..#
#..#
.##.


###.
#..#
#..#
###.
#...
#...


#####.
#....#
#....#
#....#
#####.
#.....
#.....
#.....
#.....
#.....


###.
#..#
#..#
###.
#.#.
#..#


#####.
#....#
#....#
#....#
#####.
#..#..
#...#.
#...#.
#....#
#....#


.###
#...
#...
.##.
...#
###.


#..#
#..#
#..#
#..#
#..#
.##.


#....#
#....#
.#..#.
.#..#.
..##..
..##..
.#..#.
.#..#.
#....#
#....#


####
...#
..#.
.#..
#...
####


######
.....#
.....#
....#.
...#..
..#...
.#....
#.....
#.....
######


#####
#...#
#...#
#...#
#####
"""


glyphs = {g: np.array(ZGrid(g)) == "#" for g in glyphs.strip().split("\n\n\n")}
known = dict(zip(glyphs, "AABBCCEEFFGGHHHIIJJKKLLNOPPRRSUXZZ□"))
known[""] = ""

day10_2022_expected_example_render = """
##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....
"""
known[day10_2022_expected_example_render.strip()] = "CRT"


def autocrop(A):
    if A.dtype != int:
        cropped = autocrop((A == "#").astype(int))
        return np.where(cropped, "#", ".")
    on = np.argwhere(A)
    if not on.size:
        return A[:0, :0]
    r0, c0 = on.min(axis=0)
    r1, c1 = on.max(axis=0) + 1
    return A[r0:r1, c0:c1]


class DebugDict(dict):
    def __getitem__(self, item):
        if isinstance(item, np.ndarray) and item.ndim == 2:
            if item.dtype == "U1":
                item = (item == "#").astype(int)
            item = autocrop(item)
            txt = array2txt(item).replace("0", ".").replace("1", "#")
            if txt in known:
                return known[txt]
            H, W = item.shape
            for k, v in glyphs.items():
                h, w = v.shape
                if h == H and (item[:, :w] == v).all():
                    letter = known[k]
                    return letter + self.__getitem__(item[:, w:])
            item = txt  # trigger fallthrough to __missing__
        if isinstance(item, (dict, ZGrid)):
            grid = ZGrid(item)
            grid.translate({grid.off: 0, grid.on: 1})
            full = np.array(grid)
            full = autocrop(full)
            return self.__getitem__(full)
        if isinstance(item, np.ndarray):
            self.__missing__(array2txt(item))
        return super(DebugDict, self).__getitem__(item)

    def __missing__(self, key):
        cprint("AOCR does not understand this item:", color="red")
        print(key)
        cprint("Identify it and add to {}".format(__file__), color="red")
        raise KeyError(key)


AOCR = DebugDict(known)
