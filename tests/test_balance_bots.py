from aoc_wim.aoc2016 import q10


test_data = """\
value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2"""


def test_five_two():
    assert q10.part_ab(test_data, lh=(2, 5))[0] == 2
