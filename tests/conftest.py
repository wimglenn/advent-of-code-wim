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
    config.addinivalue_line("markers", "year(arg): particular AoC year (2015+)")
    config.addinivalue_line("markers", "day(arg): particular AoC day (1-25)")


def pytest_collection_modifyitems(config, items):
    runslow = config.getoption("--slow")
    skip_slow = pytest.mark.skip(reason="need --slow option to run")
    yyyy_dd = re.compile(r"20\d\d_\d\d")
    for item in items:
        if "slow" in item.nodeid:
            item.add_marker(pytest.mark.slow)
            if not runslow:
                item.add_marker(skip_slow)
        match = yyyy_dd.findall(item.name)
        if match is not None and len(match) == 1:
            [year_day] = match
            year, day = year_day.split("_")
            item.add_marker(pytest.mark.year(int(year)))
            item.add_marker(pytest.mark.day(int(day)))
    # for item in items:
    #     print(item.nodeid)
    #     print(*list(item.iter_markers()), sep="\n")
    #     print()
