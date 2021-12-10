"""Wim's solutions for https://adventofcode.com/"""
import io
import runpy
import sys


__version__ = "2021.10"


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
            if len(line.split()) > 2:
                part_a = line.split()[-1]
            else:
                part_a = ""
        elif line.startswith("part b"):
            if len(line.split()) > 2:
                part_b = line.split()[-1]
            else:
                part_b = ""
    if part_a is not None and part_b is not None:
        return part_a, part_b
    if not lines:
        return None, None
    if len(lines) == 1:
        part_a = lines[0].split()[-1]
    else:
        if part_a is None:
            part_a = lines[-2].split()[-1]
        if part_b is None:
            part_b = lines[-1].split()[-1]
    return part_a, part_b
