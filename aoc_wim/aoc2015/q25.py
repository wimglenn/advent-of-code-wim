from aocd import data


def parsed(data):
    words = data.split()
    row = int(words[-3].rstrip(","))
    col = int(words[-1].rstrip("."))
    return row, col


def n(row, col):
    i = (row + col) * (row + col) + 2 - col - 3 * row
    return i // 2


def code(row, col, code0=20151125, m=252533, d=33554393):
    i = n(row, col)
    code = code0
    for _ in range(i - 1):
        code = m * code % d
    return code


row, col = parsed(data)
print(code(row, col))
