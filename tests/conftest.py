import datetime
import json
import os
import re
import sys
import warnings

import pytest


class MockAocd(type(sys)):
    def __getattr__(self, name):
        if name == "extra":
            return json.loads(os.environ.get("AOCD_EXTRA", "{}"))
        if name == "data":
            return ""
        raise AttributeError(name)

    def submit(self, *args, **kwargs):
        msg = f"Submission is disabled during test"
        if len(args) == 1 and not kwargs:
            msg += f" ({args[0]!r})"
        else:
            msg += f" ({args=} {kwargs=})"
        warnings.warn(msg)


sys.modules["aocd"] = MockAocd("aocd")


def pytest_addoption(parser):
    parser.addoption("--slow", action="store_true", default=0, help="run slow tests")
    parser.addoption("--part-a-only", action="store_true", default=0, help="don't assert on part b result")


def pytest_configure(config):
    msg = """slow: marks tests as slow (deselect with '-m "not slow"')"""
    config.addinivalue_line("markers", msg)
    for year in range(2015, datetime.date.today().year + 1):
        msg = f"y{year}: https://adventofcode.com/{year}"
        config.addinivalue_line("markers", msg)
    for day in range(1, 26):
        msg = f"d{day:02d}: https://adventofcode.com/*/day/{day:02d}"
        config.addinivalue_line("markers", msg)


def pytest_collection_modifyitems(config, items):
    runslow = config.getoption("--slow")
    skip_slow = pytest.mark.skip(reason="need --slow option to run")
    yyyy_dd = re.compile(r"20[0-9]{2}/[0-2][0-9]]")
    for item in items:
        if "slow" in item.nodeid:
            item.add_marker(pytest.mark.slow)
            if not runslow:
                item.add_marker(skip_slow)
        if "broken" in item.nodeid:
            item.add_marker(pytest.mark.skip(reason="the code can't solve this case yet"))
        match = yyyy_dd.findall(item.name)
        if match is not None and len(match) == 1:
            [year_day] = match
            year, day = year_day.split("/")
            item.add_marker(getattr(pytest.mark, f"y{year}"))
            item.add_marker(getattr(pytest.mark, f"d{int(day):02}"))
