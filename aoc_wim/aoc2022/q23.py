"""
--- Day 23: Unstable Diffusion ---
https://adventofcode.com/2022/day/23
"""
import numpy as np
from aocd import data
from scipy.signal import convolve2d

from aoc_wim.ocr import autocrop


A = np.array([[int(c == "#") for c in line] for line in data.splitlines()])
mask = [1 << i for i in range(8)]
mask.insert(4, 0)
kernel = np.array(mask).reshape(3, 3)
maskN = kernel[-1,:].sum()
maskS = kernel[0,:].sum()
maskW = kernel[:,-1].sum()
maskE = kernel[:,0].sum()
masks = np.array([[maskN, maskS, maskW, maskE]]).T
offsets = np.array([
    [-1, 0],
    [1, 0],
    [0, -1],
    [0, 1],
])
a = b = None
r = 0
while a is None or b is None:
    r += 1
    A = np.pad(autocrop(A), pad_width=1)
    C = convolve2d(A, kernel, mode="same")
    w = np.argwhere(A)
    dirs = C[*w.T] & masks
    d0 = dirs == 0
    d = d0.argmax(axis=0)
    stay = d0.all(axis=0) | (~d0).all(axis=0)
    if b is None and stay.all():
        b = r
    w_ = w.copy()
    for i in range(4):
        w_[~stay & (d == i)] += offsets[i]
    yx, i, u = np.unique(w_, axis=0, return_counts=True, return_index=True)
    stay.fill(True)
    stay[i[u==1]] = False
    A.fill(0)
    A[*np.where(stay[:,None], w, w_).T] = 1
    offsets = np.roll(offsets, -1, axis=0)
    masks = np.roll(masks, -1, axis=0)
    if r == 10:
        a = (autocrop(A) == 0).sum()

print("answer_a:", a)
print("answer_b:", b)
