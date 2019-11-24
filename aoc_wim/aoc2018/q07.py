import logging
from types import SimpleNamespace

from aocd import data
from parse import parse


log = logging.getLogger(__name__)
# logging.basicConfig(format='%(message)s', level=logging.DEBUG)


test_data = """\
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
"""


class Worker:
    def __init__(self):
        self.has = "."  # idle
        self.t = -1

    def tick(self):
        self.t -= 1
        if self.t == 0:
            val = self.has
            self.has = "."
            return val


def work(data, n_workers=4, delay=60):
    template = "Step {} must be finished before step {} can begin."
    pairs = [parse(template, s).fixed for s in data.splitlines()]
    remaining = {x for pair in pairs for x in pair}
    in_progress = set()
    done = set()
    text = ""
    t = -1
    workers = [Worker() for i in range(n_workers)]
    while remaining or in_progress:
        for w in workers:
            x = w.tick()
            if x is not None:
                text += x
                pairs = [pair for pair in pairs if x not in pair]
                in_progress.remove(x)
                done.add(x)
        avail = remaining - {two for one, two in pairs} - in_progress
        log.debug("candidates %d: %s", t, avail)
        for w in workers:
            if w.has == "." and avail:
                w.has = x = min(avail)
                avail.remove(x)
                remaining.remove(x)
                in_progress.add(x)
                if n_workers == 1:
                    w.t = 1
                else:
                    w.t = ord(x) - ord("A") + 1 + delay
        t += 1
        log.debug("%4d: %s   %s", t, " ".join(w.has for w in workers), text)
    result = SimpleNamespace(text=text, n_iterations=t)
    return result


assert work(test_data, n_workers=1, delay=0).text == "CABDFE"
assert work(test_data, n_workers=2, delay=0).n_iterations == 15

print("part a:", work(data, n_workers=1).text)
print("part b:", work(data).n_iterations)
