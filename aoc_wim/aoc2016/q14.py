import re
from collections import defaultdict
from aocd import data
try:
    from _md5 import md5
except ImportError:
    from hashlib import md5


def normal_hash(s):
    return md5(s).hexdigest()


def stretched_hash(s):
    for i in range(2017):
        s = md5(s).hexdigest().encode()
    return s.decode()


def search(data=data, hash_function=normal_hash):
    template = data.encode() + b"%d"
    keys = []
    triples = defaultdict(list)
    pat3 = re.compile(r"([0-9a-f])\1{2}")
    pat5 = re.compile(r"([0-9a-f])\1{4}")
    i = 0
    stop = None
    while stop is None or i < stop:
        hash_ = hash_function(template % i)
        triple = pat3.search(hash_)
        if triple is not None:
            for quintuple in pat5.findall(hash_):
                keys.extend([x for x in triples[quintuple] if i - x <= 1000])
                triples[quintuple].clear()  # avoid to count same key twice
                if stop is None and len(keys) >= 64:
                    stop = i + 1001
            triples[triple.group()[0]].append(i)
        i += 1
    return sorted(keys)[:64][-1]


print("part a:", search())
print("part b:", search(hash_function=stretched_hash))
