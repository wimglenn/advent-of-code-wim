from aocd import data
from fractions import Fraction
from collections import defaultdict
from operator import itemgetter
import logging


# logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)


maps = """\
.#..#
.....
#####
....#
...##

......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####

#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.

.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..

.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
"""

pos_n = {(3, 4): 8, (5, 8): 33, (1, 2): 35, (6, 3): 41, (11, 13): 210}
tests = dict(zip(maps.split("\n\n"), pos_n.items()))


def parsed(data):
    asteroids = []
    rows = data.splitlines()
    for y, row in enumerate(rows):
        for x, val in enumerate(row):
            if val == "#":
                asteroids.append((x, y))
    assert len(asteroids) == data.count("#")
    return asteroids


def quadrant(a0, a):
    x0, y0 = a0
    x, y = a
    if y < y0 and x >= x0:
        return 1
    if y >= y0 and x > x0:
        return 2
    if y > y0 and x <= x0:
        return 3
    if y <= y0 and x < x0:
        return 4


def grad(a0, a):
    q = quadrant(a0, a)
    x0, y0 = a0
    x, y = a
    try:
        m = abs(Fraction(y - y0, x - x0))
    except ZeroDivisionError:
        m = float("inf")
    if q % 2:
        m *= -1
    return q, m


def part_a(data):
    gradients = defaultdict(set)
    A = parsed(data)
    for i, a0 in enumerate(A):
        for a in A[i + 1 :]:
            q, g = grad(a, a0)
            gradients[a0].add((q, g))
            gradients[a].add(((q + 2) % 4, -g))
    n_collinear = {k: len(v) for k, v in gradients.items()}
    a, n = max(n_collinear.items(), key=itemgetter(1))
    return a, n


def norm2(a1, a2):
    dx = a2[0] - a1[0]
    dy = a2[1] - a1[1]
    d2 = dx * dx + dy * dy
    return d2


def part_ab(data, target=200, extra_assertions=()):
    A = parsed(data)
    a0, part_a_answer = part_a(data)
    d = defaultdict(list)
    for a in A:
        if a == a0:
            continue
        g = grad(a0, a)
        d[g].append(a)
    ds = {}
    for g in sorted(d):
        ds[g] = sorted(d[g], key=lambda a: norm2(a0, a), reverse=True)
    i = 0
    while True:
        for g in ds:
            if ds[g]:
                a = ds[g].pop()
                i += 1
                if i in extra_assertions:
                    assert extra_assertions[i] == a
                    log.info("The %dth asteroid to be vaporized is at %d,%d", i, *a)
                if i == target:
                    part_b_answer = 100 * a[0] + a[1]
                    return part_a_answer, part_b_answer


for test_data, expected in tests.items():
    assert part_a(test_data) == expected

extra = """\
The 1st asteroid to be vaporized is at 11,12.
The 2nd asteroid to be vaporized is at 12,1.
The 3rd asteroid to be vaporized is at 12,2.
The 10th asteroid to be vaporized is at 12,8.
The 20th asteroid to be vaporized is at 16,0.
The 50th asteroid to be vaporized is at 16,9.
The 100th asteroid to be vaporized is at 10,16.
The 199th asteroid to be vaporized is at 9,6.
The 200th asteroid to be vaporized is at 8,2.
The 201st asteroid to be vaporized is at 10,9.
The 299th and final asteroid to be vaporized is at 11,1."""
extra_assertions = {}
for line in extra.splitlines():
    the, nth, *stuff, pos = line.split()
    n = int(nth[:-2])
    x, y = [int(v) for v in pos.strip(".").split(",")]
    extra_assertions[n] = (x, y)

test_b = list(tests)[-1]
assert part_ab(test_b) == (210, 802)
assert part_ab(test_b, 299, extra_assertions) == (210, 1101)

a, b = part_ab(data)
print(a)
print(b)
