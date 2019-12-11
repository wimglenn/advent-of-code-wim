from collections import Counter
import numpy as np
from termcolor import cprint


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
                rows = [["#" if val else "." for val in row] for row in item]
                item = "\n".join(["".join(row) for row in rows])
            elif H in {h for (h, w) in known_dims}:
                widths = {w for (h, w) in known_dims if H == h}
                for w in sorted(widths, reverse=True):
                    n, rem = divmod(W, w)
                    if rem == 0:
                        # could be a word? retry OCR per character
                        chars = [item[:, w * i : w * (i + 1)] for i in range(n)]
                        txt = "".join([self[char] for char in chars])
                        return txt
        if isinstance(item, dict) and {type(k) for k in item} == {complex}:
            # sparse grid
            sparse = np.array([(int(k.imag), int(k.real), v) for k, v in item.items()])
            h, w, _ = sparse.ptp(axis=0)
            full = np.zeros((h + 1, w + 1), dtype=int)
            rows, cols, vals = sparse.T
            full[rows - rows.min(), cols - cols.min()] = vals
            # trim fat from left
            while not full[:, 0].any():
                full = full[:, 1:]
            # trim fat from right
            while not full[:, -2:].any():
                full = full[:, :-1]
            return self.__getitem__(np.flipud(full))
        if isinstance(item, np.ndarray):
            self.__missing__(item)
        return super(DebugDict, self).__getitem__(item)

    def __missing__(self, key):
        cprint("AOCR does not understand this item:", color="red")
        print(key)
        cprint("Identify it and add to {}".format(__file__), color="red")
        raise KeyError(key)


AOCR = DebugDict(known)
