"""
--- Day 22: Wizard Simulator 20XX ---
https://adventofcode.com/2015/day/22
"""
from aocd import data
from fields import Fields
from aoc_wim.search import AStar


class Spell(Fields.name.cost.duration[0].damage[0].healing[0].armor[0].mana[0]):
    pass


spells = [
    Spell("Magic Missile", cost=53, damage=4),
    Spell("Drain", cost=73, damage=2, healing=2),
    Spell("Shield", cost=113, duration=6, armor=7),
    Spell("Poison", cost=173, duration=6, damage=3),
    Spell("Recharge", cost=229, duration=5, mana=101),
]
cheapest_spell_cost = min(s.cost for s in spells)
spells = {s.name: s for s in spells}


def parsed(data):
    data = {k: int(v) for k, v in (line.split(": ") for line in data.splitlines())}
    return data["Hit Points"], data["Damage"]


class GameState:

    boss_hp0, boss_damage = parsed(data)

    def __init__(
        self,
        player_hp=50,
        mana=500,
        boss_hp=boss_hp0,
        to_move="player",
        history=(),
        spent=0,
        part="a",
    ):
        self.player_hp = player_hp
        self.mana = mana
        self.boss_hp = boss_hp
        self.to_move = to_move
        self.history = history
        self.spent = spent
        self.part = part

    @property
    def winner(self):
        if self.player_hp <= 0:
            return "boss"
        if self.boss_hp <= 0:
            return "player"
        if self.to_move == "player":
            if self.mana < cheapest_spell_cost and "Recharge" not in self.active_spells:
                return "boss"
        if self.to_move == "boss":
            if "Poison" in self.active_spells:
                if self.boss_hp <= spells["Poison"].damage:
                    return "player"

    @property
    def active_spells(self):
        return {move for move, duration_left in self.history if duration_left > 0}

    def next_states(self):
        if self.winner is not None:
            return []

        player_hp = self.player_hp
        boss_hp = self.boss_hp
        mana = self.mana

        new_history = []
        for h in self.history:
            move, duration_left = h
            if duration_left > 0:
                if move == "Poison":
                    boss_hp -= spells["Poison"].damage
                elif move == "Recharge":
                    mana += spells["Recharge"].mana
                if duration_left > 1:
                    new_history.append((move, duration_left - 1))

        self.history = new_history

        if self.to_move == "boss":
            if "Shield" in self.active_spells:
                player_hp -= max(self.boss_damage - spells["Shield"].armor, 1)
            else:
                player_hp -= self.boss_damage
            return [
                GameState(
                    player_hp=player_hp,
                    mana=mana,
                    boss_hp=boss_hp,
                    to_move="player",
                    history=self.history,
                    spent=self.spent,
                    part=self.part,
                )
            ]

        assert self.to_move == "player"

        moves = []
        if self.part == "b":
            # hard mode!
            player_hp -= 1
            if player_hp <= 0:
                return moves

        for spell_name in "Shield", "Poison", "Recharge":
            spell = spells[spell_name]
            if mana - spell.cost >= 0 and spell.name not in self.active_spells:
                moves.append(
                    GameState(
                        player_hp=player_hp,
                        mana=mana - spell.cost,
                        boss_hp=boss_hp,
                        to_move="boss",
                        history=self.history + [(spell.name, spell.duration)],
                        spent=self.spent + spell.cost,
                        part=self.part,
                    )
                )

        for spell_name in "Magic Missile", "Drain":
            spell = spells[spell_name]
            if mana - spell.cost >= 0:
                moves.append(
                    GameState(
                        player_hp=player_hp + spell.healing,
                        mana=mana - spell.cost,
                        boss_hp=boss_hp - spell.damage,
                        to_move="boss",
                        history=self.history + [(spell.name, 0)],
                        spent=self.spent + spell.cost,
                        part=self.part,
                    )
                )

        return moves

    def freeze(self):
        tup = (
            self.player_hp,
            self.mana,
            self.boss_hp,
            self.to_move,
            frozenset(self.history),
            self.spent,
            self.part,
        )
        return tup

    @classmethod
    def unfreeze(cls, tup):
        return cls(*tup)

    def __eq__(self, other):
        if not isinstance(other, GameState):
            return NotImplemented
        return self.freeze() == other.freeze()

    def __hash__(self):
        return hash(self.freeze())


class Q22AStar(AStar):
    def __init__(self, part="a"):
        state0 = GameState(part=part).freeze()
        AStar.__init__(self, state0, None)

    def target_reached(self, current_state, target):
        game = GameState.unfreeze(current_state)
        return game.winner == "player"

    def adjacent(self, state):
        game = GameState.unfreeze(state)
        result = [s.freeze() for s in game.next_states()]
        return result

    def cost(self, state0, state1):
        if state1 is None:
            return 0
        game0 = GameState.unfreeze(state0)
        game1 = GameState.unfreeze(state1)
        return abs(game1.spent - game0.spent)

    heuristic = cost


astar = Q22AStar(part="a")
astar.run()
print("part a:", GameState.unfreeze(astar.target).spent)

astar = Q22AStar(part="b")
astar.run()
print("part b:", GameState.unfreeze(astar.target).spent)
