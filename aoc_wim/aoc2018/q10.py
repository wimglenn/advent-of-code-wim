import re
import numpy as np
from aocd import data
from aoc_wim.ocr import AOCR


test_data = """\
position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>"""


def varianceish(a):
    return a.std(axis=1)[:2].sum()


def ocr(a, lettersize):
    ps = a[:2].copy()
    ps -= ps.min(axis=1).reshape(-1, 1)
    W, H = ps.max(axis=1) + 1
    img = np.full((H, W), 0)
    col, row = ps
    img[row, col] = 1
    img = np.pad(img, ((0, 0), (1, 0)), mode="constant", constant_values=0)
    W += 1
    h, w = lettersize
    assert h == H
    while W % w:
        img = np.pad(img, ((0, 0), (0, 1)), mode="constant", constant_values=0)
        W += 1
    return AOCR[img]


def part_ab(data, lettersize=(10, 8)):
    numbers = re.findall(r"-?\d+", data)
    a = np.array(numbers).astype(int).reshape(-1, 4).T
    t = 0
    minv = varianceish(a)
    while True:
        a[:2] += a[2:]
        v = varianceish(a)
        minv = min(v, minv)
        if v > minv:
            a[:2] -= a[2:]  # back up one step
            text = ocr(a, lettersize=lettersize)
            return text, t
        t += 1


assert part_ab(test_data, lettersize=(8, 7)) == ("HI", 3)
a, b = part_ab(data)
print("part a:", a)
print("part b:", b)
