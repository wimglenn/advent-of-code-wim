import logging
from collections import defaultdict
from collections import deque


# logging.basicConfig(level=logging.INFO, format="    %(message)s")
log = logging.getLogger(__name__)

# "parameter modes"
POSITION = 0
IMMEDIATE = 1
RELATIVE = 2


class IntComputer:
    class Halt(Exception):
        pass

    def __init__(self, reg0, inputs=()):
        self.ip = 0
        if not isinstance(reg0, (list, tuple)):
            reg0 = [int(x) for x in reg0.split(",")]
        self.offset = 0
        self.reg = defaultdict(int, dict(enumerate(reg0)))
        self.input = deque(inputs)
        self.output = deque()
        self.modes = [POSITION, POSITION, POSITION]
        self._iterations = 0
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
            9: (self.op_offset, 2),
            99: (self.op_halt, 1),
        }

    def op_offset(self):
        x = self.reg[self.ip + 1]
        if self.modes[0] == POSITION:
            x = self.reg[x]
        elif self.modes[0] == RELATIVE:
            x = self.reg[x + self.offset]
        self.offset += x

    def op_add(self):
        x = self.reg[self.ip + 1]
        if self.modes[0] == POSITION:
            x = self.reg[x]
        elif self.modes[0] == RELATIVE:
            x = self.reg[x + self.offset]
        y = self.reg[self.ip + 2]
        if self.modes[1] == POSITION:
            y = self.reg[y]
        elif self.modes[1] == RELATIVE:
            y = self.reg[y + self.offset]
        if self.modes[2] == RELATIVE:
            self.reg[self.reg[self.ip + 3] + self.offset] = x + y
        else:
            assert self.modes[2] == POSITION
            self.reg[self.reg[self.ip + 3]] = x + y

    def op_mul(self):
        x = self.reg[self.ip + 1]
        if self.modes[0] == POSITION:
            x = self.reg[x]
        elif self.modes[0] == RELATIVE:
            x = self.reg[x + self.offset]
        y = self.reg[self.ip + 2]
        if self.modes[1] == POSITION:
            y = self.reg[y]
        elif self.modes[1] == RELATIVE:
            y = self.reg[y + self.offset]
        if self.modes[2] == RELATIVE:
            self.reg[self.reg[self.ip + 3] + self.offset] = x * y
        else:
            assert self.modes[2] == POSITION
            self.reg[self.reg[self.ip + 3]] = x * y

    def op_input(self):
        # print(self.offset)
        if self.modes[0] == POSITION:
            target = self.reg[self.ip + 1]
        else:
            assert self.modes[0] == RELATIVE
            target = self.reg[self.ip + 1] + self.offset
        self.reg[target] = self.input.pop()

    def op_output(self):
        val = self.reg[self.ip + 1]
        if self.modes[0] == POSITION:
            val = self.reg[val]
        elif self.modes[0] == RELATIVE:
            val = self.reg[val + self.offset]
        self.output.appendleft(val)

    def op_jump_t(self):
        val1 = self.reg[self.ip + 1]
        if self.modes[0] == POSITION:
            val1 = self.reg[val1]
        elif self.modes[0] == RELATIVE:
            val1 = self.reg[val1 + self.offset]
        if not val1:
            return
        val2 = self.reg[self.ip + 2]
        if self.modes[1] == POSITION:
            val2 = self.reg[val2]
        elif self.modes[1] == RELATIVE:
            val2 = self.reg[val2 + self.offset]
        self.ip = val2 - 3

    def op_jump_f(self):
        val1 = self.reg[self.ip + 1]
        if self.modes[0] == POSITION:
            val1 = self.reg[val1]
        elif self.modes[0] == RELATIVE:
            val1 = self.reg[val1 + self.offset]
        if val1:
            return
        val2 = self.reg[self.ip + 2]
        if self.modes[1] == POSITION:
            val2 = self.reg[val2]
        elif self.modes[1] == RELATIVE:
            val2 = self.reg[val2 + self.offset]
        self.ip = val2 - 3

    def op_lt(self):
        val1 = self.reg[self.ip + 1]
        if self.modes[0] == POSITION:
            val1 = self.reg[val1]
        elif self.modes[0] == RELATIVE:
            val1 = self.reg[val1 + self.offset]
        val2 = self.reg[self.ip + 2]
        if self.modes[1] == POSITION:
            val2 = self.reg[val2]
        elif self.modes[1] == RELATIVE:
            val2 = self.reg[val2 + self.offset]
        if self.modes[2] == RELATIVE:
            val3 = self.reg[self.ip + 3] + self.offset
        else:
            val3 = self.reg[self.ip + 3]
        self.reg[val3] = int(val1 < val2)

    def op_eq(self):
        val1 = self.reg[self.ip + 1]
        if self.modes[0] == POSITION:
            val1 = self.reg[val1]
        elif self.modes[0] == RELATIVE:
            val1 = self.reg[val1 + self.offset]
        val2 = self.reg[self.ip + 2]
        if self.modes[1] == POSITION:
            val2 = self.reg[val2]
        elif self.modes[1] == RELATIVE:
            val2 = self.reg[val2 + self.offset]
        if self.modes[2] == RELATIVE:
            val3 = self.reg[self.ip + 3] + self.offset
        else:
            assert self.modes[2] == POSITION
            val3 = self.reg[self.ip + 3]
        self.reg[val3] = int(val1 == val2)

    def op_halt(self):
        raise IntComputer.Halt

    def step(self):
        opcode = self.reg[self.ip]
        modes, opnum = divmod(opcode, 100)
        op, jump = self.op_map[opnum]
        self.modes = [modes // (10 ** n) % 10 for n in range(jump - 1)]
        assert set(self.modes) <= {POSITION, IMMEDIATE, RELATIVE}
        log.info(
            "%d processing ip=%-5d opcode=%-5d op=%-10s jump=%d offset=%-5d modes=%-10s reg=%s",
            self._iterations,
            self.ip,
            opcode,
            op.__name__,
            jump,
            self.offset,
            self.modes,
        )
        self._last_instruction = op.__func__
        op()
        self.ip += jump

    def run(self, until=None):
        while True:
            try:
                self.step()
            except IntComputer.Halt:
                break
            self._iterations += 1
            if self._last_instruction is until:
                break
