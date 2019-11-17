from aocd import data


def generate_rows(row):
    while True:
        yield row
        row = "." + row + "."
        S = {"^^.", ".^^", "^..", "..^"}
        indices = range(1, len(row) - 1)
        row = "".join(".^"[row[i - 1 : i + 2] in S] for i in indices)


def make_grid(row0, nrows):
    gen = generate_rows(row0)
    return "".join(next(gen) + "\n" for i in range(nrows))


def n_safe_tiles(row0, nrows):
    gen = generate_rows(row0)
    return sum(next(gen).count(".") for i in range(nrows))


expected = """\
..^^.
.^^^^
^^..^
"""
assert make_grid("..^^.", nrows=3) == expected

test_grid = """\
.^^.^.^^^^
^^^...^..^
^.^^.^.^^.
..^^...^^^
.^^^^.^^.^
^^..^.^^..
^^^^..^^^.
^..^^^^.^^
.^^^..^.^^
^^.^^^..^^
"""

row0 = test_grid.splitlines()[0]
assert make_grid(row0, nrows=10) == test_grid
assert n_safe_tiles(row0, nrows=10) == 38

print(n_safe_tiles(data, nrows=40))
print(n_safe_tiles(data, nrows=400000))
