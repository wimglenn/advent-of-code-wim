from aocd import data


test_data = """\
cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a"""


def compute(data, c=0):
    reg = {}.fromkeys("abcd", 0)
    reg["c"] = c
    i = 0
    lines = data.splitlines()
    while i < len(lines):
        line = lines[i]
        if line.startswith("cpy"):
            a, b = line.split()[1:]
            reg[b] = reg[a] if a in reg else int(a)
        elif line.startswith("inc"):
            a = line.split()[1]
            reg[a] += 1
        elif line.startswith("dec"):
            a = line.split()[1]
            reg[a] -= 1
        elif line.startswith("jnz"):
            a, b = line.split()[1:]
            a = reg[a] if a in reg else int(a)
            if a:
                i += int(b) - 1
        i += 1
    return reg["a"]


assert compute(test_data) == 42
print(compute(data))  # 318007
print(compute(data, c=1))  # 9227661
