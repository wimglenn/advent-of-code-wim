from collections import Counter

from aocd import data

tests = {
    "ne,ne,ne": 3,
    "ne,ne,sw,sw": 0,
    "ne,ne,s,s": 2,
    "se,sw,se,sw,sw": 3,
}


def norm(data, steps=None):
    c = Counter(data.split(",")[:steps])
    c["ne"] -= c.pop("sw", 0)
    c["nw"] -= c.pop("se", 0)
    c["s"] -= c.pop("n", 0)
    d = sum(abs(x) for x in c.values()) - abs(sorted(c.values())[1])
    return d


for k, v in tests.items():
    assert norm(k) == v

print(norm(data))
print(max(norm(data, steps=i) for i in range(data.count(","))))
