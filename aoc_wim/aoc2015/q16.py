"""
--- Day 16: Aunt Sue ---
https://adventofcode.com/2015/day/16
"""
from aocd import data


message = """\
children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1
"""


d_message = {k: int(v) for k, v in (pair.split(": ") for pair in message.splitlines())}

sues = {}
for line in data.splitlines():
    sue, stats = line.split(": ", 1)
    stats = {k: int(v) for k, v in (pair.split(": ") for pair in stats.split(", "))}
    sues[sue] = stats


def find_sue(**kwargs):
    for sue, stats in sues.items():
        common_keys = d_message.keys() & stats.keys()
        if all(kwargs.get(k, int.__eq__)(stats[k], d_message[k]) for k in common_keys):
            return int(sue.split()[1])


a = find_sue()
b = find_sue(
    cats=int.__gt__,
    trees=int.__gt__,
    pomeranians=int.__lt__,
    goldfish=int.__lt__,
)

print("answer_a:", a)
print("answer_b:", b)
