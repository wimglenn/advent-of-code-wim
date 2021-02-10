"""
--- Day 5: How About a Nice Game of Chess? ---
https://adventofcode.com/2016/day/5
"""
from _md5 import md5
from aocd import data


code1 = []
code2 = ["."] * 8
remaining = set("01234567")
h0 = md5(data.encode("ascii")).copy


n = 0
while True:
    hash_ = h0()
    hash_.update(b"%d" % n)
    hash_ = hash_.hexdigest()
    n += 1
    if not hash_.startswith("00000"):
        continue
    h5, h6 = hash_[5], hash_[6]
    code1.append(h5)
    if h5 in remaining:
        code2[int(h5)] = h6
        remaining.remove(h5)
        if not remaining:
            break

code1 = "".join(code1[:8])
code2 = "".join(code2)


print("part a:", code1)
print("part b:", code2)
