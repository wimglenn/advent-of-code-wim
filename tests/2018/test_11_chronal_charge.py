import pytest
from aoc_wim.aoc2018 import q11


@pytest.mark.parametrize("serial_number,x,y,expected_power_level", [
    (8, 3, 5, 4),
    (57, 122, 79, -5),
    (39, 217, 196, 0),
    (71, 101, 153, 4),
])
def test_power_level(x, y, serial_number, expected_power_level):
    grid = q11.gen_grid(serial_number)
    assert grid[y-1, x-1] == expected_power_level


@pytest.mark.parametrize("serial_number,total_power,identifier", [
    (18, 29, (33, 45, 3)),
    (42, 30, (21, 61, 3)),
])
def test_max_power(serial_number, total_power, identifier):
    grid = q11.gen_grid(serial_number)
    assert q11.max_power(grid) == (total_power, *identifier)
