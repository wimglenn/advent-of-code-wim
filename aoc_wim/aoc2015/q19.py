from collections import defaultdict

from aocd import data


test_data = """\
e => H
e => O
H => HO
H => OH
O => HH
"""


def parsed(data):
    reactions, element = data.split("\n\n")
    tr = defaultdict(list)
    tri = {}
    for line in reactions.splitlines():
        s, r = line.split(" => ")
        tr[s].append(r)
        tri[r] = s
    return tr, tri, element


def part_a(data):
    tr, tri, element = parsed(data)
    seen = set()
    for s, rs in tr.items():
        splitted = element.split(s)
        for i, (left, right) in enumerate(zip(splitted, splitted[1:])):
            for r in rs:
                new = splitted[:]
                new[i : i + 2] = [left + r + right]
                new = s.join(new)
                seen.add(new)
    return len(seen)


def part_b(data):
    tr, tri, element = parsed(data)
    replacements = 0
    while element != "e":
        pos = {}
        for k, v in tri.items():
            delta = len(k) - len(v)
            if k in element:
                if v != "e" or len(element) - delta == 1:
                    pos[k] = (element.rfind(k) + len(k), delta)
        k = max(pos, key=pos.get)
        v = tri[k]
        # replace from right
        element = element[::-1].replace(k[::-1], v[::-1], 1)[::-1]
        replacements += 1
    return replacements


assert part_a(test_data + "\nHOH") == 4
assert part_a(test_data + "\nHOHOHO") == 7
assert part_b(test_data + "\nHOH") == 3
assert part_b(test_data + "\nHOHOHO") == 6

print("part a:", part_a(data))
print("part b:", part_b(data))
