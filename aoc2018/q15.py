from aocd import data
from collections import deque
from termcolor import colored
from operator import attrgetter
from time import sleep


class CombatEnds(Exception):
    pass


class Unit:
    grid = None
    ap = None
    glyph = 'U'

    def __init__(self, pos, id):
        self.id = id
        self.pos = pos
        self.hp = 200

    @property
    def yx(self):
        return int(self.pos.imag), int(self.pos.real)

    @property
    def alive(self):
        return self.hp > 0

    @property
    def targets(self):
        units = self.grid["units"]
        result = [u for u in units if u.alive and u.glyph != self.glyph]
        if not result:
            raise CombatEnds
        return result

    @property
    def targets_adjacent(self):
        return [u for u in self.targets if abs(u.pos - self.pos) == 1]

    @property
    def targets_with_available_squares(self):
        return [u for u in self.targets if u.available_squares]

    @property
    def available_squares(self):
        units = self.grid["units"]
        candidates = [self.pos - 1j, self.pos -1, self.pos + 1, self.pos + 1j]
        not_wall = [c for c in candidates if self.grid.get(c, "#") != "#"]
        unit_positions = {u.pos for u in units if u.alive}
        avail = [c for c in not_wall if c not in unit_positions]
        return avail

    def attack(self, other):
        assert abs(self.pos - other.pos) == 1
        assert other.alive
        other.hp -= self.ap

    def move(self):
        new_pos_choices = self.available_squares
        assert new_pos_choices
        ops = self.targets_with_available_squares
        if not ops:
            return
        target_positions = {pos for o in ops for pos in o.available_squares}
        assert target_positions
        units = self.grid["units"]
        others_positions = {o.pos for o in units if o.alive and o is not self}
        state0 = self.pos
        found = bfs(state0, targets=target_positions, grid=self.grid, others_positions=others_positions)
        if not found:
            return
        [shortest_path] = {d for (pos, d) in found}
        target_positions = [pos for (pos, d) in found]
        target_positions.sort(key=lambda pos: (pos.imag, pos.real))
        target_pos = target_positions[0]
        distances = {}
        for choice in new_pos_choices:
            found = bfs(choice, targets={target_pos}, grid=self.grid, others_positions=others_positions)
            [(t, distances[choice])] = found
            assert t == target_pos
        min_dist = min(distances.values())
        assert min_dist == shortest_path - 1
        choices = [c for (c, d) in distances.items() if d == min_dist]
        choices.sort(key=lambda pos: (pos.imag, pos.real))
        new_pos = choices[0]
        assert abs(self.pos - new_pos) == 1
        self.pos = new_pos

    @property
    def opponent(self):
        ops = self.targets_adjacent
        if ops:
            min_hp = min([o.hp for o in ops])
            ops = [o for o in ops if o.hp == min_hp]
            ops.sort(key=attrgetter('yx'))
            return ops[0]

    def act(self):
        op = self.opponent
        if op is not None:
            self.attack(other=op)
            return
        places = self.available_squares
        if not places:
            return
        self.move()
        op = self.opponent
        if op is not None:
            self.attack(other=op)
            return


class Elf(Unit):
    glyph = 'E'
    cglyph = colored(glyph, 'green', attrs=["bold"])
    ap = 3


class Goblin(Unit):
    glyph = 'G'
    cglyph = colored(glyph, 'red', attrs=["bold"])
    ap = 3


def dump(grid, round=0, interactive=False, dt=0.1):
    print("\33c")
    units = grid["units"]
    units_on_grid = {}
    for unit in units:
        if unit.alive:
            units_on_grid[unit.pos] = unit
    print()
    if round:
        print(f"After {round} round{'s' if round > 1 else ''}:")
    else:
        print("Initially:")
    for y in grid["y-axis"]:
        line = []
        units_on_line = []
        for x in grid["x-axis"]:
            pos = complex(x, y)
            if pos in units_on_grid:
                unit = units_on_grid[pos]
                line.append(unit.cglyph)
                units_on_line.append(unit)
            else:
                line.append(grid[pos])
        print(*line, sep="", end='')
        if units_on_line:
            units_str = ', '.join([f'{u.cglyph}({u.hp})' for u in units_on_line])
            print("   " + units_str)
        else:
            print()
    if interactive:
        input("Press enter to continue ...")
    else:
        sleep(dt)


def parsed(data):
    grid = {}
    lines = data.splitlines()
    h = len(lines)
    [w] = {len(x) for x in lines}
    grid['y-axis'] = range(h)
    grid['x-axis'] = range(w)
    uid = 0
    units = []
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            pos = complex(x, y)
            if char in "#.":
                grid[pos] = char
            elif char == "G":
                g = Goblin(id=uid, pos=pos)
                units.append(g)
                grid[pos] = "."
                uid += 1
            elif char == "E":
                e = Elf(id=uid, pos=pos)
                units.append(e)
                grid[pos] = "."
                uid += 1
    grid['units'] = units
    return grid


def bfs(state0, targets, grid, others_positions):
    depth = 0
    queue = deque([(state0, depth)])
    seen = {state0}
    i = 0
    found = set()
    shortest_path = None
    while queue:
        state, new_depth = queue.popleft()
        i += 1
        if new_depth > depth:
            depth = new_depth
            if shortest_path is not None and depth > shortest_path:
                assert found
                return found
        if state in targets:
            if shortest_path is not None:
                assert shortest_path == depth
            shortest_path = depth
            found.add((state, depth))
        candidates = [state - 1j, state -1, state + 1, state + 1j]
        ok = [c for c in candidates if grid.get(c, "#") != "#" and c not in others_positions and c not in seen]
        queue.extend((child, depth + 1) for child in ok)
        seen.update(ok)
    return found


def part_a(data, debug=False):
    Unit.grid = grid = parsed(data)
    round = 0
    units = grid["units"]
    n_elves = sum(1 for u in units if isinstance(u, Elf))
    while True:
        if debug:
            dump(grid, round)
        units.sort(key=attrgetter("yx"))
        for unit in units:
            if unit.alive:
                try:
                    unit.act()
                except CombatEnds:
                    score = sum(u.hp for u in units if u.alive)
                    n_elves_alive = sum(1 for u in units if isinstance(u, Elf) and u.alive)
                    part_a.all_elves_alive = n_elves == n_elves_alive
                    return round * score
        round += 1


def part_b(data, debug=False):
    Elf.ap = 3
    while True:
        Elf.ap += 1
        outcome = part_a(data, debug=debug)
        if part_a.all_elves_alive:
            Elf.ap = 3
            return outcome


part_a_tests = """\
#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######

27730

#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######

36334

#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######

39514

#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######

27755

#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######

28944

#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########

18740"""


tests = part_a_tests.split('\n\n')
grids = tests[0::2]
outcomes = [int(line) for line in tests[1::2]]
for grid, outcome in zip(grids, outcomes):
    assert part_a(grid) == outcome

part_b_tests = [4988, 31284, 3478, 6474, 1140]
del grids[1]  # wtf eric
for grid, outcome in zip(grids, part_b_tests):
    assert part_b(grid) == outcome


print("part a:", part_a(data))
print("part b:", part_b(data))
