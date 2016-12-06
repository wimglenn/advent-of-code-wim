from collections import Counter
import numpy as np
from aocd import data


columns = zip(*data.splitlines())

code1 = code2 = ''
for column in columns:
    counter = Counter(column)
    code1 += max(counter, key=counter.get)
    code2 += min(counter, key=counter.get)

print(code1)
print(code2)
