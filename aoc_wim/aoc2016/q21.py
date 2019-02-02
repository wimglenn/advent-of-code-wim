from aocd import data
from itertools import permutations


test_data = """\
swap position 4 with position 0
swap letter d with letter b
reverse positions 0 through 4
rotate left 1 step
move position 1 to position 4
move position 3 to position 0
rotate based on position of letter b
rotate based on position of letter d"""


def swap_position(list_, words):
    """swap position x with position y"""
    x, y = int(words[0]), int(words[-1])
    list_[x], list_[y] = list_[y], list_[x]

def swap_letter(list_, words):
    """swap letter x with letter y"""
    x, y = words[0], words[-1]
    tr = {x:y, y:x}
    list_[:] = [tr.get(k, k) for k in list_]

def rotate_left(list_, words):
    """rotate left x steps"""
    x = int(words[0])
    list_[:] = list_[x:] + list_[:x]

def rotate_right(list_, words):
    """rotate right x steps"""
    x = int(words[0])
    x = len(list_) - x
    list_[:] = list_[x:] + list_[:x]

def rotate_based(list_, words):
    """rotate based on position of letter x"""
    x = words[-1]
    n = list_.index(x)
    if n >= 4:
        n += 1
    n += 1
    n = len(list_) - n
    list_[:] = list_[n:] + list_[:n]

def reverse_positions(list_, words):
    """reverse positions 0 through 4"""
    x, y = int(words[0]), int(words[-1])
    list_[x:y+1] = list_[x:y+1][::-1]

def move_position(list_, words):
    """move position x to position y"""
    x, y = int(words[0]), int(words[-1])
    if x < y:
        list_.insert(y+1, list_[x])
        del list_[x]
    elif y < x:
        list_.insert(y, list_[x])
        del list_[x+1]

def scramble(data, original):
    list_ = list(original)
    for line in data.splitlines():
        line = line.replace(' ', '_', 1)
        func_name, *words = line.split()
        globals()[func_name](list_, words)
    return ''.join(list_)

def descramble(data, scrambled):
    for original in permutations(scrambled):
        if scramble(data, original) == scrambled:
            return ''.join(original)


assert scramble(test_data, 'abcde') == 'decab'
print(scramble(data, 'abcdefgh'))
print(descramble(data, 'fbgdceah'))
