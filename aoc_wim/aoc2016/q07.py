import re

from aocd import data


def splitter(s):
    pattern = r"\[([a-z]*)\]"
    ins = re.findall(pattern, s)
    outs = re.sub(pattern, " ", s).split()
    return ins, outs


def chunker(s, size):
    i = 0
    while len(s[i : i + size]) == size:
        yield s[i : i + size]
        i += 1


def has_abba(s):
    for a, b, b_, a_ in chunker(s, 4):
        if a == a_ and b == b_ and a != b:
            return True
    return False


def gen_aba(s):
    for a, b, a_ in chunker(s, 3):
        if a == a_ and a != b:
            yield a + b + a


def has_aba(s):
    return bool(next(gen_aba(s), False))


def support_tls(s):
    ins, outs = splitter(s)
    return has_abba(".".join(outs)) and not has_abba(".".join(ins))


def support_ssl(s):
    ins, outs = splitter(s)
    for a, b, a in gen_aba("..".join(ins)):
        bab = b + a + b
        if bab in "..".join(outs):
            return True
    return False


assert support_tls("abba[mnop]qrst")
assert not support_tls("abcd[bddb]xyyx")
assert not support_tls("aaaa[qwer]tyui")
assert support_tls("ioxxoj[asdfgh]zxcvbn")

assert support_ssl("aba[bab]xyz")
assert not support_ssl("xyx[xyx]xyx")
assert support_ssl("aaa[kek]eke")
assert support_ssl("zazbz[bzb]cdb")


tls = ssl = 0
for line in data.splitlines():
    tls += support_tls(line)
    ssl += support_ssl(line)

print(tls)  # 115
print(ssl)  # 231
