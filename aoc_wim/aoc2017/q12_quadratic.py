"""
--- Day 12: Digital Plumber ---
https://adventofcode.com/2017/day/12
"""
from aocd import data


d = {}
for line in data.replace(" <->", ",").splitlines():
    xs = [int(x) for x in line.split(", ")]
    d[tuple(xs)] = set(xs)

while True:
    for tuple_, set1 in d.items():
        try:
            match = next(k for k, set2 in d.items() if k != tuple_ and set1 & set2)
        except StopIteration:
            continue  # no match for this key - keep looking
        else:
            d[tuple_] = set1 | d.pop(match)
            break  # merged match and set1
    else:
        break  # no match for any key - we are done!

[set0] = [v for v in d.values() if 0 in v]
print("answer_a:", len(set0))
print("answer_b:", len(d))
