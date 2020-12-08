import logging
from collections import deque


log = logging.getLogger(__name__)


class Comp:

    def __init__(self, data, pid=None, ch_snd=None, ch_rcv=None, a0=0):
        self.code = [x.split() for x in data.splitlines()]
        self.reg = {r: 0 for op, r, *rest in self.code}
        self.reg.pop("1", None)
        self.reg = dict(sorted(self.reg.items()))
        self.pid = pid
        if self.pid is not None:
            self.reg["p"] = pid
        self.reg["a"] = a0
        if ch_snd is None:
            ch_snd = deque()
        if ch_rcv is None:
            ch_rcv = deque()
        self.ch_snd = ch_snd
        self.ch_rcv = ch_rcv
        self.line = 0
        self.n = 0
        self.n_snd = 0
        self.n_mul = 0

    def snd(self, x):
        if x in self.reg or self.pid is not None:
            self.n_snd += 1
            try:
                self.ch_snd.append(self.reg[x])
            except KeyError:
                return

    def rcv(self, x):
        if self.reg[x] or self.pid is not None:
            self.reg[x] = self.ch_rcv.popleft()

    def set(self, x, y):
        self.reg[x] = y

    def add(self, x, y):
        self.reg[x] += y

    def mul(self, x, y):
        self.reg[x] *= y
        self.n_mul += 1

    def mod(self, x, y):
        self.reg[x] %= y

    def jgz(self, x, y):
        x = self.reg[x] if x in self.reg else int(x)
        if x > 0:
            self.line += y - 1

    def sub(self, x, y):
        self.reg[x] -= y

    def jnz(self, x, y):
        x = self.reg[x] if x in self.reg else int(x)
        if x:
            self.line += y - 1

    def wtf(self, x, y):
        self.reg[x] = all(y % i for i in range(2, y))

    def blocked(self):
        if not (0 <= self.line < len(self.code)):
            return True
        if self.code[self.line][0] == "rcv" and not self.ch_rcv:
            return True

    def step(self):
        self.n += 1
        op, r, *args = self.code[self.line]
        op_func = getattr(self, op)
        if args:
            [y] = args
            y = self.reg[y] if y in self.reg else int(y)
            args = y,
        else:
            y = "."
        log.debug(f"{self.pid} {self.n:5}:   L{self.line:03d} {op:3} {r:1} {y:14}   snd={self.ch_snd[-1] if self.ch_snd else '':4}   rcv={self.ch_rcv[-1] if self.ch_rcv else '':4}  {self.reg}  n_mul={self.n_mul}")
        op_func(r, *args)
        self.line += 1
