from aoc_wim.aoc2015 import q18

example_a = """\
Initial state:
.#.#.#
...##.
#....#
..#...
#.#..#
####..

After 1 step:
..##..
..##.#
...##.
......
#.....
#.##..

After 2 steps:
..###.
......
..###.
......
.#....
.#....

After 3 steps:
...#..
......
...#..
..##..
......
......

After 4 steps:
......
......
..##..
..##..
......
......"""

example_b = """\
Initial state:
##.#.#
...##.
#....#
..#...
#.#..#
####.#

After 1 step:
#.##.#
####.#
...##.
......
#...#.
#.####

After 2 steps:
#..#.#
#....#
.#.##.
...##.
.#..##
##.###

After 3 steps:
#...##
####.#
..##.#
......
##....
####.#

After 4 steps:
#.####
#....#
...#..
.##...
#.....
#.#..#

After 5 steps:
##.###
.##..#
.##...
.##...
#.#...
##...#"""


def test_gif_a():
    frame0, *frames = example_a.split("\n\n")
    assert len(frames) == 4
    header, sep, grid = frame0.partition("\n")
    assert header == "Initial state:"
    A = q18.parsed(grid)
    for frame in frames:
        header, sep, grid = frame.partition("\n")
        expected = q18.parsed(grid)
        A = q18.evolve(A)
        assert (A == expected).all()
    assert A.sum() == 4


def test_gif_b():
    frame0, *frames = example_b.split("\n\n")
    assert len(frames) == 5
    header, sep, grid = frame0.partition("\n")
    assert header == "Initial state:"
    A = q18.parsed(grid)
    for frame in frames:
        header, sep, grid = frame.partition("\n")
        expected = q18.parsed(grid)
        A = q18.evolve(A, part="b")
        assert (A == expected).all()
    assert A.sum() == 17
