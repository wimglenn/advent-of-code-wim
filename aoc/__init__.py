import itertools
import json
import logging
import os
import runpy
import sys
from argparse import ArgumentParser
from contextlib import redirect_stdout
from datetime import datetime
from io import StringIO
from pathlib import Path
from pkg_resources import iter_entry_points

import pebble
from aocd import AOC_TZ
from aocd import get_cookie
from aocd import get_data
from aocd import get_answer
from aocd import PuzzleUnsolvedError
from aocd import submit
from termcolor import colored
from time import time
from wimpy import strip_prefix


# from https://adventofcode.com/about
# every problem has a solution that completes in at most 15 seconds on ten-year-old hardware


def main():
    users = {ep.name: ep for ep in iter_entry_points(group='aoc')}
    aoc_now = datetime.now(tz=AOC_TZ)
    all_years = range(2015, aoc_now.year + int(aoc_now.month == 12))
    all_days = range(1, 26)
    path = Path("~/.config/aocd/tokens.json").expanduser()
    try:
        all_datasets = json.loads(path.read_text())
    except FileNotFoundError:
        all_datasets = {"default": get_cookie()}
    parser = ArgumentParser("AoC runner")
    parser.add_argument("-u", "--users", choices=users)
    parser.add_argument("-y", "--years", type=int, nargs="+", choices=all_years)
    parser.add_argument("-d", "--days", type=int, nargs="+", choices=all_days)
    parser.add_argument("-D", "--data", nargs="+", choices=all_datasets)
    parser.add_argument("-t", "--timeout", type=int, default=300)
    parser.add_argument("--log-level", default="WARNING", choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    # parser.add_argument("--data")  # TODO: allow custom data for 1 endpoint
    args = parser.parse_args()
    logging.basicConfig(level=getattr(logging, args.log_level))
    run_for(
        users=args.users or list(users),
        years=args.years or all_years,
        days=args.days or all_days,
        datasets={k: all_datasets[k] for k in (args.data or all_datasets)},
        timeout=args.timeout,
    )


def call_with_timeout(func, timeout, **kwargs):
    # TODO : multi-process over the different tokens
    pool = pebble.ProcessPool(max_workers=1)
    with pool:
        future = pool.schedule(func, kwargs=kwargs, timeout=timeout)
        return future.result()


def run_for(users, years, days, datasets, timeout=300, autosubmit=True):
    aoc_now = datetime.now(tz=AOC_TZ)
    entry_points = {ep.name: ep for ep in iter_entry_points(group='aoc') if ep.name in users}
    it = itertools.product(years, days, users, datasets)
    template = (
        "{runtime}   {year}/{day:<2d}   {user}/{dataset}   "
        "{a_icon} part a: {part_a_answer} "
        "{b_icon} part b: {part_b_answer}"
    )
    for year, day, user, dataset in it:
        if year == aoc_now.year and day > aoc_now.day:
            continue
        token = os.environ["AOC_SESSION"] = datasets[dataset]
        data = get_data(day=day, year=year, session=token)
        entry_point = entry_points[user]
        t0 = time()
        crashed = False
        try:
            result = call_with_timeout(
                entry_point.load(),
                timeout=timeout,
                year=year,
                day=day,
                data=data,
            )
        except Exception as err:
            a = b = repr(err)
            crashed = True
        else:
            a, b = result
        t = time() - t0  # wall time
        expected_a = expected_b = None
        try:
            expected_a = get_answer(day=day, year=year, session=token, level=1)
        except PuzzleUnsolvedError:
            pass
        if expected_a is None and autosubmit and not crashed:
            submit(a, day=day, year=year, session=token, reopen=False, quiet=True, level=1)
            try:
                expected_a = get_answer(day=day, year=year, session=token, level=1)
            except PuzzleUnsolvedError:
                pass
        try:
            expected_b = get_answer(day=day, year=year, session=token, level=2)
        except PuzzleUnsolvedError:
            pass
        if expected_b is None and autosubmit and not crashed:
            submit(b, day=day, year=year, session=token, reopen=False, quiet=True, level=2)
            try:
                expected_b = get_answer(day=day, year=year, session=token, level=2)
            except PuzzleUnsolvedError:
                pass
        a_correct = str(expected_a) == a
        b_correct = str(expected_b) == b
        a_icon = colored("✔", "green") if a_correct else colored("✖", "red")
        b_icon = colored("✔", "green") if b_correct else colored("✖", "red")
        if t < 15:
            runtime = colored(f"{t:.2f}s", "green")
        elif t < 60:
            runtime = colored(f"{t:.2f}s", "yellow")
        else:
            runtime = colored(f"{t:.2f}s", "red")
        a_correction = b_correction = ""
        if not a_correct:
            if expected_a is None:
                a_icon = colored("?", "magenta")
                a_correction = "(correct answer is unknown)"
            else:
                a_correction = f"(expected: {expected_a})"
        if not b_correct:
            if expected_b is None:
                b_icon = colored("?", "magenta")
                b_correction = "(correct answer is unknown)"
            else:
                b_correction = f"(expected: {expected_b})"
        part_a_answer = f"{a} {a_correction}"
        part_b_answer = f"{b} {b_correction}"
        line = template.format(
            runtime=runtime.rjust(16), year=year, day=day, user=user, dataset=dataset,
            a_icon=a_icon, part_a_answer=part_a_answer.ljust(30),
            b_icon=b_icon, part_b_answer=part_b_answer,
        )
        if day == 25:
            # there's no part b on christmas day
            line = line.split(b_icon)[0].rstrip()
        print(line)


def wim(year, day, data):
    mod_name = f"aoc{year}.q{day:02d}"
    sys.modules.pop(mod_name, None)
    out = StringIO()
    with redirect_stdout(out):
        runpy.run_module(mod_name, run_name="__main__")
    output_lines = [x for x in out.getvalue().splitlines() if x]
    # TODO: parse for "part a: ", "part b: "
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
