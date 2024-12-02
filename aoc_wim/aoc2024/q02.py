from aocd import data


def safe(ns0):
    ns = sorted(ns0)
    if ns != ns0 and ns != ns0[::-1]:
        return False
    return all(1 <= j - i <= 3 for i, j in zip(ns, ns[1:]))


a = b = 0
for line in data.splitlines():
    levels = [int(n) for n in line.split()]
    if safe(levels):
        a += 1
        b += 1
        continue
    for i in range(len(levels)):
        b_levels = levels.copy()
        del b_levels[i]
        if safe(b_levels):
            b += 1
            break

print("answer_a:", a)
print("answer_b:", b)
