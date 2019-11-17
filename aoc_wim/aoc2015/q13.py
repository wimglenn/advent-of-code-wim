from collections import defaultdict
from itertools import permutations

from aocd import data


test_data = """\
Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.
"""


def parsed(data, extra_name=None):
    d = defaultdict(int)
    names = {extra_name} - {None}
    for line in data.splitlines():
        words = line.split()
        name0 = words[0]
        name1 = words[-1].rstrip(".")
        n = {"gain": 1, "lose": -1}[words[2]] * int(words[3])
        d[(name0, name1)] = n
        names |= {name0, name1}
    return names, d


def get_best_plan(data, extra_name=None):
    names, d = parsed(data, extra_name)
    n = len(names)
    plans = permutations(names)
    happiness = {}
    for plan in plans:
        total = 0
        for i in range(n):
            person = plan[i]
            left = plan[(i - 1) % n]
            right = plan[(i + 1) % n]
            total += d[(person, left)]
            total += d[(person, right)]
        happiness[plan] = total
    return max(happiness.values())


assert get_best_plan(test_data) == 330
print(get_best_plan(data))
print(get_best_plan(data, extra_name="wim"))
