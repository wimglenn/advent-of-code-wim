from collections import Counter
import numpy as np
from aocd import data


A = np.array([list(a) for a in data.splitlines()], dtype='U1')

code1 = code2 = ''
for column in A.T:
    counter = Counter(column)
    code1 += max(counter, key=counter.get)
    code2 += min(counter, key=counter.get)

print(code1)
print(code2)
