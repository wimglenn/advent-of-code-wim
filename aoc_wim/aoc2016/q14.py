import re
from collections import defaultdict
from hashlib import md5

from aocd import data


def get_first_triple(hash_):
    candidate = re.search(r"([0-9a-f])\1{2}", hash_)
    if candidate is not None:
        return candidate.group()[0]


def get_all_quintuples(hash_):
    return re.findall(r"([0-9a-f])\1{4}", hash_)


def normal_hash(s):
    return md5(s).hexdigest()


def stretched_hash(s):
    for i in range(2017):
        s = md5(s).hexdigest().encode("ascii")
    return s.decode("ascii")


def search(data=data, hash_function=normal_hash):
    template = data.strip().encode("ascii") + b"%d"
    keys = []
    triples = defaultdict(list)
    i = 0
    stop = None
    while stop is None or i < stop:
        hash_ = hash_function(template % i)
        for k in get_all_quintuples(hash_):
            keys.extend([x for x in triples[k] if i - x <= 1000])
            triples[k].clear()  # avoid to count same key twice
            if len(keys) >= 64 and stop is None:
                stop = i + 1001
        triple = get_first_triple(hash_)
        if triple is not None:
            triples[triple].append(i)
        i += 1
    return sorted(keys)[:64][-1]


assert search(data="abc") == 22728
print("part a:", search())

assert stretched_hash(b"abc0") == "a107ff634856bb300138cac6568c0f24"
assert search(data="abc", hash_function=stretched_hash) == 22551
print("part b:", search(hash_function=stretched_hash))
