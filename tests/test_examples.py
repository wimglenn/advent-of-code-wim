import pathlib
from operator import attrgetter

import pytest

from aoc_wim import plugin


here = pathlib.Path(__file__).parent
data_samples = sorted(here.joinpath("data").glob("*.txt"))
slow = {"2015_04_a.txt", "2015_04_b.txt"}
data_samples = [p for p in data_samples if p.name not in slow]


@pytest.mark.parametrize("input_file", data_samples, ids=attrgetter("name"))
def test_example(input_file, monkeypatch):
    # the example input filename is e.g. YYYY_dd_suffix.txt
    year, day, *rest = str(input_file.name).split("_")
    year = int(year)
    day = int(day)

    # the head of each example file is an input data
    # the last two lines are part a and part b correct answers
    *lines, part_a_answer, part_b_answer = input_file.read_text().splitlines()
    input_data = "\n".join(lines).strip()

    # patch out aocd
    monkeypatch.setattr("aocd.data", input_data)

    # invoke the entrypoint with a controlled input
    part_a, part_b = plugin(year, day, input_data)

    # verify correct answers returned. sometimes a dash (-) may be used to indicate
    # an example input where the answer was provided for only one of the two parts
    if part_a_answer != "-":
        assert part_a == part_a_answer
    if part_b_answer != "-":
        assert part_b == part_b_answer
