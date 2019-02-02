from aocd import data
from parse import parse
from wimpy import strip_prefix
from operator import attrgetter
import logging


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
        groups = sorted(self.groups, key=attrgetter("effective_power", "initiative"), reverse=True)
        groups = [g for g in groups if g.alive]
        for group in groups:
            other_groups = [g for g in other_system.groups if g.id not in taken and g.alive]
            group.select_target_from(other_groups)
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
        self.n, self.hp, props, self.ap, self.atype, self.initiative = parse(self.template, text).fixed
        self.ap += boost
        self.weak = []
        self.immune = []
        for prop in props.strip(' ()').split('; '):
            if not prop:
                continue
            if prop.startswith("immune to "):
                self.immune.extend(strip_prefix(prop, "immune to ", strict=True).split(", "))
            else:
                assert prop.startswith("weak to ")
                self.weak.extend(strip_prefix(prop, "weak to ", strict=True).split(", "))
        self.target = None

    @property
    def alive(self):
        return self.n > 0

    @property
    def effective_power(self):
        return self.n * self.ap

    def attack(self):
        assert self.target is not None
        assert self.target.alive
        kills = self.damage(self.target) // self.target.hp
        kills = min(kills, self.target.n)
        self.target.n -= kills
        log.debug(
            "%s group %d attacks defending group %d, killing %d units",
            self.system.name, self.id, self.target.id, kills,
        )

    def damage(self, other_group):
        multiplier = 1
        if self.atype in other_group.immune:
            multiplier = 0
        elif self.atype in other_group.weak:
            multiplier = 2
        return self.effective_power * multiplier

    def select_target_from(self, other_groups):
        targets = []
        for other_group in other_groups:
            damage = self.damage(other_group)
            if damage > 0:
                log.debug(
                    "%s group %d would deal defending group %d %d damage",
                    self.system.name, self.id, other_group.id, damage,
                )
                targets.append(other_group)
        self.target = None
        if targets:
            self.target = max(targets, key=lambda t: (self.damage(t), t.effective_power, t.initiative))


class Battle:
    template = "{s1}:\n{txt1}\n\n{s2}:\n{txt2}"

    def __init__(self, data, immuno_boost=0):
        self.ticks = 0
        result = parse(self.template, data)
        self.immune = System(name=result.named["s1"], text=result.named["txt1"], boost=immuno_boost)
        self.infection = System(name=result.named["s2"], text=result.named["txt2"])

    def target_selection_phase(self):
        self.infection.select_targets_from(self.immune)
        self.immune.select_targets_from(self.infection)

    def attacking_phase(self):
        all_groups = self.infection.groups + self.immune.groups
        all_groups_in_attacking_order = sorted(all_groups, key=attrgetter("initiative"), reverse=True)
        for group in all_groups_in_attacking_order:
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


def part_a(data):
    return Battle(data).part_a()


def part_b(data, boost0=0):
    boost = boost0
    while True:
        battle = Battle(data, immuno_boost=boost)
        try:
            battle.run_until_complete()
        except StaleMate:
            pass
        if battle.immune.alive and not battle.infection.alive:
            return battle.immune.n
        boost += 1


test_data = """\
Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4"""


assert part_a(test_data) == 5216
assert part_b(test_data, boost0=1570) == 51


print("part a:", part_a(data))
print("part b:", part_b(data))
