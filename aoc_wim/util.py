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
from aocd.get import most_recent_year
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
    years = range(2015, aoc_now.year + int(aoc_now.month == 12))
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
        default=most_recent_year(),
        help="2015-{} (default: %(default)s)".format(years[-1]),
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
    if day < 25 and year == aoc_now.year and day == aoc_now.day:
        if src.exists() and str(day) not in sys.argv:
            day += 1
            blocker()
            src = here / f"aoc{year}" / f"q{day:02d}.py"
    if src.exists():
        if not args.force:
            sys.exit(f"{src} already exists!")
        shutil.copy2(src, tempfile.gettempdir())
    src.write_text(dedent('''\
        from aocd import data
        from collections import *

        # import numpy as np
        # import networkx as nx

        tdata = """\\
        """
        # data = tdata





        print("part a:", )
        print("part b:", )
    '''))
    test = here / "tests" / str(year) / str(day) / "a.txt"
    if not test.exists():
        test.parent.mkdir(parents=True, exist_ok=True)
        test.touch(exist_ok=True)
    data = get_data(day=day, year=year)
    print(data)
    set_docstrings([src])
    webbrowser.open(Puzzle(year, day).url)
