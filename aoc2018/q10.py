from aocd import data
import re
import numpy as np


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


def draw(a):
    ps = a[:2].copy()
    ps -= ps.min(axis=1).reshape(-1, 1)
    w, h = ps.max(axis=1) + 1
    img = np.full((h, w), ".")
    col, row = ps
    img[row, col] = "#"
    for row in img:
        print(*row, sep='')
    print('\n')


def run(data):
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
            draw(a)
            return t
        t += 1


assert run(test_data) == 3  # HI
print(run(data))

# TODO: OCR
