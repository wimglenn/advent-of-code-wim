# coding: utf-8
from __future__ import print_function, unicode_literals
from aocd import data
import numpy as np 


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
    else:
        print(line)
        raise Exception

print(A.sum())

print('\n')
for row in A:
    print(''.join([' █'[x] for x in row]))
print('\n')
