import logging
from multiprocessing import current_process
from _md5 import md5
from functools import partial
import re


log = logging.getLogger(__name__)
# logging.basicConfig(format="%(message)s", level=logging.INFO)


class AssembunnyComputer:
    def __init__(self, source, a0=0, b0=0, c0=0, d0=0):
        self.i = 0
        self.lines = source.splitlines()
        self.reg = {"a": a0, "b": b0, "c": c0, "d": d0}

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
            asm = self.lines[self.i : self.i + 3]
            if len(asm) == 3 and asm[1].startswith("dec"):
                _, r_inc = asm[0].split()
                _, r_dec = asm[1].split()
                if asm[2].startswith("jnz"):
                    _, r_cond, j = asm[2].split()
                    if j == "-2" and r_cond == r_dec:
                        if self.reg[r_cond] > 0:
                            add = self.reg[r_cond]
                            msg = "patching out iadd loop (lines %d-%d): %s += %d"
                            log.info(msg, self.i, self.i + 2, r_inc, add)
                            self.reg[r_inc] += add
                            self.reg[r_cond] = 0
                            self.i += 3
                            return

        if op == "cpy" and self.lines[self.i : self.i + 6] == [
            "cpy b c",
            "inc a",
            "dec c",
            "jnz c -2",
            "dec d",
            "jnz d -5",
        ]:
            msg = "patching out multiply double loop (lines %d-%d): a += b * d"
            log.info(msg, self.i, self.i + 6)
            self.reg["a"] += self.reg["b"] * self.reg["d"]
            self.reg["c"] = self.reg["d"] = 0
            self.i += 6
            return

        getattr(self, op)(*args)
        self.i += 1

    def cpy(self, x, y):
        self.reg[y] = self.reg[x] if x in self.reg else int(x)

    def jnz(self, x, y):
        x = self.reg[x] if x in self.reg else int(x)
        y = self.reg[y] if y in self.reg else int(y)
        if x:
            self.i += y - 1

    def dec(self, r):
        self.reg[r] -= 1

    def inc(self, r):
        self.reg[r] += 1

    def tgl(self, di):
        di = self.reg[di] if di in self.reg else int(di)
        i = self.i + di
        try:
            line = self.lines[i]
        except IndexError:
            # If an attempt is made to toggle an instruction
            # outside the program, nothing happens
            return
        op, *args = line.split()
        if len(args) == 1:
            # For one-argument instructions, inc becomes dec,
            # and all other one-argument instructions become inc.
            op = "dec" if op == "inc" else "inc"
        elif len(args) == 2:
            # For two-argument instructions, jnz becomes cpy,
            # and all other two-instructions become jnz.
            op = "cpy" if op == "jnz" else "jnz"
        self.lines[i] = " ".join([op, *args])


def md5_miner(data, i0, n, keep, stretch=None, verbose=False):
    pid = current_process().pid
    if verbose:
        print(f"MD5 miner start {i0=} {pid=}")
    h0 = md5(data.encode("ascii")).copy
    results = []
    for i in range(i0, i0 + n):
        hash_ = h0()
        hash_.update(b"%d" % i)
        result = hash_.hexdigest()
        if stretch is not None:
            result = result.encode()
            for _ in range(stretch - 1):
                result = md5(result).hexdigest().encode()
            result = result.decode()
        if keep(result):
            results.append((i, result))
    mined = len(results)
    if verbose:
        print(f"MD5 miner stop  {i0=} {pid=} {mined=}")
    return results


def _keep_q05(digest, difficulty=5):
    return digest.startswith("0" * difficulty)


def _keep_q14(digest):
    pat3 = re.compile(r"(.)\1{2}")
    return pat3.search(digest) is not None


md5_miner_q05 = partial(md5_miner, keep=_keep_q05)
md5_miner_q14a = partial(md5_miner, keep=_keep_q14)
md5_miner_q14b = partial(md5_miner, keep=_keep_q14, stretch=2017)
