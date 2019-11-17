from aocd import data


def part_a(data, b_offset=1):
    state = [int(x) for x in data.split()]
    i = pos = 0
    while True:
        try:
            offset = state[pos]
        except IndexError:
            part_a.final_state = state
            return i
        i += 1
        state[pos] += b_offset if offset >= 3 else 1
        pos += offset


def part_b(data):
    return part_a(data, b_offset=-1)


test_data = "0 3 0 1 -3"
assert part_a(test_data) == 5
assert part_a.final_state == [2, 5, 0, 1, -2]
assert part_b(test_data) == 10
assert part_a.final_state == [2, 3, 2, 3, -1]


print("part a:", part_a(data))
print("part b:", part_b(data))
