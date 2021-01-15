"""
--- Day 24: Immune System Simulator 20XX ---
https://adventofcode.com/2018/day/24
"""
import logging
from operator import attrgetter

from aocd import data
from parse import parse
from wimpy import strip_prefix


log = logging.getLogger(__name__)
# logging.basicConfig(format="%(message)s", level=logging.DEBUG)


class StaleMate(Exception):
    """Neither infection nor immune can deal damage to eachother"""


class System:
    def __init__(self, name, text, boost=0):
        self.name = name
        self.groups = []
        for i, line in enumerate(text.splitlines(), start=1):
            self.groups.append(Group(id=i, text=line, system=self, boost=boost))

    def select_targets_from(self, other_system):
        taken = set()
        key = attrgetter("power", "initiative")
        groups = sorted(self.groups, key=key, reverse=True)
        groups = [g for g in groups if g.alive]
        for group in groups:
            other = [g for g in other_system.groups if g.id not in taken and g.alive]
            group.select_target_from(other)
            if group.target is not None:
                assert group.target not in taken, "group ids must be unique"
                taken.add(group.target.id)

    @property
    def alive(self):
        return any(g.alive for g in self.groups)

    @property
    def n(self):
        return sum(g.n for g in self.groups)


class Group:

    template = "{:d} units each with {:d} hit points{}with an attack that does {:d} {} damage at initiative {:d}"

    def __init__(self, id, text, system, boost=0):
        self.id = id
        self.system = system
        parsed = parse(self.template, text).fixed
        self.n, self.hp, props, self.ap, self.atype, self.initiative = parsed
        self.ap += boost
        self.weak = []
        self.immune = []
        for prop in props.strip(" ()").split("; "):
            if not prop:
                continue
            if prop.startswith("immune to "):
                prop = strip_prefix(prop, "immune to ", strict=True)
                self.immune.extend(prop.split(", "))
            else:
                prop = strip_prefix(prop, "weak to ", strict=True)
                self.weak.extend(prop.split(", "))
        self.target = None

    @property
    def alive(self):
        return self.n > 0

    @property
    def power(self):
        return self.n * self.ap

    def attack(self):
        assert self.target is not None
        assert self.target.alive
        kills = self.damage(self.target) // self.target.hp
        kills = min(kills, self.target.n)
        self.target.n -= kills
        log.debug(
            "%s group %d attacks defending group %d, killing %d units",
            self.system.name,
            self.id,
            self.target.id,
            kills,
        )

    def damage(self, other_group):
        multiplier = 1
        if self.atype in other_group.immune:
            multiplier = 0
        elif self.atype in other_group.weak:
            multiplier = 2
        return self.power * multiplier

    def select_target_from(self, other_groups):
        targets = []
        for other_group in other_groups:
            damage = self.damage(other_group)
            if damage > 0:
                log.debug(
                    "%s group %d would deal defending group %d %d damage",
                    self.system.name,
                    self.id,
                    other_group.id,
                    damage,
                )
                targets.append(other_group)
        if not targets:
            self.target = None
            return
        self.target = max(
            targets, key=lambda t: (self.damage(t), t.power, t.initiative)
        )


class Battle:
    template = "{s1}:\n{txt1}\n\n{s2}:\n{txt2}"

    def __init__(self, data, immuno_boost=0):
        self.ticks = 0
        result = parse(self.template, data)
        name = result.named["s1"]
        text = result.named["txt1"]
        self.immune = System(name, text, boost=immuno_boost)
        self.infection = System(name=result.named["s2"], text=result.named["txt2"])

    def target_selection_phase(self):
        self.infection.select_targets_from(self.immune)
        self.immune.select_targets_from(self.infection)

    def attacking_phase(self):
        all_groups = self.infection.groups + self.immune.groups
        # sort in attacking order
        all_groups.sort(key=attrgetter("initiative"), reverse=True)
        for group in all_groups:
            if group.target is not None and group.target.alive:
                group.attack()

    def tick(self):
        for system in self.immune, self.infection:
            log.debug(system.name + ":")
            if system.alive:
                for group in system.groups:
                    if group.alive:
                        log.debug("Group %d contains %d units", group.id, group.n)
            else:
                log.debug("No groups remain.")
        log.debug("")
        self.target_selection_phase()
        log.debug("")
        n_before = self.immune.n + self.infection.n
        self.attacking_phase()
        n_after = self.immune.n + self.infection.n
        if n_after == n_before:
            raise StaleMate
        log.debug("")
        self.ticks += 1

    def run_until_complete(self):
        while self.infection.alive and self.immune.alive:
            self.tick()

    def part_a(self):
        self.run_until_complete()
        if self.immune.alive:
            assert not self.infection.alive
            winner = self.immune
        else:
            assert self.infection.alive
            winner = self.infection
        return winner.n


print("part a:", Battle(data).part_a())

boost = 0
while True:
    battle = Battle(data, immuno_boost=boost)
    try:
        battle.run_until_complete()
    except StaleMate:
        pass
    if battle.immune.alive and not battle.infection.alive:
        break
    boost += 1

print("part b:", battle.immune.n)
