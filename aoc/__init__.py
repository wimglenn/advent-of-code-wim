from argparse import ArgumentParser
from datetime import datetime
from importlib import import_module
from pkg_resources import iter_entry_points

from aocd import AOC_TZ
from aocd import get_data
from aocd import get_answer
from aocd import PuzzleUnsolvedError
from termcolor import cprint


users = {}


def main():
    for ep in iter_entry_points(group='aoc'):
        users[ep.name] = ep.load()
    aoc_now = datetime.now(tz=AOC_TZ)
    parser = ArgumentParser("AoC runner")
    parser.add_argument("user", choices=users)
    parser.add_argument("year", type=int, choices=range(2015, aoc_now.year + 1))
    parser.add_argument("day", type=int, choices=range(1, 26))
    parser.add_argument("part", choices="ab")
    parser.add_argument("--data")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()
    ep = users[args.user]
    ep(year=args.year, day=args.day, part=args.part, data=args.data, verbose=args.verbose)


def wim(year, day, part, data=None, verbose=False):
    mod = import_module(f"aoc{year}.q{day:02d}")
    if data is None:
        data = get_data(day=day, year=year)
    func = getattr(mod, f"part_{part}")
    try:
        result = func(data)
    except Exception as err:
        result = err
    level = {"a": 1, "b": 2}[part]
    try:
        expected = get_answer(day=day, year=year, level=level)
    except PuzzleUnsolvedError:
        expected = None
    if isinstance(result, Exception):
        cprint("💩", "red")
    elif expected is None:
        cprint("?", "magenta")
    else:
        if str(result) == str(expected):
            cprint("✔", "green")
        else:
            cprint("✖", "red")
    print("wim result", result)
    print("expected result", expected)
