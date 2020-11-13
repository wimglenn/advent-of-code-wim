"""
--- Day 21: RPG Simulator 20XX ---
https://adventofcode.com/2015/day/21
"""
from collections import defaultdict
from itertools import combinations

from aocd import data
from fields import Fields
from fields import Tuple


shop_data = """\
Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3
"""


class Item(Tuple.name.cost.damage.armor):
    @classmethod
    def fromline(cls, line):
        name, cost, damage, armor = line.rsplit(None, 3)
        item = Item(name, cost=int(cost), damage=int(damage), armor=int(armor))
        return item


shop = defaultdict(list)
for line in shop_data.splitlines():
    if ":" in line:
        itemtype = line.split(":")[0].lower().rstrip("s")
    else:
        if line:
            item = Item.fromline(line)
            shop[itemtype].append(item)


class Player(Fields.damage.armor.name["player"].hp[100]):
    ...


def battle_winner(attacker, defender):
    while attacker.hp > 0 and defender.hp > 0:
        defender.hp -= max(attacker.damage - defender.armor, 1)
        attacker, defender = defender, attacker
    return defender


def parsed(data):
    d = {k.lower(): int(v) for k, v in (line.split(": ") for line in data.splitlines())}
    d["hp"] = d.pop("hit points")
    return Player(name="boss", **d)


def choices(shop):
    weapon_choices = combinations(shop["weapon"], 1)

    armor_choices = [()]  # no armor..
    armor_choices += combinations(shop["armor"], 1)

    ring_choices = [()]  # no rings..
    ring_choices += combinations(shop["ring"], 1)
    ring_choices += combinations(shop["ring"], 2)

    for weapon in weapon_choices:
        for armor in armor_choices:
            for rings in ring_choices:
                items = [*weapon, *armor, *rings]
                total_damage = sum(item.damage for item in items)
                total_armor = sum(item.armor for item in items)
                total_cost = sum(item.cost for item in items)
                player = Player(damage=total_damage, armor=total_armor)
                player.items = items
                player.cost = total_cost
                yield player


def play(data, shop):
    min_cost = float("inf")
    max_cost = 0
    for player in choices(shop):
        boss = parsed(data)
        if battle_winner(player, boss) is player:
            min_cost = min(player.cost, min_cost)
        else:
            max_cost = max(player.cost, max_cost)
    return min_cost, max_cost


if __name__ == "__main__":
    min_cost_to_win, max_cost_to_lose = play(data, shop)
    print(min_cost_to_win)
    print(max_cost_to_lose)
