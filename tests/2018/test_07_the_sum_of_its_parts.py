from aoc_wim.aoc2018 import q07

test_data = """\
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
"""


def test_order():
    assert q07.work(test_data, n_workers=1, delay=0).text == "CABDFE"


def test_duration():
    assert q07.work(test_data, n_workers=2, delay=0).n_iterations == 15
