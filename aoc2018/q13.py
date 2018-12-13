from aocd import data, submit1
import random
import numpy as np
from itertools import cycle
from collections import Counter
from bidict import bidict
from termcolor import colored, COLORS


class CartCollision(Exception):

    def __init__(self, coordinates, submit=False):
        self.coordinates = coordinates
        if submit:
            submit1(coordinates)
        super().__init__(coordinates)


class Cart:

    vs = bidict(zip('^>v<', [-1j, 1, 1j, -1]))

    def __init__(self, x, y, glyph, color=None):
        self.glyph = glyph
        self._position = complex(x, y)
        self._turns = cycle([-1j, 1, 1j])  # left, straight, right
        self.color = color

    def __repr__(self):
        return f"<Cart {self.pretty_glyph} at {self.coordinates}>"

    def __lt__(self, other):
        if not isinstance(other, Cart):
            return NotImplemented
        return (self.y, self.x) < (other.y, other.x)

    @property
    def pretty_glyph(self):
        return colored(self.glyph, self.color, attrs=["bold"])

    @property
    def velocity(self):
        return self.vs[self.glyph]

    @property
    def y(self):
        # row
        return int(self._position.imag)

    @property
    def x(self):
        # column
        return int(self._position.real)

    @property
    def coordinates(self):
        return f"{self.x},{self.y}"

    def turn(self, direction=None):
        if direction is None:
            direction = next(self._turns)
        v = self.velocity * direction
        self.glyph = self.vs.inv[v]

    def tick(self, grid):
        # dump(grid, carts=[self])
        self._position += self.velocity
        track = grid[self.y, self.x]
        assert track in r"+/-\|", f"WTF: {self} ran off the rails"
        if track == "+":
            direction = None
        elif track == "\\":
            direction = -1j if self.glyph in 'v^' else 1j
        elif track == "/":
            direction = -1j if self.glyph in '><' else 1j
        else:
            return
        self.turn(direction)


def parsed(data):
    a = np.array([list(line) for line in data.splitlines()], dtype="<U20")
    carts = []
    for glyph in "v>^<":
        ys, xs = np.where(a==glyph)
        for y, x in zip(ys, xs):
            cart = Cart(x, y, glyph, color=random.choice(list(COLORS)))
            carts.append(cart)
            if cart.glyph in "<>":
                a[cart.y, cart.x] = '-'
            else:
                assert cart.glyph in '^v'
                a[cart.y, cart.x] = '|'
    return a, carts


def dump(a, carts):
    a = a.copy()
    seen = set()
    for cart in carts:
        if cart.coordinates in seen:
            # collision
            val = colored("X", "red", attrs=["bold"])
        else:
            val = cart.pretty_glyph
        a[cart.y, cart.x] = val
        seen.add(cart.coordinates)
    print()
    for row in a:
        print(*row, sep='')
    print()
    return a


def find_collision(carts):
    counter = Counter([(c.y, c.x) for c in carts])
    pos = max(counter, key=counter.get)
    if counter[pos] > 1:
        coordinates = f"{pos[1]},{pos[0]}"
        raise CartCollision(coordinates)


def run(data, part_b=False):
    a0, carts = parsed(data)
    while True:
        # dump(a0, carts)
        carts.sort()
        for cart in carts:
            cart.tick(grid=a0)
            try:
                find_collision(carts)
            except CartCollision as err:
                if not part_b:
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


assert run(test_data1) == "0,3"
assert run(test_data2) == "7,3"

print(run(data, part_b=False))  # 113,136
print(run(data, part_b=True))   # 114,136
