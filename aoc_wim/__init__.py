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
    part_a = part_b = None
    for line in lines:
        if line.startswith("part a"):
            part_a = line.split()[-1]
        elif line.startswith("part b"):
            part_b = line.split()[-1]
    if part_a and part_b:
        return part_a, part_b
    if not lines:
        return None, None
    if len(lines) == 1:
        part_a = lines[0].split()[-1]
    else:
        part_a = lines[-2].split()[-1]
        part_b = lines[-1].split()[-1]
    return part_a, part_b
