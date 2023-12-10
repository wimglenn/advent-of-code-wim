import numpy as np

from aoc_wim.aoc2016 import q08
from aoc_wim.zgrid import ZGrid


frames = """\
###....
###....
.......

#.#....
###....
.#.....

....#.#
###....
.#.....

.#..#.#
#.#....
.#.....
"""

data = """\
rect 3x2
rotate column x=1 by 1
rotate row y=0 by 4
rotate column x=1 by 1
"""


def test_animate():
    A = np.full((3, 7), ".")
    for frame, line in zip(frames.split("\n\n"), data.splitlines()):
        A = q08.animate(A, line)
        expected = np.array(ZGrid(frame))
        assert (A == expected).all()
