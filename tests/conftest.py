import datetime
import re
import pytest
import sys

Module = type(sys)
mock_aocd = Module("aocd")
mock_aocd.data = ""
sys.modules["aocd"] = mock_aocd


def pytest_addoption(parser):
    parser.addoption("--slow", action="store_true", default=0, help="run slow tests")


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
    yyyy_dd = re.compile(r"20\d\d/\d\d")
    for item in items:
        if "slow" in item.nodeid:
            item.add_marker(pytest.mark.slow)
            if not runslow:
                item.add_marker(skip_slow)
        match = yyyy_dd.findall(item.name)
        if match is not None and len(match) == 1:
            [year_day] = match
            year, day = year_day.split("/")
            year = f"y{year}"
            day = f"d{int(day):02}"
            item.add_marker(getattr(pytest.mark, year))
            item.add_marker(getattr(pytest.mark, day))