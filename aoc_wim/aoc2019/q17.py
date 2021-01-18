"""
--- Day 17: Set and Forget ---
https://adventofcode.com/2019/day/17
"""
from aocd import data
from aoc_wim.aoc2019 import IntComputer
from aoc_wim.zgrid import ZGrid


def parsed(data):
    comp = IntComputer(data)
    comp.run()
    txt = "".join([chr(x) for x in reversed(comp.output)])
    grid = ZGrid(txt)
    grid.draw()
    return grid


def calibration(grid):
    result = 0
    for z0, txt in grid.items():
        if txt == "#" and {grid.get(z) for z in grid.near(z0)} == {"#"}:
            result += int(z0.real) * int(z0.imag)
    return result


def get_path(grid, compressed=True):
    # detect initial position and orientation
    [(z0, glyph)] = [(k,v) for (k,v) in grid.items() if v in "^>v<"]
    dz0 = grid.dzs[glyph]
    [z1] = [z for z in grid.near(z0) if grid.get(z) == "#"]
    steps = []

    # orient self onto scaffold
    if z0 + dz0 != z1:
        if z0 + dz0 * grid.turn_right == z1:
            steps.append("R")
            dz0 *= grid.turn_right
        elif z0 + dz0 * grid.turn_left == z1:
            steps.append("L")
            dz0 *= grid.turn_left
        else:
            assert z0 - dz0 == z1
            steps.extend("RR")
            dz0 *= grid.turn_around

    # find an uncompressed path
    z = z0
    dz = dz0
    while True:
        n = 0
        while grid.get(z + dz) == "#":
            n += 1
            z += dz
        steps.append(str(n))
        if grid.get(z + dz * grid.turn_right) == "#":
            dz *= grid.turn_right
            steps.append("R")
        elif grid.get(z + dz * grid.turn_left) == "#":
            dz *= grid.turn_left
            steps.append("L")
        else:
            break

    # compress path to memory requirement
    path = ",".join(steps)
    if compressed:
        options = compress(path)
        path = min(options, key=len)
        path += "\nn\n"  # suppress "continuous video feed"
    return path


def chunk_choices(path):
    choices = []
    for i in range(1, 20):
        chunk = path[:i]
        if path[i:i+1] not in {"", ","}:
            continue
        score = len(chunk) * path.count(chunk)
        choices.append((score, chunk))
    choices = {chunk: score for score, chunk in sorted(choices, reverse=True)}
    return choices


def compress(path, mem=20):
    results = []
    A_choices = chunk_choices(path)
    for A in A_choices:
        compressed_pathA = ""
        pathA = path
        while pathA.startswith(A):
            compressed_pathA += "A,"
            pathA = pathA[len(A):].lstrip(",")
        B_choices = chunk_choices(pathA)
        for B in B_choices:
            compressed_pathAB = compressed_pathA
            pathAB = pathA
            while pathAB.startswith((A, B)):
                if pathAB.startswith(A):
                    pathAB = pathAB[len(A):].lstrip(",")
                    compressed_pathAB += "A,"
                if pathAB.startswith(B):
                    pathAB = pathAB[len(B):].lstrip(",")
                    compressed_pathAB += "B,"
            C_choices = chunk_choices(pathAB)
            for C in C_choices:
                compressed_pathABC = compressed_pathAB
                pathABC = pathAB
                while pathABC.startswith((A, B, C)):
                    if pathABC.startswith(A):
                        pathABC = pathABC[len(A):].lstrip(",")
                        compressed_pathABC += "A,"
                    if pathABC.startswith(B):
                        pathABC = pathABC[len(B):].lstrip(",")
                        compressed_pathABC += "B,"
                    if pathABC.startswith(C):
                        pathABC = pathABC[len(C):].lstrip(",")
                        compressed_pathABC += "C,"
                if not pathABC:
                    result = compressed_pathABC.rstrip(",")
                    if len(result) <= mem:
                        results.append("\n".join([result, A, B, C]))
    return results


if __name__ == "__main__":
    grid = parsed(data)
    print("part a", calibration(grid))

    comp = IntComputer(data)
    comp.reg[0] = 2
    path = get_path(grid)
    comp.input_text(path)
    comp.run()
    print("part b", comp.output[0])
