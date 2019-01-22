from aocd import data
import random
from itertools import cycle
from collections import Counter
from bidict import bidict
from termcolor import colored, COLORS


class CartCollision(Exception):
    def __init__(self, coordinates):
        self.coordinates = coordinates
        super().__init__(coordinates)


class Cart:

    vs = bidict(zip("^>v<", [-1j, 1, 1j, -1]))

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
            direction = -1j if self.glyph in "v^" else 1j
        elif track == "/":
            direction = -1j if self.glyph in "><" else 1j
        else:
            return
        self.turn(direction)


def parsed(data):
    grid = {}
    carts = []
    lines = data.splitlines()
    h = len(lines)
    [w] = {len(line) for line in lines}
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char in "v>^<":
                grid[y, x] = "|" if char in "v^" else "-"
                cart = Cart(x, y, glyph=char, color=random.choice(list(COLORS)))
                carts.append(cart)
            elif char != " ":
                grid[y, x] = char
    grid["y-axis"] = range(h)
    grid["x-axis"] = range(w)
    return grid, carts


def dump(grid, carts):
    seen = set()
    carts_on_grid = {}
    prompt = ""
    for cart in carts:
        if cart.coordinates in seen:
            # collision
            prompt = "Collision detected! "
            val = colored("X", "red", attrs=["bold"])
        else:
            val = cart.pretty_glyph
        carts_on_grid[cart.y, cart.x] = val
        seen.add(cart.coordinates)
    print()
    for y in grid["y-axis"]:
        line = []
        for x in grid["x-axis"]:
            pos = (y, x)
            if pos in carts_on_grid:
                line.append(carts_on_grid[pos])
            else:
                line.append(grid.get(pos, " "))
        print(*line, sep="")
    prompt += "Press enter to continue..."
    input(prompt)
    print("\33c")


def find_collision(carts):
    counter = Counter([c.coordinates for c in carts])
    pos = max(counter, key=counter.get)
    if counter[pos] > 1:
        raise CartCollision(pos)


def part_a(data, first_crash=True, debug=False):
    a0, carts = parsed(data)
    while True:
        if debug:
            dump(a0, carts)
        carts.sort()
        for cart in carts:
            cart.tick(grid=a0)
            try:
                find_collision(carts)
            except CartCollision as err:
                if debug:
                    dump(a0, carts)
                if first_crash:
                    return err.coordinates
                # remove exactly 2 crashed carts. there can not be more than
                # one collision at a time because we only moved 1 cart at a
                # time. this is not strictly correct approach because 3 or 4
                # carts could theoretically crash together at an intersection
                carts = [c for c in carts if c.coordinates != err.coordinates]
        if len(carts) == 1:
            [cart] = carts
            return cart.coordinates


def part_b(data, debug=False):
    return part_a(data, first_crash=False, debug=debug)



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


test_data3 = r"""/>-<\  
|   |  
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/"""


assert part_a(test_data1) == "0,3"
assert part_a(test_data2) == "7,3"
assert part_b(test_data3) == "6,4"


print("part a:", part_a(data))
print("part b:", part_b(data))
