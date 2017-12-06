from aocd import data
import numpy as np

def run(data):
    a = np.fromstring(data, sep=' ', dtype=int)
    n = len(a)
    seen = {}
    i = 0
    while True:
        t = tuple(a)
        if t in seen:
            return i, i - seen[t]
        seen[t] = i
        max_pos = a.argmax()
        max_ = a[max_pos]
        q, r = divmod(max_, n)
        a[max_pos] = 0
        a += q
        a = np.roll(a, -max_pos-1)
        a[:r] += 1
        a = np.roll(a, max_pos+1)
        i += 1

test_data = '0 2 7 0'
assert run(test_data) == (5, 4)

a, b = run(data)
print(a)  # part a: 14029
print(b)  # part b: 2765
