import logging
import sys


# logging.basicConfig(level=logging.INFO, format="    %(message)s")
log = logging.getLogger(__name__)

# "parameter modes"
POSITION = 0
IMMEDIATE = 1


class IntComputer:
    class Halt(Exception):
        pass

    class CatchFire(Exception):
        pass

    def __init__(self, reg0, input=input, output=sys.stdout):
        self.input = input
        self.output = output
        self.op_modes = [POSITION, POSITION, POSITION]
        self.ip = 0
        self.reg = reg0
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

    @classmethod
    def fromsource(cls, data):
        reg0 = [int(x) for x in data.split(",")]
        comp = cls(reg0)
        return comp

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
        val = self.reg[self.ip + 1]
        self.reg[val] = int(self.input("IntComputer input --> "))

    def op_output(self):
        val = self.reg[self.ip + 1]
        if self.modes[0] == POSITION:
            val = self.reg[val]
        print(val, file=self.output)

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
        op, jump = self.op_map[opcode % 100]
        self.modes = [int(x) for x in reversed(str(opcode // 100).zfill(jump))]
        assert set(self.modes) <= {POSITION, IMMEDIATE}
        log.debug("processing opcode=%s op=%s jump=%d", opcode, op.__name__, jump)
        op()
        self.ip += jump

    def run(self, max_i=5000):
        i = 0
        while True:
            try:
                self.step()
            except IntComputer.Halt:
                break
            i += 1
            if i > max_i:
                raise IntComputer.CatchFire
