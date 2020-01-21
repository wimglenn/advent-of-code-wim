from aoc_wim.aoc2015 import q23

data = """\
inc a
jio a, +2
tpl a
inc a
"""


def test_simple_jump():
    computer = q23.Computer(instructions=data)
    computer.compute()
    assert computer.registers["a"] == 2
