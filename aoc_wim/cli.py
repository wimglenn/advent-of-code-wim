"""Wim's solutions for https://adventofcode.com/"""
import logging
import os
import runpy
import sys
from argparse import ArgumentParser
from datetime import datetime
from shutil import copy

from aocd.get import most_recent_year
from aocd.models import Puzzle
from aocd.utils import AOC_TZ


def run_one():
    parser = ArgumentParser(description=__doc__)
    aoc_now = datetime.now(tz=AOC_TZ)
    parser.add_argument(
        "day",
        nargs="?",
        type=int,
        choices=range(1, 26),
        default=min(aoc_now.day, 25) if aoc_now.month == 12 else 1,
        help="1-25 (default: %(default)s)",
    )
    parser.add_argument(
        "year",
        nargs="?",
        type=int,
        choices=range(2015, aoc_now.year + int(aoc_now.month == 12)),
        default=most_recent_year(),
        help=">= 2015 (default: %(default)s)",
    )
    parser.add_argument("-d", "--data")
    log_levels = "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
    parser.add_argument("--log-level", choices=log_levels)
    args = parser.parse_args()
    if args.log_level:
        level_int = getattr(logging, args.log_level)
        logging.basicConfig(format="%(message)s", level=level_int)
    mod_name = f"aoc_wim.aoc{args.year}.q{args.day:02d}"
    sys.modules.pop(mod_name, None)
    if args.data is not None:
        os.environ["AOC_SESSION"] = "aocw"
        path = os.path.expanduser("~/.config/aocd/aocw/")
        os.makedirs(path, exist_ok=True)
        path += f"{args.year}_{args.day:02d}_input.txt"
        if os.path.isfile(args.data):
            copy(args.data, path)
        else:
            with open(path, "w") as f:
                print(args.data, file=f)
    print(f"--- {args.year} Day {args.day}: {Puzzle(args.year, args.day).title} ---")
    runpy.run_module(mod_name, run_name="__main__")
