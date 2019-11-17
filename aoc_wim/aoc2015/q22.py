import heapq

from aocd import data
from fields import Fields


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
    ):
        self.player_hp = player_hp
        self.mana = mana
        self.boss_hp = boss_hp
        self.to_move = to_move
        self.history = history
        self.spent = spent

    def __repr__(self):
        return "GameState({}player={}+{}, {}boss={})".format(
            {"player": "*", "boss": ""}[self.to_move],
            self.player_hp,
            self.mana,
            {"player": "", "boss": "*"}[self.to_move],
            self.boss_hp,
        )

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

    def __lt__(self, other):  # needed for min-heap
        return self.spent < other.spent

    @property
    def active_spells(self):
        return {move for move, duration_left in self.history if duration_left > 0}

    def next_states(self, hard_mode=False):
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
                )
            ]

        assert self.to_move == "player"

        moves = []
        if hard_mode:
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
                    )
                )

        return moves


def bfs(state0, hard_mode=False):
    queue = [(state0.spent, state0)]  # min-heap
    while queue:
        spent, state = heapq.heappop(queue)
        if state.winner == "player":
            return spent
        if state.winner is None:
            for child in state.next_states(hard_mode=hard_mode):
                heapq.heappush(queue, (child.spent, child))


min_spent = bfs(GameState())
min_spent_hard = bfs(GameState(), hard_mode=True)

print(min_spent)
print(min_spent_hard)
