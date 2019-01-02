from argparse import ArgumentParser
from concurrent.futures import ProcessPoolExecutor
from contextlib import redirect_stderr
from contextlib import redirect_stdout
from datetime import datetime
from importlib import import_module
from io import StringIO
from pkg_resources import iter_entry_points

from aocd import AOC_TZ
from aocd import get_data
from aocd import get_answer
from aocd import PuzzleUnsolvedError
from termcolor import cprint
from time import time


def main():
    users = {ep.name: ep for ep in iter_entry_points(group='aoc')}
    aoc_now = datetime.now(tz=AOC_TZ)
    all_years = range(2015, aoc_now.year + int(aoc_now.month == 12))
    all_days = range(1, 26)
    parser = ArgumentParser("AoC runner")
    parser.add_argument("-u", "--users", choices=users)
    parser.add_argument("-y", "--years", type=int, nargs="+", choices=all_years)
    parser.add_argument("-d", "--days", type=int, nargs="+", choices=all_days)
    parser.add_argument("-p", "--parts", nargs="+", choices="ab")
    parser.add_argument("-t", "--timeout", type=int, default=30)
    parser.add_argument("-v", "--verbose", action="store_true")
    # parser.add_argument("--data")  # TODO: allow custom data for 1 endpoint
    args = parser.parse_args()
    run_for(
        users=args.users or list(users),
        years=args.years or all_years,
        days=args.days or all_days,
        parts=args.parts or "ab",
        timeout=args.timeout,
        verbose=args.verbose,
    )


def run_with_timeout(func, t=30, *args, **kwargs):
    with ProcessPoolExecutor() as p:
        future = p.submit(func, *args, **kwargs)
        result = future.result(timeout=t)
        return result


def run_for(users, years, days, parts, timeout=30, verbose=False):
    entry_points = {ep.name: ep for ep in iter_entry_points(group='aoc') if ep.name in users}
    for year in years:
        print(f"Year: {year}")
        print("----------")
        for day in days:
            print(f"Day {day:<2d}", end=" ", flush=True)
            # TODO: run on multiple days
            data = get_data(day=day, year=year)
            # TODO: handle days not yet released yet during AoC
            for user in users:
                print(user, end="  ", flush=True)
                for part in parts:
                    entry_point = entry_points[user]
                    expected = None
                    level = {"a": 1, "b": 2}[part]
                    try:
                        expected = get_answer(day=day, year=year, level=level)
                    except PuzzleUnsolvedError:
                        pass
                    out = StringIO()
                    err = StringIO()
                    t0 = time()
                    try:
                        with redirect_stdout(out), redirect_stderr(err):
                            result = run_with_timeout(
                                entry_point.load(),
                                t=timeout,
                                year=year,
                                day=day,
                                part=part,
                                data=data,
                                verbose=verbose,
                            )
                    except Exception as err:
                        result = repr(err)
                    t = time() - t0  # wall time
                    if isinstance(result, Exception):
                        cprint("💩", "red", end=" ", flush=True)
                    elif expected is None:
                        cprint(" ?", "magenta", end=" ", flush=True)
                    else:
                        if str(result) == str(expected):
                            cprint(f" ✔ {t: 3.2f}s", "green", end=" ", flush=True)
                        else:
                            cprint(f" ✖ {t: 3.2f}s", "red", end=" ", flush=True)
                    print(f"part {part}: {result}".ljust(40), end=" ", flush=True)
                    if str(result) != str(expected):
                        print("expected result:", expected, end=" ", flush=True)
                print()


def wim(year, day, part, data, verbose=False):
    mod = import_module(f"aoc{year}.q{day:02d}")
    try:
        attr = getattr(mod, f"part_{part}")
    except AttributeError:
        both = getattr(mod, "part_ab")
        answers = dict(zip("ab", both(data)))
        answer = answers[part]
    else:
        if callable(attr):
            answer = attr(data)
        else:
            answer = attr
    return answer
