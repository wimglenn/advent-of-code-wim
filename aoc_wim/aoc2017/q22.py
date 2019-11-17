from aocd import data


def parsed(data):
    lines = data.splitlines()
    s = len(lines) // 2
    grid = {}
    for row, line in enumerate(lines, -s):
        for col, char in enumerate(line, -s):
            grid[col - row * 1j] = char
    return grid


def mutate(data, n_iterations, mutation=1):
    mutations = {
        1: {"#": ".", ".": "#"},
        2: {"#": "F", "F": ".", ".": "W", "W": "#"},
    }
    mutation = mutations[mutation]
    factors = {".": 1j, "W": 1, "F": -1, "#": -1j}
    grid = parsed(data)
    p, v = 0, 1j
    n_infected = 0
    for i in range(n_iterations):
        s = grid.get(p, ".")
        v *= factors[s]
        grid[p] = mutation[s]
        if grid[p] == "#":
            n_infected += 1
        p += v
    return n_infected


test_data = """\
..#
#..
...
"""
assert mutate(test_data, n_iterations=7) == 5
assert mutate(test_data, n_iterations=70) == 41
assert mutate(test_data, n_iterations=10000) == 5587
assert mutate(test_data, n_iterations=100, mutation=2) == 26
assert mutate(test_data, n_iterations=10000000, mutation=2) == 2511944

print("part a:", mutate(data, n_iterations=10000))
print("part b:", mutate(data, n_iterations=10000000, mutation=2))
