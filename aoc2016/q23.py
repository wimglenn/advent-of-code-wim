from aocd import data
from textwrap import dedent


test_data = '''cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a'''


def toggle(line):
    words = line.split()
    if len(words) == 2:
        if line.startswith('inc'):
            line = line.replace('inc', 'dec')
        else:
            line = 'inc ' + words[1]
    elif len(words) == 3:
        if line.startswith('jnz'):
            line = line.replace('jnz', 'cpy')
        else:
            line = ' '.join(['jnz'] + words[1:])
    else:
        # 'mul' and 'pass'
        raise NotImplemented
    return line


def compute(reg, lines, lineno=0, original_data=data, patched_area=()):
    i = lineno
    while i < len(lines):
        line = lines[i]
        if line.startswith('cpy'):
            a, b = line.split()[1:]
            reg[b] = reg[a] if a in reg else int(a)
        elif line.startswith('inc'):
            a = line.split()[1]
            reg[a] += 1
        elif line.startswith('dec'):
            a = line.split()[1]
            reg[a] -= 1
        elif line.startswith('jnz'):
            a, b = line.split()[1:]
            a = reg[a] if a in reg else int(a)
            b = reg[b] if b in reg else int(b)
            if a:
                i += b - 1
                if i in patched_area:
                    lines[:] = original_data.splitlines()
        elif line.startswith('tgl'):
            a = line.split()[1]
            a = reg[a] if a in reg else int(a)
            if 0 <= i + a < len(lines):
                lines[i + a] = toggle(lines[i + a])
        elif line.startswith('pass'):
            pass
        elif line.startswith('mul'):
            a, b, c = line.split()[1:]
            a = reg[a] if a in reg else int(a)
            b = reg[b] if b in reg else int(b)
            reg[c] = a * b
        else:
            raise Exception
        i += 1
    return reg


def part_a(data):
    registers = {}.fromkeys('abcd', 7)
    registers = compute(reg=registers, lines=data.splitlines())
    return registers['a']

def part_b(data):
    registers = {}.fromkeys('abcd', 12)
    patch_target = dedent('''\
        cpy 0 a
        cpy b c
        inc a
        dec c
        jnz c -2
        dec d
        jnz d -5''')
    patch = dedent('''\
        mul b d a
        cpy 0 c
        cpy 0 d
        pass
        pass
        pass
        pass''')
    patch_length = len(patch.splitlines())
    assert patch_length == len(patch_target.splitlines())
    patch_start = len(data[:data.find(patch_target)].splitlines())
    patched_area = range(patch_start + 1, patch_start + 1 + patch_length)
    patched_data = data.replace(patch_target, patch, 1)
    lines = patched_data.splitlines()
    registers = compute(reg=registers, lines=lines, original_data=data, patched_area=patched_area)
    return registers['a']


assert part_a(test_data) == 3
print(part_a(data))  # 10584
print(part_b(data))  # 479007144
