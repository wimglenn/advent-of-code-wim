from aoc_wim.aoc2019 import q12


test10 = """\
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>"""

test100 = """\
<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>"""


def test_total_energy_after_10_steps():
    assert q12.simulate(test10, n=10) == 179


def test_total_energy_after_100_steps():
    assert q12.simulate(test100, n=100) == 1940
