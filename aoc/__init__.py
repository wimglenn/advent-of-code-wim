import runpy
import sys
from io import StringIO
from contextlib import redirect_stdout


def wim(year, day, data):
    mod_name = f"aoc{year}.q{day:02d}"
    sys.modules.pop(mod_name, None)
    out = StringIO()
    with redirect_stdout(out):
        runpy.run_module(mod_name, run_name="__main__")
    output_lines = [x for x in out.getvalue().splitlines() if x]
    if len(output_lines) == 2:
        part_a, part_b = output_lines
    elif day == 25 and len(output_lines) == 1:
        [part_a] = output_lines
        part_b = None
    else:
        part_a = next((s for s in output_lines if s.lower().startswith("part a:")), None)
        part_b = next((s for s in output_lines if s.lower().startswith("part b:")), None)
    if part_a and part_a.lower().startswith("part a:"):
        part_a = part_a[7:].strip()
    if part_b and part_b.lower().startswith("part b:"):
        part_b = part_b[7:].strip()
    return part_a, part_b
