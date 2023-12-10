import pytest

from aoc_wim.aoc2021.q24 import Comp


prog1 = """\
inp x
mul x -1"""

prog2 = """\
inp z
inp x
mul z 3
eql z x
"""

prog3 = """\
inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2"""


@pytest.mark.parametrize("i", range(-10, 10))
def test_negation(i):
    comp = Comp(code=prog1, inputs=[i])
    comp.run()
    assert comp.reg["x"] == -i


@pytest.mark.parametrize("a,b,z", [
    (1, 3, 1),
    (1, 2, 0),
    (0, 0, 1),
    (-1, -3, 1),
    (123, 369, 1),
    (369, 123, 0),
])
def test_triple_eq(a, b, z):
    comp = Comp(code=prog2, inputs=[a, b])
    comp.run()
    assert comp.reg["z"] == z


@pytest.mark.parametrize("i", range(20))
def test_binary(i):
    comp = Comp(code=prog3, inputs=[i])
    comp.run()
    expected = f"{i:04b}"[-4:]
    actual = "".join(str(comp.reg[i]) for i in "wxyz")
    assert expected == actual
