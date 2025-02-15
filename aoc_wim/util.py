import argparse
import ast
import shutil
import sys
import tempfile
import webbrowser
from datetime import datetime
from pathlib import Path
from textwrap import dedent

import aocd
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


def split_trailing_comments(lines):
    extra = []
    while lines and (not lines[-1].strip() or lines[-1].startswith("#")):
        extra.append(lines.pop())
    if len(lines) and "#" in lines[-1]:
        line, comment = lines[-1].split("#", 1)
        lines[-1] = line.strip()
        extra.append(comment.strip())
    if len(lines) > 1 and "#" in lines[-2]:
        line, comment = lines[-2].split("#", 1)
        lines[-2] = line.strip()
        extra.append(comment.strip())
    extra = [x.strip() for x in extra if x.strip()]
    return extra


def parse_extra_context(extra):
    result = {}
    for line in extra:
        equals = line.count("=")
        commas = line.count(",")
        if equals and equals == commas + 1:
            for part in line.split(","):
                k, v = part.strip().split("=")
                k = k.strip()
                v = v.strip()
                try:
                    v = ast.literal_eval(v)
                except ValueError:
                    pass
                if k in result:
                    raise NotImplementedError(f"Duplicate key {k!r}")
                result[k] = v
    return result


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
    src.write_text(
        dedent(
            """\
            from aocd import data
            from aoc_wim.autoparse import parsed
            from collections import Counter, defaultdict, deque
            d = parsed(data)
            if d != data:
                print(d)
                print(f"{parsed.n_bytes} bytes/{parsed.n_lines} lines, parsed by {parsed.parser}")

            # import numpy as np
            # import networkx as nx
            # from aoc_wim.zgrid import ZGrid; grid = ZGrid(data)
            # from aoc_wim import stuff

            # import logging; logging.basicConfig(level=logging.DEBUG)





            print("answer_a:", )
            print("answer_b:", )

            # from aocd import submit; submit(a)
            """
        )
    )
    test = here.parent / "tests" / str(year) / str(day).zfill(2) / "0.txt"
    if not test.exists():
        test.parent.mkdir(parents=True, exist_ok=True)
        test.write_text("\n-\n-\n")
    if block:
        blocker()
    data = aocd.get_data(day=day, year=year, block=True)
    print(data)
    set_docstrings([src])
    puzzle = Puzzle(year, day)
    [example] = puzzle.examples
    if test.read_text() == "\n-\n-\n":
        test.write_text(
            f"{example.input_data}\n"
            f"{example.answer_a or '-'}\n"
            f"{example.answer_b or '-'}\n"
        )
    webbrowser.open(puzzle.url)
