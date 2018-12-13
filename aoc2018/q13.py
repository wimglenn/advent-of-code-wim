from aocd import data, submit1
import numpy as np
from itertools import cycle
from collections import Counter


class CartCollision(Exception):

    def __init__(self, coordinates, submit=False):
        self.coordinates = coordinates
        if submit:
            submit1(coordinates)
        super().__init__(coordinates)


class Cart:

    def __init__(self, row, col, glyph):
        self.row = row
        self.col = col
        self.glyph = glyph
        self.turns = cycle('LSR')

    @property
    def coordinates(self):
        return f"{self.col},{self.row}"  # x,y

    @property
    def v_row(self):
        if self.glyph == 'v':
            return 1
        elif self.glyph == '>':
            return 0
        elif self.glyph == '^':
            return -1
        else:
            assert self.glyph == '<'
            return 0

    @property
    def v_col(self):
        if self.glyph == 'v':
            return 0
        elif self.glyph == '>':
            return 1
        elif self.glyph == '^':
            return 0
        else:
            assert self.glyph == '<'
            return -1

    def turn_left(self):
        self.glyph = {
            ">": "^",
            "^": "<",
            "<": "v",
            "v": ">",
        }[self.glyph]

    def turn_right(self):
        self.glyph = {
            ">": "v",
            "v": "<",
            "<": "^",
            "^": ">",
        }[self.glyph]

    def step(self, grid):
        self.row += self.v_row
        self.col += self.v_col
        x = grid[self.row, self.col]
        assert x in r"+/-\|"
        if x == "+":
            turn = next(self.turns)
            if turn == "L":
                self.turn_left()
            elif turn == "R":
                self.turn_right()
        elif x == "\\":
            if self.glyph in "><":
                self.turn_right()
            else:
                assert self.glyph in "v^"
                self.turn_left()
        elif x == "/":
            if self.glyph in "><":
                self.turn_left()
            else:
                assert self.glyph in "v^"
                self.turn_right()


def parsed(data):
    a = np.array([list(line) for line in data.splitlines()], dtype="|U1")
    carts = []
    for glyph in "v>^<":
        rows, cols = np.where(a==glyph)
        for row, col in zip(rows, cols):
            cart = Cart(row, col, glyph)
            carts.append(cart)
            if cart.glyph in "<>":
                a[cart.row, cart.col] = '-'
            else:
                assert cart.glyph in '^v'
                a[cart.row, cart.col] = '|'
    return a, carts


def dump(a, carts):
    a = a.copy()
    for cart in carts:
        a[cart.row, cart.col] = cart.glyph
    print()
    for row in a:
        print(*row, sep='')
    print()


def find_collision(carts):
    counter = Counter([(c.row, c.col) for c in carts])
    pos = max(counter, key=counter.get)
    if counter[pos] > 1:
        coordinates = f"{pos[1]},{pos[0]}"
        raise CartCollision(coordinates)


def run(data, part):
    a0, carts = parsed(data)
    while True:
        carts.sort(key=lambda c: (c.row, c.col))
        for cart in carts:
            cart.step(grid=a0)
            try:
                find_collision(carts)
            except CartCollision as err:
                if part == "a":
                    return err.coordinates
                # remove crashed carts
                carts = [c for c in carts if c.coordinates != err.coordinates]
        if len(carts) == 1:
            [cart] = carts
            return cart.coordinates


test_data1 = """|
v
|
|
|
^
|"""


test_data2 = r"""/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   """


assert run(test_data1, part="a") == "0,3"
assert run(test_data2, part="a") == "7,3"

assert run(data, part="a") == "113,136"
assert run(data, part="b") == "114,136"

# print(run(data, part="a"))  # 113,136
# print(run(data, part="b"))  # 114,136
