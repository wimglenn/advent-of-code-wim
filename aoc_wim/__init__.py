"""Wim's solutions for https://adventofcode.com/"""
import io
import runpy
import sys
from pathlib import Path


def dynamic_version():
    here = Path(__file__).parent
    years = here.glob("aoc20??")
    max_year = max(years)
    days = max_year.glob("q??.py")
    max_day = max(days)
    year = int(max_year.name[-4:])
    day = int(max_day.name[1:3])
    return f"{year}.{day}"


__version__ = dynamic_version()


def plugin(year, day, data):
    mod_name = "aoc_wim.aoc{}.q{:02d}".format(year, day)
    sys.modules.pop(mod_name, None)
    old_stdout = sys.stdout
    sys.stdout = out = io.StringIO()
    try:
        import aocd
        aocd.data = data
        runpy.run_module(mod_name, run_name="__main__")
    finally:
        sys.stdout = old_stdout
        del aocd.data
    lines = [x for x in out.getvalue().splitlines() if x]
    answer_a = answer_b = None
    for line in lines:
        if line.startswith("answer_a"):
            if len(line.split()) > 1:
                answer_a = line.split()[-1]
            else:
                answer_a = ""
        elif line.startswith("answer_b"):
            if len(line.split()) > 1:
                answer_b = line.split()[-1]
            else:
                answer_b = ""
    if answer_a is not None and answer_b is not None:
        return answer_a, answer_b
    if not lines:
        return None, None
    if len(lines) == 1:
        answer_a = lines[0].split()[-1]
    else:
        if answer_a is None:
            answer_a = lines[-2].split()[-1]
        if answer_b is None:
            answer_b = lines[-1].split()[-1]
    return answer_a, answer_b
