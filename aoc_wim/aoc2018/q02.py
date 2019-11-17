from collections import Counter
from itertools import combinations

from aocd import data


def part_a(data):
    counters = [Counter(s) for s in data.split()]
    doubles = sum(1 for c in counters if 2 in c.values())
    triples = sum(1 for c in counters if 3 in c.values())
    return doubles * triples


def part_b(data):
    for a, b in combinations(data.split(), 2):
        s = "".join([x for x, y in zip(a, b) if x == y])
        if len(s) == len(a) - 1:
            return s


test_a = """
abcdef
bababc
abbcde
abcccd
aabcdd
abcdee
ababab
"""

test_b = """
abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz
"""

assert part_a(test_a) == 12
assert part_b(test_b) == "fgij"


print("part a:", part_a(data))
print("part b:", part_b(data))
