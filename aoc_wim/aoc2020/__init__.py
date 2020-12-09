import logging


log = logging.getLogger(__name__)


class Comp:

    def __init__(self, ops):
        self.ops = ops  # parsed code
        self.a = 0      # accumulator
        self.line = 0   # instruction pointer into ops
        self.n = 0      # number of instructions exec

    def acc(self, a):
        self.a += a

    def jmp(self, i):
        self.line += i - 1

    def nop(self, _):
        pass

    def step(self):
        self.n += 1
        op, arg = self.ops[self.line]
        op_func = getattr(self, op)
        log.debug(f"{self.n:5}:   {op:3}{arg:4}   L={self.line:3}   a={self.a:4}")
        op_func(arg)
        self.line += 1


def find_pair(counter, target=2020):
    # find a pair of numbers from the multiset (counter) which sums to target
    # if the input is a set, find a pair of *distinct* numbers
    for number in counter:
        diff = target - number
        if diff in counter:
            if diff == number and (isinstance(counter, set) or counter[number] <= 1):
                continue
            return number, diff
