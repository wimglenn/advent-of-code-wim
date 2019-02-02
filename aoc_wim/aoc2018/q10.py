from aocd import data
import re
import numpy as np
from ..ocr import AOCR


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


def ocr(a, lettersize, draw=False):
    ps = a[:2].copy()
    ps -= ps.min(axis=1).reshape(-1, 1)
    W, H = ps.max(axis=1) + 1
    img = np.full((H, W), ".")
    h, w = lettersize
    assert h == H
    col, row = ps
    img[row, col] = "#"
    img = np.pad(img, ((0, 0), (1, 0)), mode='constant', constant_values=".")
    W += 1
    while W % w:
        img = np.pad(img, ((0, 0), (0, 1)), mode='constant', constant_values=".")
        W += 1
    n = W // w
    if draw:
        for row in img:
            print(*row, sep='')
        print("\n")
    letters = []
    for i in range(n):
        chunk = img[:, w*i:w*i+w]
        key = '\n'.join(''.join(row) for row in chunk)
        try:
            letter = AOCR[key]
        except KeyError:
            print(key)
            raise
        letters.append(letter)
    return ''.join(letters)


def part_ab(data, debug=False, lettersize=(10, 8)):
    numbers = [int(x) for x in re.findall("-?\d+", data)]
    a = np.array(numbers).reshape(-1, 4).T
    t = 0
    minv = varianceish(a)
    while True:
        a[:2] += a[2:]
        v = varianceish(a)
        minv = min(v, minv)
        if v > minv:
            a[:2] -= a[2:]  # back up one step
            text = ocr(a, lettersize=lettersize, draw=debug)
            return text, t
        t += 1


assert part_ab(test_data, lettersize=(8, 7)) == ("HI", 3)
a, b = part_ab(data)
print("part a:", a)
print("part b:", b)
