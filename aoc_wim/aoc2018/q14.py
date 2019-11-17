from collections import deque

from aocd import data
from wimpy import is_subsequence


def gen():
    recipes = [3, 7]
    e1, e2 = 0, 1
    yield recipes[0]
    yield recipes[1]
    while True:
        n = recipes[e1] + recipes[e2]
        vals = [int(x) for x in str(n)]
        for val in vals:
            yield val
        recipes.extend(vals)
        e1 = (e1 + 1 + recipes[e1]) % len(recipes)
        e2 = (e2 + 1 + recipes[e2]) % len(recipes)


def part_a(data):
    k = int(data)
    g = gen()
    for n in range(k):
        next(g)
    s = "".join(str(next(g)) for n in range(10))
    return s


def part_b(data):
    n = len(data)
    s = [int(x) for x in data]
    g = gen()
    i = 0
    tail = deque(maxlen=n)
    while not is_subsequence(s, tail):
        tail.append(next(g))
        i += 1
    return i - n


tests = [
    (9, "5158916779"),
    (5, "0124515891"),
    (18, "9251071085"),
    (2018, "5941429882"),
]

for n_recipes, scores in tests:
    assert part_a(n_recipes) == scores
    assert part_b(scores[:5]) == n_recipes


print("part a:", part_a(data))
print("part b:", part_b(data))
