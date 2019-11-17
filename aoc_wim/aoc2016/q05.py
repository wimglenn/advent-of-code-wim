from hashlib import md5

from aocd import data


def part_ab(data):
    data = data.strip().encode("ascii")
    code1 = ""
    code2 = [None] * 8
    n = 0
    remaining = set("01234567")
    while True:
        test = b"%s%d" % (data, n)
        hash_ = md5(test).hexdigest()
        n += 1
        if not hash_.startswith("0" * 5):
            continue
        h5, h6 = hash_[5], hash_[6]
        code1 += h5
        if h5 in remaining:
            code2[int(h5)] = h6
            remaining.remove(h5)
            if not remaining:
                break
    code1 = code1[:8]
    code2 = "".join(code2)
    return code1, code2


assert part_ab("abc") == ("18f47a30", "05ace8e3")

a, b = part_ab(data)
print("part a:", a)
print("part b:", b)
