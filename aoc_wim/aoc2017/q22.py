"""
--- Day 22: Sporifica Virus ---
https://adventofcode.com/2017/day/22
"""
from aocd import data
from aocd import extra


def parsed(data):
    lines = data.splitlines()
    s = len(lines) // 2
    grid = {}
    for row, line in enumerate(lines, -s):
        for col, char in enumerate(line, -s):
            grid[col - row * 1j] = char
    return grid


def mutate(data, n, part="a"):
    mutations = {
        "a": {"#": ".", ".": "#"},
        "b": {"#": "F", "F": ".", ".": "W", "W": "#"},
    }
    mutation = mutations[part]
    factors = {".": 1j, "W": 1, "F": -1, "#": -1j}
    grid = parsed(data)
    p, v = 0, 1j
    n_infected = 0
    for i in range(n):
        s = grid.get(p, ".")
        v *= factors[s]
        grid[p] = mutation[s]
        if grid[p] == "#":
            n_infected += 1
        p += v
    return n_infected


if __name__ == "__main__":
    print("answer_a:", mutate(data, n=extra.get("iterations", 10000), part="a"))
    print("answer_b:", mutate(data, n=extra.get("iterations", 10000000), part="b"))
