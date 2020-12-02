import pytest
from aoc_wim.aoc2016 import q20


test_data = """\
5-8
0-2
4-7"""


@pytest.fixture
def clean_test_data():
    return q20.cleanup_data(test_data)


def test_lowest_ip_allowed(clean_test_data):
    assert q20.part_a(clean_test_data) == 3


def test_number_of_ips_allowed(clean_test_data):
    assert q20.part_b(clean_test_data, n_min=0, n_max=9) == 2
