"""
--- Day 20: Pulse Propagation ---
https://adventofcode.com/2023/day/20
"""
from aocd import data
from collections import deque
import logging


# logging.basicConfig(format="%(message)s", level=logging.DEBUG)


log = logging.getLogger(__name__)


net = deque([])


class Module:
    def __init__(self, pk):
        self.pk = pk
        self.dsts = []
        self._state = 0
        self._n_sent = [0, 0]
        self._recv = []

    def connect(self, dst):
        self.dsts.append(dst)
        if isinstance(dst, Conjunction):
            dst.register(self)

    def send(self):
        for dst in self.dsts:
            log.debug("%s -%s-> %s", self.pk, 'high' if self._state else 'low', dst.pk)
            net.append((self.pk, self._state, dst.pk))
            self._n_sent[self._state] += 1

    def recv(self, pulse, sender_id):
        if self.pk == "output":
            self._recv.append((pulse, sender_id))
        elif self.pk == "broadcaster":
            self.send()

    def __repr__(self):
        return f"<{type(self).__name__}({self.pk}) {self._state}>"


class FlipFlop(Module):
    def __init__(self, pk):
        super().__init__(pk)
        self._n_flips = 0

    def recv(self, pulse, sender_id):
        if pulse:
            return
        self._state = 1 - self._state
        self._n_flips += 1
        self.send()


class Conjunction(Module):
    def __init__(self, pk):
        super().__init__(pk)
        self.memory = {}

    def register(self, src):
        self.memory[src.pk] = 0

    def recv(self, pulse, sender_id):
        self.memory[sender_id] = pulse
        self.send()

    @property
    def _state(self):
        return 1 - all(self.memory.values())

    @_state.setter
    def _state(self, val):
        return


# modules = dict.fromkeys(["gx", "mg", "cb", "mt", "ng", "hd", "vh", "pb", "lt", "zn", "vj", "xg", "xz", "gb", "pp", "kx", "fl", "gk", "tr", "qx", "lj", "cn", "lq", "bc", "vn", "vx", "vl", "vf", "zr", "cd", "kk", "zt", "lz", "qn", "rr", "hq", "sb", "xv", "rl", "bf", "qm", "jg", "gc", "tv", "tx", "hk", "jr", "qz"])
modules = {}
module_types = {
    "%": FlipFlop,
    "&": Conjunction,
}


lines = sorted(data.splitlines(), key=lambda line: (line[0], len(line)))
for line in lines:
    src, _ = line.split(" -> ")
    ModuleType = module_types.get(src[0], Module)
    pk = src.lstrip("%&")
    modules[pk] = ModuleType(pk)
for line in lines:
    src, dsts = line.split(" -> ")
    src = modules[src.lstrip("%&")]
    for dst in dsts.split(", "):
        if dst not in modules:
            modules[dst] = Module(dst)
        src.connect(modules[dst])
button = modules["button"] = Module("button")
button.dsts.append(modules["broadcaster"])


def serialize_state(i=0):
    result = tuple(m._state for m in modules.values())
    print(f"{i}:", *result)
    return result


initial_state = serialize_state()
seen = {initial_state: 0}
i = 0
period = None
while period is None:
    button.send()
    while net:
        src_pk, pulse, dst_pk = net.popleft()
        modules[dst_pk].recv(pulse, src_pk)
    i += 1
    state = serialize_state(i)
    if state not in seen:
        seen[state] = i
        print(f"{len(seen)=}")
    if state == initial_state:
        period = i

f = 1000 // period
n_low_sent = sum(m._n_sent[0] for m in modules.values())
n_high_sent = sum(m._n_sent[1] for m in modules.values())
a = n_low_sent * f * n_high_sent * f

print("answer_a:", a)
print("answer_b:", )

# from aocd import submit; submit(a)
