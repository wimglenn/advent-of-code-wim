from aocd import data


def part_a(data):
    s0 = data
    while True:
        xs = set(s0.lower())
        for x in xs:
            sub1 = x + x.upper()
            sub2 = x.upper() + x
            s1 = s0.replace(sub1, "").replace(sub2, "")
            if len(s1) < len(s0):
                s0 = s1
                break
        else:
            return len(s0)


def part_b(data):
    result = len(data)
    for x in set(data.lower()):
        m = part_a(data.replace(x, "").replace(x.upper(), ""))
        result = min(m, result)
    return result


test_data = "dabAcCaCBAcCcaDA"
assert part_a(test_data) == 10
assert part_b(test_data) == 4


print("part a:", part_a(data))
print("part b:", part_b(data))
