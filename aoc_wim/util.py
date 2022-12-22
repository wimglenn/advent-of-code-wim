import argparse
import ast
import shutil
import sys
import tempfile
import webbrowser
from pathlib import Path
from datetime import datetime
from textwrap import dedent

from aocd import get_data
from aocd.models import Puzzle
from aocd.utils import AOC_TZ
from aocd.utils import blocker


here = Path(__file__).parent.resolve()


def get_module_docstring(path):
    """get a .py file docstring, without actually executing the file"""
    with open(path) as f:
        return ast.get_docstring(ast.parse(f.read()))


def set_module_docstring(path, text):
    """update docstring of file at path with text, cautiously"""
    prev = get_module_docstring(path)
    if prev == text:
        # nothing to do
        return
    if prev is not None:
        print(repr(text))
        print(repr(prev))
        raise Exception(f"refusing to clobber existing docstring on {path}")
    content = Path(path).read_text()
    Path(path).write_text(f'"""\n{text}\n"""\n{content}')


def set_docstrings(files=()):
    """puts name and link into puzzle source files"""
    for file in files or here.glob("aoc*/q*.py"):
        day = int(file.name[1:3])
        year = int(file.parent.name[3:])
        puzzle = Puzzle(year, day)
        docstring = f"--- Day {day}: {puzzle.title} ---\n"
        docstring += puzzle.url
        set_module_docstring(file, docstring)


def start():
    """init a new source file at ./aocYYYY/qDD.py"""
    aoc_now = datetime.now(tz=AOC_TZ)
    years = range(2015, aoc_now.year + int(aoc_now.month >= 11))
    days = range(1, 26)
    parser = argparse.ArgumentParser(description="init current day")
    parser.add_argument(
        "day",
        nargs="?",
        type=int,
        default=min(aoc_now.day, 25) if aoc_now.month == 12 else 1,
        help="1-25 (default: %(default)s)",
    )
    parser.add_argument(
        "year",
        nargs="?",
        type=int,
        default=years[-1],
        help="2015-%(default)s (default: %(default)s)",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="create the template file even if source already exists",
    )
    args = parser.parse_args()
    if args.day in years and args.year in days:
        # be forgiving
        args.day, args.year = args.year, args.day
    if args.day not in days or args.year not in years:
        parser.print_usage()
        parser.exit(1)
    year = args.year
    day = args.day
    here = Path(__file__).parent
    src = here / f"aoc{year}" / f"q{day:02d}.py"
    block = False
    if day < 25 and year == aoc_now.year and day == aoc_now.day:
        if src.exists() and str(day) not in sys.argv:
            day += 1
            block = True
            src = here / f"aoc{year}" / f"q{day:02d}.py"
    if src.exists():
        if not args.force:
            sys.exit(f"{src} already exists! (use -f to overwrite)")
        shutil.copy2(src, tempfile.gettempdir())
    if day == 1 and not src.parent.is_dir():
        src.parent.mkdir()
        src.parent.joinpath("__init__.py").touch()
    src.write_text(dedent('''\
        from aocd import data
        from aoc_wim.autoparse import parsed
        from collections import Counter, defaultdict, deque
        d = parsed(data)
        if d != data:
            print(d)
            print(f"{parsed.n_bytes} bytes/{parsed.n_lines} lines, parsed by {parsed.parser}")

        # import numpy as np
        # import networkx as nx
        # from aoc_wim.zgrid import ZGrid
        # from aoc_wim import stuff

        # import logging; logging.basicConfig(level=logging.DEBUG)






        print("part a:", )
        print("part b:", )
    '''))
    test = here.parent / "tests" / str(year) / str(day).zfill(2) / "a.txt"
    if not test.exists():
        test.parent.mkdir(parents=True, exist_ok=True)
        test.write_text("\n-\n-\n")
    if block:
        blocker()
    data = get_data(day=day, year=year, block=True)
    print(data)
    set_docstrings([src])
    puzzle = Puzzle(year, day)
    if test.read_text() == "\n-\n-\n":
        test.write_text("{}\n-\n-\n".format(puzzle.example_data))
    webbrowser.open(puzzle.url)
