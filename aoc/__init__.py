import io
import runpy
import sys

from aocd.post import AocdError
from aocd.post import get_answer
from aocd.post import submit


def wim(year, day, data, autosubmit=True):
    mod_name = "aoc{}.q{:02d}".format(year, day)
    sys.modules.pop(mod_name, None)
    old_stdout = sys.stdout
    sys.stdout = out = io.StringIO()
    try:
        runpy.run_module(mod_name, run_name="__main__")
    finally:
        sys.stdout = old_stdout
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
    if autosubmit:
        for (answer, level) in [(part_a, 1), (part_b, 2)]:
            expected = get_answer(day=day, year=year, level=level)
            if answer and expected is None:
                try:
                    submit(answer, day=day, year=year, reopen=False, quiet=True, level=level)
                except AocdError:
                    pass
    return part_a, part_b
