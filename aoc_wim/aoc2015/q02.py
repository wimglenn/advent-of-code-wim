from aocd import data


def box_area(w, h, l):
    return 2 * l * w + 2 * w * h + 2 * h * l


def smallest_side(w, h, l):
    return min(l * w, w * h, h * l)


def shortest_perimeter(w, h, l):
    return 2 * min(l + w, w + h, h + l)


def box_volume(w, h, l):
    return w * h * l


def part_ab(data):
    area = 0
    length = 0
    for line in data.splitlines():
        w, h, l = [int(d) for d in line.split("x")]
        area += box_area(w, h, l) + smallest_side(w, h, l)
        length += shortest_perimeter(w, h, l) + box_volume(w, h, l)
    return area, length


a_tests = {
    "2x3x4": (58, 34),
    "1x1x10": (43, 14),
}
for test_data, expected in a_tests.items():
    assert part_ab(test_data) == expected


a, b = part_ab(data)
print("part a:", a)
print("part b:", b)
