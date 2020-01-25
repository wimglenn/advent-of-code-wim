import pathlib

import pytest

from aoc_wim import plugin


here = pathlib.Path(__file__).parent
input_files = sorted(here.glob("20*/*/*.txt"))


def path2id(input_file):
    return str(input_file.relative_to(here))


@pytest.mark.parametrize("input_file", input_files, ids=path2id)
def test_example(input_file, monkeypatch):
    # example input files are in ./YYYY/dd/fname.txt
    *pre, year, day, fname = input_file.parts
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
