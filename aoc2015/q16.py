from aocd import data
from collections import defaultdict
import operator


message = '''
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
'''.strip()


d_message = {k: int(v) for k,v in (pair.split(': ') for pair in message.splitlines())}

sues = {}
for line in data.splitlines():
    sue, stats = line.split(': ', 1)
    stats = {k: int(v) for k,v in (pair.split(': ') for pair in stats.split(', '))}
    sues[sue] = stats


def find_sue(**kwargs):
    opmap = defaultdict(lambda: operator.eq)
    opmap.update(kwargs)
    for sue, stats in sues.items():
        common_keys = d_message.keys() & stats.keys()
        if all(opmap[k](stats[k], d_message[k]) for k in common_keys):
            return int(sue.split()[1])


print(find_sue())  # part a: 103
print(find_sue(cats=operator.gt, trees=operator.gt, pomeranians=operator.lt, goldfish=operator.lt))  # part b: 405
