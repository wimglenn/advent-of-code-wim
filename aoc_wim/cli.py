"""Wim's solutions for https://adventofcode.com/"""
import logging
import runpy
import subprocess
import sys
from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path

import aocd
from aocd.models import Puzzle
from aocd.utils import AOC_TZ


def run_one():
    parser = ArgumentParser(description=__doc__)
    aoc_now = datetime.now(tz=AOC_TZ)
    days = range(1, 26)
    years = range(2015, aoc_now.year + int(aoc_now.month == 12))
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
    parser.add_argument("-d", "--data", help="string or file to monkeypatch in aocd.data")
    log_levels = "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
    parser.add_argument("--log-level", type=str.upper, choices=log_levels)
    args = parser.parse_args()
    if args.day in years and args.year in days:
        args.day, args.year = args.year, args.day
    if args.log_level:
        level_int = getattr(logging, args.log_level)
        logging.basicConfig(format="%(message)s", level=level_int)
    mod_name = f"aoc_wim.aoc{args.year}.q{args.day:02d}"
    sys.modules.pop(mod_name, None)
    if args.data is not None:
        if args.data.endswith("txt"):
            path = Path(args.data)
            if path.is_file():
                txt = path.read_text()
                if "tests" in path.parts:
                    args.data = "\n".join(txt.splitlines()[:-2])
                else:
                    args.data = txt
        aocd.data = args.data
    print(f"--- {args.year} Day {args.day}: {Puzzle(args.year, args.day).title} ---")
    runpy.run_module(mod_name, run_name="__main__")


def speedhack():
    here = Path(__file__).parent
    aoc_now = datetime.now(tz=AOC_TZ)
    if aoc_now.month != 12:
        sys.exit("It's not December yet")
    year = aoc_now.year
    day = aoc_now.day
    test_dir = here.parent / "tests" / str(year) / str(day).zfill(2)
    examples = sorted(test_dir.glob("*.txt"))
    puzzle = Puzzle(year, day)
    print(f"--- {year} Day {day}: {puzzle.title} ---")
    print(puzzle.url)
    if examples:
        print(f"{len(examples)} example(s) to test...")
        args = [sys.executable, "-m", "pytest", "-k", f"{year}/{day:02d}"]
        subprocess.check_call(args)
    args = ["aoc", "-y", str(year), "-d", str(day), "-u", "github.wimglenn.119932", "-r", "--log-level", "DEBUG", "--timeout", "600"]
    print("\n" + " ".join(args))
    subprocess.check_call(args)
