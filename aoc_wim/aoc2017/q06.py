from aocd import data
from itertools import count
import numpy as np

def part_ab(data):
    a = np.fromstring(data, sep=' ', dtype=int)
    n = len(a)
    seen = {}
    for i in count():
        t = tuple(a)
        if t in seen:
            return i, i - seen[t]
        seen[t] = i
        max_pos = a.argmax()
        q, r = divmod(a[max_pos], n)
        a[max_pos] = 0
        a += np.roll([q+1]*r + [q]*(n-r), max_pos+1)

test_data = '0 2 7 0'
assert part_ab(test_data) == (5, 4)


a, b = part_ab(data)
print("part a:", a)
print("part b:", b)
