"""
--- Day 25: Cryostasis ---
https://adventofcode.com/2019/day/25
"""
import logging
from collections import deque
import anytree
from aocd import data
from aoc_wim.aoc2019 import IntComputer
from itertools import combinations
from wimpy.util import cached_property


log = logging.getLogger(__name__)


def parse_room(txt):
    txt = txt.strip()
    lines = txt.splitlines()
    if len(lines) < 3:
        log.warning("failed to parse output\n%r", txt)
        raise Exception
    first, description, *rest, last = lines
    if not first.startswith("==") or not last.startswith("Command?"):
        log.warning("failed to parse output\n%r", txt)
        raise Exception
    name = first.strip("= ")
    doors = []
    items = []
    section = None
    for line in rest:
        line = line.strip()
        if not line:
            continue
        if line == "Doors here lead:":
            section = doors
            continue
        if line == "Items here:":
            section = items
            continue
        if line.startswith("- "):
            line = line[2:]
            section.append(line)
            continue
        if not line.startswith("Command?"):
            log.info("suffix: %s", line)
    doors = {}.fromkeys(doors)
    result = {"name": name, "description": description, "doors": doors, "items": items}
    return result


class Room(anytree.NodeMixin):
    def __init__(self, name, description, doors, items):
        self.name = name
        self.description = description
        self.doors = doors
        self.items = items

    def __repr__(self):
        return f"<Room({self.name})>"


class Game:
    def __init__(self):
        self.comp = IntComputer(data)
        self.root = None
        self.comp.input = self
        self.command_queue = deque()
        self.shortcuts = {
            "n": "north",
            "s": "south",
            "e": "east",
            "w": "west",
            "\x1b[A": "north",
            "\x1b[B": "south",
            "\x1b[C": "east",
            "\x1b[D": "west",
        }
        self.inverse = {
            "north": "south",
            "south": "north",
            "east": "west",
            "west": "east",
        }
        self.rooms = {}
        self.current_room = None
        self.prev_direction = None
        self.prev_room = None
        self.inventory = set()
        self.mode = "explore"  # or "unlock"
        self.combo = None

    def shortest_path(self, to):
        to_path = to.path
        path = []
        for room in reversed(self.current_room.path):
            if room in to_path:
                to_path = to_path[to_path.index(room):]
                path.extend(to_path)
                break
            path.append(room)
        return path

    def find_path(self, to=None):
        last_step = None
        if to is None:
            # just go to any unexplored room...
            for room in self.rooms.values():
                if room.name == "Security Checkpoint":
                    continue
                if any(v is None for v in room.doors.values()):
                    to = room
                    last_step = next(k for k, v in room.doors.items() if v is None)
                    break
            else:
                return
        intermediate_rooms = self.shortest_path(to=to)
        path = []
        for left, right in zip(intermediate_rooms, intermediate_rooms[1:]):
            direction = next(d for d, r in left.doors.items() if r is right)
            path.append(direction)
        if last_step is not None:
            path.append(last_step)
        if not path:
            # can happen if you try to find path to room but you're already there
            return
        first_step = path[0]
        return first_step

    @cached_property
    def combos(self):
        data = {}
        inventory = sorted(self.inventory)
        for i in range(len(inventory)):
            for combo in combinations(inventory, i):
                data[combo] = "new"
        return data

    @cached_property
    def unlock_direction(self):
        return next(k for k, v in self.current_room.doors.items() if v is None)

    def pop(self):
        if not self.command_queue:
            # command queue is exhausted, need to update status and find task to do
            command = ""
            output = self.comp.output_as_text

            # entered a room
            if output.strip().startswith("=="):
                parsed_room = parse_room(output)
                here = parsed_room["name"]
                if here == "Pressure-Sensitive Floor":
                    if "ejected" in output:
                        if "Droids on this ship are heavier" in output:
                            self.combos[self.combo] = "too light"
                            self.combo = None
                        elif "Droids on this ship are lighter" in output:
                            self.combos[self.combo] = "too heavy"
                            self.combo = None
                        else:
                            log.warning("shouldn't be here: %r", output)
                log.debug("parsed room data: %s", parsed_room)
                if here not in self.rooms:
                    log.debug("entered new room %r, adding to graph", parsed_room)
                    new_room = self.rooms[here] = Room(**parsed_room)
                    if self.prev_room is not None:
                        new_room.parent = self.prev_room
                        back = self.inverse[self.prev_direction]
                        new_room.doors[back] = self.prev_room
                        self.prev_room.doors[self.prev_direction] = new_room
                    else:
                        self.root = new_room

                self.current_room = self.rooms[here]
                if here == "Pressure-Sensitive Floor":
                    if "ejected" in output:
                        # actually we got kicked out
                        self.current_room = self.rooms["Security Checkpoint"]

            # update inventory of self and rooms
            for line in output.splitlines():
                if line.startswith("You take the "):
                    item = line[13:-1]
                    self.current_room.items.remove(item)
                    self.inventory.add(item)
                if line.startswith("You drop the "):
                    item = line[13:-1]
                    self.inventory.remove(item)
                    self.current_room.items.append(item)

            # echo on
            self.comp.output.clear()
            print(output, end="", flush=True)

            # pick up any crap we find lying around
            if self.mode == "explore":
                for item in self.current_room.items:
                    if item not in blacklist:
                        log.info("autotaking %r", item)
                        command += f"take {item}\n"

            # there was nothing to take, explore around the ship
            if self.mode == "explore" and not command:
                step = self.find_path()
                if step is not None:
                    command = step
                else:
                    # we've explored everything, proceed to checkpoint
                    self.mode = "unlock"
                    command = self.find_path(to=self.rooms["Security Checkpoint"])
                if command is None:
                    command = "inv"
                else:
                    self.prev_direction = command
                    self.prev_room = self.current_room
                log.info("entering command %r", command)

            # continue proceeding to checkpoint
            if self.mode == "unlock":
                if self.current_room.name != "Security Checkpoint":
                    command = self.find_path(to=self.rooms["Security Checkpoint"])
                    self.prev_direction = command
                    self.prev_room = self.current_room

            if self.mode == "unlock" and not command:
                assert self.current_room.name == "Security Checkpoint"
                if self.combo is None:
                    self.combo = next(k for k, v in self.combos.items() if v == "new")
                combo = set(self.combo)
                diff = combo ^ self.inventory
                for item in diff:
                    if item in self.inventory:
                        command = f"drop {item}"
                    else:
                        assert item in combo and item not in self.inventory
                        command = f"take {item}"
                    break
                else:
                    assert combo == self.inventory
                    log.info("trying combo %s", combo)
                    command = self.prev_direction = self.unlock_direction
                    self.prev_room = self.current_room

            # don't know what to do
            if not command:
                # interactive fallback
                command = input()

            if not command:
                # so that pressing "enter" at the prompt adds some useful context
                if self.root:
                    print(anytree.RenderTree(self.root))
                print("current room:", self.current_room.name)
                print(self.current_room.description)
                print("doors:", "/".join(self.current_room.doors))
                print("inventory:", ", ".join(sorted(self.inventory)))

            # a convenience shortcut to take the item here
            if command == "t" and len(self.current_room.items) == 1:
                [item] = self.current_room.items
                command = f"take {item}"

            # allows to use the arrow keys or enter just "n" instead of typing "north"
            command = self.shortcuts.get(command, command)
            if not command.endswith("\n"):
                command += "\n"

            for char in command:
                self.command_queue.appendleft(ord(char))

        return self.command_queue.pop()

    def play(self):
        self.comp.run()
        txt = self.comp.output_as_text
        if "Analysis complete! You may proceed." not in txt:
            log.warning("should be done but: %r", txt)
            raise Exception
        [code] = [word for word in txt.split() if word.isdigit()]
        print("part a", code)


# traps .. don't pick up this crap
blacklist = [
    "photons",
    "infinite loop",
    "molten lava",
    "giant electromagnet",
    "escape pod",
]

game = Game()
game.play()
