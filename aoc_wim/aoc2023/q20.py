"""
--- Day 20: Pulse Propagation ---
https://adventofcode.com/2023/day/20
"""
from aocd import data
from collections import deque
import logging
import networkx as nx


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
        if self.pk == "output" or self.pk == "rx":
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


modules = {}
module_types = {
    "%": FlipFlop,
    "&": Conjunction,
}


g = nx.DiGraph()
lines = sorted(data.splitlines(), key=lambda line: (line[0], len(line)))
for line in lines:
    src, _dsts = line.split(" -> ")
    ModuleType = module_types.get(src[0], Module)
    pk = src.lstrip("%&")
    modules[pk] = ModuleType(pk)
for line in lines:
    src, dsts = line.split(" -> ")
    src = modules[src.lstrip("%&")]
    for dst in dsts.split(", "):
        if dst not in modules:
            modules[dst] = Module(dst)
        g.add_edge(src.pk, dst)
        src.connect(modules[dst])
button = modules["button"] = Module("button")
button.dsts.append(modules["broadcaster"])
g.add_edge("button", "broadcaster")

groups = [{*nx.descendants(g, n), n} - {"dt", "rx"} for n in nx.neighbors(g, 'broadcaster')]

def module_sort_key(item):
    pk, mod = item
    t1 = type(mod).__name__.replace("M", "A")
    for t0, group in enumerate(groups, 1):
        if pk in group:
            break
    else:
        t0 = 0
    t2 = -nx.shortest_path_length(g, 'button', pk)
    t3 = nx.shortest_path_length(g, pk, 'rx')
    return t0, t1, t2, t3


modules = dict(sorted(modules.items(), key=module_sort_key))


def serialize_state(i=0):
    result = [m._state for m in modules.values()]
    result.insert(-14*4, "|")
    result.insert(-14*3, "|")
    result.insert(-14*2, "|")
    result.insert(-14*1, "|")
    print(f"{i: 4d}:", *result)
    return result


initial_state = serialize_state()
# seen = {initial_state: 0}
i = 0
period = None
while period is None:
    button.send()
    while net:
        src_pk, pulse, dst_pk = net.popleft()
        modules[dst_pk].recv(pulse, src_pk)
    i += 1
    state = serialize_state(i)
    # if state not in seen:
    #     seen[state] = i
    if state == initial_state:
        period = i

print(period)
f = 1000 // period
n_low_sent = sum(m._n_sent[0] for m in modules.values())
n_high_sent = sum(m._n_sent[1] for m in modules.values())
a = n_low_sent * f * n_high_sent * f

print("answer_a:", a)
print("answer_b:", )

# from aocd import submit; submit(a)
