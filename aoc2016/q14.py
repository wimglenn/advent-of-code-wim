from aocd import data
from collections import defaultdict
from hashlib import md5
import re


def get_first_triple(hash_):
    candidate = re.search(r'([0-9a-f])\1{2}', hash_)
    if candidate is not None:
        return candidate.group()[0]


def get_all_quintuples(hash_):
    return re.findall(r'([0-9a-f])\1{4}', hash_)


def normal_hash(s):
    return md5(s).hexdigest()


def stretched_hash(s):
    for i in range(2017):
        s = md5(s).hexdigest().encode('ascii')
    return s.decode('ascii')


def search(data=data, hash_function=normal_hash):
    template = data.strip().encode('ascii') + b'%d'
    keys = []
    triples = defaultdict(list)
    i, max_i = 0, float('inf')
    while i < max_i:
        hash_ = hash_function(template % i)
        for k in get_all_quintuples(hash_):
            indices = triples[k]
            for index in indices:
                if i - index < 1000:
                    keys.append(index)
                    if len(keys) == 64:
                        max_i = i + 1000
        triple = get_first_triple(hash_)
        if triple is not None:
            triples[triple].append(i)
        i += 1
    return sorted(keys)[:64][-1]

assert search(data='abc') == 22728
print(search())

assert stretched_hash(b'abc0').startswith('a107ff')
assert search(data='abc', hash_function=stretched_hash) == 22551
print(search(hash_function=stretched_hash))
