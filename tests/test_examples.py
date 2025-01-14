import json
import pathlib

import pytest

from aoc_wim import plugin
from aoc_wim.util import parse_extra_context
from aoc_wim.util import split_trailing_comments


here = pathlib.Path(__file__).parent
input_files = sorted(here.glob("20*/*/*.txt"))


def path2id(input_file):
    rel_path = input_file.relative_to(here)
    result = str(rel_path)
    titles = getattr(pytest, "puzzle_titles", {})
    title = titles.get(str(rel_path.parent))
    if title:
        result += f" : {title}"
    return result


@pytest.mark.parametrize("input_file", input_files, ids=path2id)
def test_example(input_file, monkeypatch, request):
    # example input files are in ./YYYY/dd/fname.txt
    *pre, year, day, fname = input_file.parts
    year = int(year)
    day = int(day)
    # the head of each example file is an input data
    # the last two lines are part a and part b correct answers
    # there may be trailing comments after the answers
    lines = input_file.read_text(encoding="utf-8").splitlines()
    extra = split_trailing_comments(lines)
    extra = parse_extra_context(extra)
    if extra:
        monkeypatch.setenv("AOCD_EXTRA", json.dumps(extra))
    if len(lines) < 3:
        pytest.fail(f"test data {input_file} is malformed")
    *lines, expected_answer_a, expected_answer_b = lines
    input_data = "\n".join(lines).rstrip()
    # patch out aocd
    monkeypatch.setattr("aocd.data", input_data)
    # invoke the entrypoint with a controlled input
    actual_answer_a, actual_answer_b = plugin(year, day, input_data)
    # verify correct answers returned. sometimes a dash (-) may be used to indicate
    # an example input where the answer was provided for only one of the two parts
    if expected_answer_a != "-":
        assert actual_answer_a == expected_answer_a, f"{actual_answer_a=} {expected_answer_a=}"
    if expected_answer_b != "-" and not request.config.getoption("--part-a-only"):
        assert actual_answer_b == expected_answer_b, f"{actual_answer_b=} {expected_answer_b=}"
