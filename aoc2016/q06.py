from collections import Counter
from aocd import data


counters = [Counter(x) for x in zip(*data.splitlines())]
for f in max, min: 
    print(''.join(f(c, key=c.get) for c in counters))

