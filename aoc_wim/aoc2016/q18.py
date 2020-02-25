from aocd import data


def generate_rows(row):
    idx = range(len(row))
    S = {"^^.", ".^^", "^..", "..^"}
    while True:
        yield row
        row = "." + row + "."
        row = "".join([".^"[row[i:i + 3] in S] for i in idx])


def make_grid(row0, nrows):
    gen = generate_rows(row0)
    return "".join(next(gen) + "\n" for i in range(nrows))


def n_safe_tiles(row0, nrows):
    gen = generate_rows(row0)
    return sum(next(gen).count(".") for i in range(nrows))


if __name__ == "__main__":
    print(n_safe_tiles(data, nrows=40))
    print(n_safe_tiles(data, nrows=400000))
