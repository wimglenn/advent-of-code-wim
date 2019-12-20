from collections import Counter
import numpy as np
from termcolor import cprint
from aoc_wim.zgrid import ZGrid
from aoc_wim.zgrid import array2txt


glyphs = """
.##..
#..#.
#..#.
####.
#..#.
#..#.


...##...
..#..#..
.#....#.
.#....#.
.#....#.
.######.
.#....#.
.#....#.
.#....#.
.#....#.


###..
#..#.
###..
#..#.
#..#.
###..


.#####..
.#....#.
.#....#.
.#....#.
.#####..
.#....#.
.#....#.
.#....#.
.#....#.
.#####..


.##..
#..#.
#....
#....
#..#.
.##..


..####..
.#....#.
.#......
.#......
.#......
.#......
.#......
.#......
.#....#.
..####..


####.
#....
###..
#....
#....
####.


.######.
.#......
.#......
.#......
.#####..
.#......
.#......
.#......
.#......
.######.


####.
#....
###..
#....
#....
#....


.######.
.#......
.#......
.#......
.#####..
.#......
.#......
.#......
.#......
.#......


.##..
#..#.
#....
#.##.
#..#.
.###.


..####..
.#....#.
.#......
.#......
.#......
.#..###.
.#....#.
.#....#.
.#...##.
..###.#.


#..#.
#..#.
####.
#..#.
#..#.
#..#.


.#....#.
.#....#.
.#....#.
.#....#.
.######.
.#....#.
.#....#.
.#....#.
.#....#.
.#....#.


.#...#.
.#...#.
.#...#.
.#####.
.#...#.
.#...#.
.#...#.
.#...#.


.###.
..#..
..#..
..#..
..#..
.###.


.###...
..#....
..#....
..#....
..#....
..#....
..#....
.###...


..##.
...#.
...#.
...#.
#..#.
.##..


....###.
.....#..
.....#..
.....#..
.....#..
.....#..
.....#..
.#...#..
.#...#..
..###...


.#....#.
.#...#..
.#..#...
.#.#....
.##.....
.##.....
.#.#....
.#..#...
.#...#..
.#....#.


#..#.
#.#..
##...
#.#..
#.#..
#..#.


#....
#....
#....
#....
#....
####.


.#......
.#......
.#......
.#......
.#......
.#......
.#......
.#......
.#......
.######.


.#....#.
.##...#.
.##...#.
.#.#..#.
.#.#..#.
.#..#.#.
.#..#.#.
.#...##.
.#...##.
.#....#.


.##..
#..#.
#..#.
#..#.
#..#.
.##..


###..
#..#.
#..#.
###..
#....
#....


.#####..
.#....#.
.#....#.
.#....#.
.#####..
.#......
.#......
.#......
.#......
.#......


###..
#..#.
#..#.
###..
#.#..
#..#.


.#####..
.#....#.
.#....#.
.#....#.
.#####..
.#..#...
.#...#..
.#...#..
.#....#.
.#....#.


.###.
#....
#....
.##..
...#.
###..


#..#.
#..#.
#..#.
#..#.
#..#.
.##..


.#....#.
.#....#.
..#..#..
..#..#..
...##...
...##...
..#..#..
..#..#..
.#....#.
.#....#.


####.
...#.
..#..
.#...
#....
####.


.######.
......#.
......#.
.....#..
....#...
...#....
..#.....
.#......
.#......
.######.
"""


glyphs = glyphs.strip().split("\n\n\n")
known = dict(zip(glyphs, "AABBCCEEFFGGHHHIIJJKKLLNOPPRRSUXZZ"))
known_dims = Counter()  # (height, width): count
for glyph in glyphs:
    lines = glyph.splitlines()
    [w] = {len(x) for x in lines}
    h = len(lines)
    known_dims[(h, w)] += 1


class DebugDict(dict):
    def __getitem__(self, item):
        if isinstance(item, np.ndarray) and item.ndim == 2:
            H, W = item.shape
            if (H, W) in known_dims:
                # looking for just one letter in a numpy array
                if item.dtype.name.startswith("int") or item.dtype.name == "bool":
                    item = [["#" if val else "." for val in row] for row in item]
                item = "\n".join(["".join(row) for row in item])
            elif H in {h for (h, w) in known_dims}:
                widths = {w for (h, w) in known_dims if H == h}
                for w in sorted(widths, reverse=True):
                    n, rem = divmod(W, w)
                    if rem == 0:
                        # could be a word? retry OCR per character
                        chars = [item[:, w * i : w * (i + 1)] for i in range(n)]
                        txt = "".join([self[char] for char in chars])
                        return txt
        if isinstance(item, dict):
            grid = ZGrid(item)
            grid.translate({0: ".", 1: "#"})
            full = np.array(grid)
            full = full[:, 1:-2]  # TODO: template matching
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
