"""
--- Day 10: Monitoring Station ---
https://adventofcode.com/2019/day/10
"""
import logging
from aocd import data
from fractions import Fraction
from collections import defaultdict
from operator import itemgetter
from aoc_wim.zgrid import ZGrid


# logging.basicConfig(format="%(message)s", level=logging.INFO)
log = logging.getLogger(__name__)


def parsed(data):
    zs = ZGrid(data).z(val="#", first=False)
    xys = [(int(z.real), int(z.imag)) for z in zs]
    assert len(xys) == data.count("#")
    return xys


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


def best_monitoring_station(data):
    # returns (x, y), n_asteroids_detected
    gradients = defaultdict(set)
    asteroids = parsed(data)
    for i, a0 in enumerate(asteroids):
        for a in asteroids[i + 1 :]:
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


def part_ab(data, target=200):
    n_max = data.count("#") - 1
    target = min(target, n_max)
    asteroids = parsed(data)
    a0, part_a_answer = best_monitoring_station(data)
    d = defaultdict(list)
    for a in asteroids:
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
                s = {1: "st", 2: "nd", 3: "rd"}.get(i % 10, "th")
                f = "and final " if i == n_max else ""
                log.info("The %d%s %sasteroid to be vaporized is at %d,%d.", i, s, f, *a)
                if i == target:
                    part_b_answer = 100 * a[0] + a[1]
                    return part_a_answer, part_b_answer


if __name__ == "__main__":
    a, b = part_ab(data)
    print("part a:", a)
    print("part b:", b)
