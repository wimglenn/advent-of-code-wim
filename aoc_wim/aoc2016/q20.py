from aocd import data


test_data = """\
5-8
0-2
4-7"""


def cleanup_data(data):
    ranges = []
    for line in data.splitlines():
        ranges.append(tuple([int(n) for n in line.split("-")]))

    ranges.sort()

    while True:
        n = len(ranges)
        for i0, i1 in zip(range(n), range(n)[1:]):
            lo_p, hi_p = ranges[i0]
            lo, hi = ranges[i1]
            if lo <= hi_p + 1:
                del ranges[i1]
                ranges[i0] = (lo_p, max(hi_p, hi))
                break
        else:
            break

    return ranges


def part_a(clean_data):
    return clean_data[0][1] + 1


def part_b(clean_data, n_min=0, n_max=4294967295):
    n = n_max - n_min + 1
    for lo, high in clean_data:
        n -= high - lo + 1
    return n


clean_test_data = cleanup_data(test_data)
assert part_a(clean_test_data) == 3
assert part_b(clean_test_data, n_min=0, n_max=9) == 2

clean_data = cleanup_data(data)
print(part_a(clean_data))
print(part_b(clean_data))
