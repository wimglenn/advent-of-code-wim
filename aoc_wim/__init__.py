"""Wim's solutions for https://adventofcode.com/"""
import io
import runpy
import sys


__version__ = "2020.1"


def plugin(year, day, data):
    mod_name = "aoc_wim.aoc{}.q{:02d}".format(year, day)
    sys.modules.pop(mod_name, None)
    old_stdout = sys.stdout
    sys.stdout = out = io.StringIO()
    try:
        runpy.run_module(mod_name, run_name="__main__")
    finally:
        sys.stdout = old_stdout
    lines = [x for x in out.getvalue().splitlines() if x]
    if len(lines) == 2:
        part_a, part_b = lines
    elif day == 25 and len(lines) == 1:
        [part_a] = lines
        part_b = None
    else:
        part_a = next((s for s in lines if s.lower().startswith("part a")), None)
        part_b = next((s for s in lines if s.lower().startswith("part b")), None)
    if part_a and part_a.lower().startswith("part a"):
        part_a = part_a.split()[-1]
    if part_b and part_b.lower().startswith("part b"):
        part_b = part_b.split()[-1]
    return part_a, part_b
