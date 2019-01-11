from aocd import data
import numpy as np

def s2a(s):
    return np.array([[{'.': 0, '#': 1}[c] for c in row] for row in s.split('/')])

def a2s(a):
    return '/'.join(''.join('.#'[n] for n in row) for row in a)

def parsed(data):
    rules = {}
    for line in data.splitlines():
        a, _sep, b = line.partition(' => ')
        a, b = s2a(a), s2a(b)
        for i in range(4):
            rules[a2s(a)] = rules[a2s(np.flipud(a))] = rules[a2s(np.fliplr(a))] = b
            a = np.rot90(a)
    return rules

def run(data, iterations):
    rules = parsed(data)
    grid = s2a('.#./..#/###')
    for i in range(iterations):
        n = len(grid)
        s = 3 if n%2 else 2
        n //= s
        rows = []
        for row in range(n):
            r = []
            for col in range(n):
                c = grid[row*s:(row+1)*s, col*s:(col+1)*s]
                r.append(rules[a2s(c)])
            r = np.hstack(r)
            rows.append(r)
        grid = np.vstack(rows)
    return grid.sum()

test_data = """\
../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#"""

assert run(test_data, 2) == 12
print(run(data, 5))
print(run(data, 18))
