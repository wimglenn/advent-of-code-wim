import logging
from aocd import data


log = logging.getLogger(__name__)
# logging.basicConfig(level=logging.INFO, format="%(message)s")


class AssembunnyComputer:

    def __init__(self, source, c=0):
        self.i = 0
        self.lines = source.splitlines()
        self.reg = dict.fromkeys("abcd", 0)
        self.reg["c"] = c

    def run(self):
        while True:
            try:
                self.step()
            except IndexError:
                return

    def step(self):
        line = self.lines[self.i]
        log.debug("i=%02d %-8s %s", self.i, line, self.reg)
        op, *args = line.split()

        if op == "inc":
            asm = self.lines[self.i:self.i+3]
            if len(asm) == 3 and asm[1].startswith("dec"):
                _, r_inc = asm[0].split()
                _, r_dec = asm[1].split()
                if asm[2].startswith("jnz"):
                    _, r_cond, j = asm[2].split()
                    if j == "-2" and r_cond == r_dec:
                        if self.reg[r_cond] > 0:
                            add = self.reg[r_cond]
                            log.info("patching out loop: %s += %d", r_inc, add)
                            self.reg[r_inc] += add
                            self.i += 3
                            return

        getattr(self, op)(*args)
        self.i += 1

    def cpy(self, x, y):
        self.reg[y] = self.reg[x] if x in self.reg else int(x)

    def jnz(self, x, y):
        x = self.reg[x] if x in self.reg else int(x)
        if x:
            self.i += int(y) - 1

    def dec(self, r):
        self.reg[r] -= 1

    def inc(self, r):
        self.reg[r] += 1


comp = AssembunnyComputer(data)
comp.run()
print("part a", comp.reg["a"])
comp.__init__(data, c=1)
comp.run()
print("part b", comp.reg["a"])
