from aocd import data


test_data = '''cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a'''


def compute(data, c=None):
    reg = dict.fromkeys('abcd', 0)
    if c:
        reg['c'] = 1
    i = 0
    lines = data.splitlines()
    while i < len(lines):
        line = lines[i]
        if line.startswith('cpy'):
            a, b = line.split()[1:]
            try:
                a = int(a)
            except ValueError:
                a = reg[a]
            reg[b] = a
        elif line.startswith('inc'):
            a = line.split()[1]
            reg[a] += 1
        elif line.startswith('dec'):
            a = line.split()[1]
            reg[a] -= 1
        if line.startswith('jnz'):
            a, b = line.split()[1:]
            try:
                a = int(a)
            except ValueError:
                a = reg[a]
            b = int(b)
            if a:
                i = i + b
            else:
                i += 1
        else:
            i += 1
    return reg['a']


assert(compute(test_data) == 42)
print(compute(data))
print(compute(data, c=1))
