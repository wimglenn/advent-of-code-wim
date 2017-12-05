from aocd import data

def run(data, b_offset=1):
    state = [int(x) for x in data.split()]
    i = pos = 0
    while True:
        try:
            offset = state[pos]
        except IndexError:
            return i, state
        i += 1
        state[pos] += b_offset if offset >= 3 else 1
        pos += offset

test_data = '0 3 0 1 -3'
assert run(test_data) == (5, [2, 5, 0, 1, -2])
assert run(test_data, b_offset=-1) == (10, [2, 3, 2, 3, -1])

print(run(data)[0])  # part a: 356945
print(run(data, b_offset=-1)[0])  # part b: 28372145
