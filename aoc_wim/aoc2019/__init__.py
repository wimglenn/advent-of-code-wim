import logging
from collections import deque


# logging.basicConfig(level=logging.INFO, format="    %(message)s")
log = logging.getLogger(__name__)

# "parameter modes"
POSITION = 0
IMMEDIATE = 1


class IntComputer:
    class Halt(Exception):
        pass

    def __init__(self, reg0, inputs=()):
        self.ip = 0
        if not isinstance(reg0, (list, tuple)):
            reg0 = [int(x) for x in reg0.split(",")]
        self.reg = reg0
        self.input = deque(inputs)
        self.output = deque()
        self.modes = [POSITION, POSITION, POSITION]
        self._last_instruction = None
        self.op_map = {
            # opcode: (op, jump)
            1: (self.op_add, 4),
            2: (self.op_mul, 4),
            3: (self.op_input, 2),
            4: (self.op_output, 2),
            5: (self.op_jump_t, 3),
            6: (self.op_jump_f, 3),
            7: (self.op_lt, 4),
            8: (self.op_eq, 4),
            99: (self.op_halt, 1),
        }

    def op_add(self):
        x = self.reg[self.ip + 1]
        if self.modes[0] == POSITION:
            x = self.reg[x]
        y = self.reg[self.ip + 2]
        if self.modes[1] == POSITION:
            y = self.reg[y]
        assert self.modes[2] == POSITION
        self.reg[self.reg[self.ip + 3]] = x + y

    def op_mul(self):
        x = self.reg[self.ip + 1]
        if self.modes[0] == POSITION:
            x = self.reg[x]
        y = self.reg[self.ip + 2]
        if self.modes[1] == POSITION:
            y = self.reg[y]
        assert self.modes[2] == POSITION
        self.reg[self.reg[self.ip + 3]] = x * y

    def op_input(self):
        target = self.reg[self.ip + 1]
        self.reg[target] = self.input.pop()

    def op_output(self):
        val = self.reg[self.ip + 1]
        if self.modes[0] == POSITION:
            val = self.reg[val]
        self.output.appendleft(val)

    def op_jump_t(self):
        val1 = self.reg[self.ip + 1]
        if self.modes[0] == POSITION:
            val1 = self.reg[val1]
        if not val1:
            return
        val2 = self.reg[self.ip + 2]
        if self.modes[1] == POSITION:
            val2 = self.reg[val2]
        self.ip = val2 - 3

    def op_jump_f(self):
        val1 = self.reg[self.ip + 1]
        if self.modes[0] == POSITION:
            val1 = self.reg[val1]
        if val1:
            return
        val2 = self.reg[self.ip + 2]
        if self.modes[1] == POSITION:
            val2 = self.reg[val2]
        self.ip = val2 - 3

    def op_lt(self):
        val1 = self.reg[self.ip + 1]
        if self.modes[0] == POSITION:
            val1 = self.reg[val1]
        val2 = self.reg[self.ip + 2]
        if self.modes[1] == POSITION:
            val2 = self.reg[val2]
        val3 = self.reg[self.ip + 3]
        self.reg[val3] = int(val1 < val2)

    def op_eq(self):
        val1 = self.reg[self.ip + 1]
        if self.modes[0] == POSITION:
            val1 = self.reg[val1]
        val2 = self.reg[self.ip + 2]
        if self.modes[1] == POSITION:
            val2 = self.reg[val2]
        val3 = self.reg[self.ip + 3]
        self.reg[val3] = int(val1 == val2)

    def op_halt(self):
        raise IntComputer.Halt

    def step(self):
        opcode = self.reg[self.ip]
        modes, opnum = divmod(opcode, 100)
        op, jump = self.op_map[opnum]
        self.modes = [modes // (10 ** n) % 10 for n in range(jump)]
        assert set(self.modes) <= {POSITION, IMMEDIATE}
        log.debug("processing opcode=%s op=%s jump=%d", opcode, op.__name__, jump)
        self._last_instruction = op.__func__
        op()
        self.ip += jump

    def run(self, until=None):
        while True:
            try:
                self.step()
            except IntComputer.Halt:
                break
            if self._last_instruction == until:
                break
