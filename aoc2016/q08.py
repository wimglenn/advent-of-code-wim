from aocd import data
from collections import deque
import numpy as np 
import matplotlib.pyplot as plt


W, H = 50, 6
A = np.zeros((H, W), dtype=bool)

for line in data.splitlines():
    if line.startswith('rect'):
        w, h = [int(x) for x in line.split()[1].split('x')]
        A[0:h,0:w] = True
    elif line.startswith('rotate'):
        i, shift = [int(x) for x in line.split('=')[1].split(' by ')]
        item = (i, slice(None)) if 'row' in line else (slice(None), i)
        d = deque(A[item])
        d.rotate(shift)
        A[item] = d
    else:
        print(line)
        raise Exception

print(A.sum())
plt.imshow(~A, interpolation='nearest')
plt.gray()
plt.show()
