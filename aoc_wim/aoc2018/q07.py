"""
--- Day 7: The Sum of Its Parts ---
https://adventofcode.com/2018/day/7
"""
import logging
from types import SimpleNamespace

from aocd import data
from aocd import extra
from parse import parse


log = logging.getLogger(__name__)
# logging.basicConfig(format='%(message)s', level=logging.DEBUG)


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


def work(data, part="a"):
    template = "Step {} must be finished before step {} can begin."
    pairs = [parse(template, s).fixed for s in data.splitlines()]
    remaining = {x for pair in pairs for x in pair}
    n_workers = 1 if part == "a" else extra.get("n_workers", 5)
    delay = extra.get("delay", 60)
    in_progress = set()
    done = set()
    text = ""
    t = -1
    workers = [Worker() for _ in range(n_workers)]
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


print("answer_a:", work(data).text)
print("answer_b:", work(data, part="b").n_iterations)
