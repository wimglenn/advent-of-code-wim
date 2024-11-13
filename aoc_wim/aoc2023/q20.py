"""
--- Day 20: Pulse Propagation ---
https://adventofcode.com/2023/day/20
"""

from aocd import data
from collections import deque
import logging
import math


# logging.basicConfig(format="%(message)s", level=logging.DEBUG)
log = logging.getLogger(__name__)


pending = deque([])


class Module:
    def __init__(self, pk):
        self.pk = pk
        self.dsts = []
        self.reset()

    def reset(self):
        self._state = 0
        self._n_sent = [0, 0]
        self._recv = []
        self.disabled = False

    @classmethod
    def from_str(cls, s):
        s0, pk = s[:1], s[1:]
        if s0 == "%":
            return FlipFlop(pk)
        elif s0 == "&":
            return Conjunction(pk)
        else:
            return Module(s)

    def connect(self, dst):
        self.dsts.append(dst)
        if isinstance(dst, Conjunction):
            dst.register(self)

    def send(self):
        if self.disabled:
            log.debug("%s is disabled - not sending", self.pk)
            return
        for dst in self.dsts:
            log.debug("%s -%s-> %s", self.pk, "high" if self._state else "low", dst.pk)
            pending.append((self.pk, self._state, dst.pk))
            self._n_sent[self._state] += 1

    def recv(self, pulse, sender_id):
        if self.pk == "output" or self.pk == "rx":
            self._recv.append((pulse, sender_id))
        elif self.pk == "broadcaster":
            self.send()

    def __repr__(self):
        return f"<{type(self).__name__}({self.pk}) {self._state}>"


class FlipFlop(Module):

    def recv(self, pulse, sender_id):
        if self.disabled:
            return
        if pulse:
            return
        self._state = 1 - self._state
        self.send()


class Conjunction(Module):
    def __init__(self, pk):
        super().__init__(pk)
        self.memory = {}

    def register(self, src):
        self.memory[src.pk] = 0

    def recv(self, pulse, sender_id):
        if self.disabled:
            return
        self.memory[sender_id] = pulse
        self.send()

    @property
    def _state(self):
        return 1 - all(self.memory.values())

    @_state.setter
    def _state(self, val):
        return


modules = {}
lines = sorted(data.splitlines(), key=lambda line: (line[0], len(line)))
for line in lines:
    src, _dsts = line.split(" -> ")
    mod = Module.from_str(src)
    modules[mod.pk] = mod
for line in lines:
    src, dsts = line.split(" -> ")
    src = modules[src.lstrip("%&")]
    for dst in dsts.split(", "):
        if dst not in modules:
            modules[dst] = Module(dst)
        src.connect(modules[dst])
button = modules["button"] = Module("button")
button.dsts.append(modules["broadcaster"])

for i in range(1000):
    button.send()
    while pending:
        src_pk, pulse, dst_pk = pending.popleft()
        modules[dst_pk].recv(pulse, src_pk)

n_low_sent = sum(m._n_sent[0] for m in modules.values())
n_high_sent = sum(m._n_sent[1] for m in modules.values())
a = n_low_sent * n_high_sent
print("answer_a:", a)

# dsts of broadcaster, only enable one at a time
periods = []
broadcasted = modules["broadcaster"].dsts
for branch in broadcasted:
    for m in modules.values():
        m.reset()
        if m in broadcasted and m is not branch:
            m.disabled = True
    s0 = tuple(m._state for m in modules.values())
    seen = set()
    i = 0
    while True:
        button.send()
        while pending:
            src_pk, pulse, dst_pk = pending.popleft()
            modules[dst_pk].recv(pulse, src_pk)
        i += 1
        state = tuple(m._state for m in modules.values())
        if state in seen:
            periods.append(i - 1)
            break
        seen.add(state)
b = math.lcm(*periods)
print("answer_b:", b)
