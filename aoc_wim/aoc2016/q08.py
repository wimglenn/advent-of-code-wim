from aocd import data
import numpy as np
from ..ocr import AOCR


def parsed(data):
    W, H = 50, 6
    A = np.zeros((H, W), dtype=bool)
    for line in data.splitlines():
        if line.startswith('rect'):
            w, h = [int(x) for x in line.split()[1].split('x')]
            A[0:h,0:w] = True
        elif line.startswith('rotate'):
            i, shift = [int(x) for x in line.split('=')[1].split(' by ')]
            item = (i, slice(None)) if 'row' in line else (slice(None), i)
            A[item] = np.roll(A[item], shift)
    return A


def part_a(data):
    A = parsed(data)
    return A.sum()


def part_b(data, dump=False):
    A = parsed(data)
    if dump:
        print("\n")
        for row in A.astype(int):
            print("".join([" █"[x] for x in row]))
        print("\n")
    w = 5  # letter column width
    n = A.shape[1] // w  # number of chars
    msg = []
    for i in range(n):
        chunk = A[:, w*i:w*i+w]
        txt = "\n".join(["".join([".#"[int(i)] for i in row]) for row in chunk])
        try:
            msg.append(AOCR[txt])
        except KeyError:
            print(txt)
            raise
    return "".join(msg)


print("part a:", part_a(data))
print("part b:", part_b(data))
