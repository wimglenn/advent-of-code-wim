from aoc_wim.aoc2015.q14 import race

data = """\
Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.
"""

def test_distance_race():
    assert race(data, max_t=1000, measure="distance") == 1120

def test_points_race():
    assert race(data, max_t=1000, measure="points") == 689
