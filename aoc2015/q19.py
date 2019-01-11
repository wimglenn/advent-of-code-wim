from aocd import data
from collections import defaultdict


test_data = """\
e => H
e => O
H => HO
H => OH
O => HH
"""


def parse_tr(data):
    tr = defaultdict(list)
    tri = defaultdict(list)
    for line in data.strip().splitlines():
        s, r = line.split(' => ')
        tr[s].append(r)
        tri[r].append(s)
    return tr, tri


def gen(tr, element):
    for s, rs in tr.items():
        splitted = element.split(s)
        for i, (left, right) in enumerate(zip(splitted, splitted[1:])):
            for r in rs:
                new = splitted[:]
                new[i:i+2] = [left + r + right]
                new = s.join(new)
                yield new


def part_a(data, element):
    tr, tri = parse_tr(data)
    return len({word for word in gen(tr, element)})


def part_b(data, element, element0='e'):
    tr, tri = parse_tr(data)
    i = 0
    while element != element0:
        subs = [k for k in tri if k in element]
        subs.sort(key=len)
        sub = subs[-1]
        element = element.replace(sub, tri[sub][0], 1)
        i += 1
    return i


assert part_a(test_data, 'HOH') == 4
assert part_a(test_data, 'HOHOHO') == 7
assert part_b(test_data, 'HOH') == 3
assert part_b(test_data, 'HOHOHO') == 6


element_pos = data.rfind('\n')
data_, element = data[:element_pos], data[element_pos:].strip()

print(part_a(data_, element))
print(part_b(data_, element))
