"""
--- Day 12: Digital Plumber ---
https://adventofcode.com/2017/day/12
"""
from aocd import data


def part_ab(data):
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
    a = len(set0)
    b = len(d)
    return a, b


test_data = """\
0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5"""

assert part_ab(test_data) == (6, 2)

a, b = part_ab(data)
print("part a:", a)
print("part b:", b)
