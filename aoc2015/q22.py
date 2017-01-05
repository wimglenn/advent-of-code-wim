from aocd import data
from collections import deque
from fields import Fields
from copy import deepcopy


class Spell(Fields.name.cost.duration[0].damage[0].healing[0].armor[0].mana[0]):
    pass

spells = [
    Spell('Magic Missile', cost=53, damage=4),
    Spell('Drain', cost=73, damage=2, healing=2),
    Spell('Shield', cost=113, duration=6, armor=7),
    Spell('Poison', cost=173, duration=6, damage=3),
    Spell('Recharge', cost=229, duration=5, mana=101)
]
cheapest_spell_cost = min(s.cost for s in spells)
spells = {s.name: s for s in spells}


def parse_data(data):
    data = {k: int(v) for k,v in (line.split(': ') for line in data.splitlines())}
    return data['Hit Points'], data['Damage']


class GameState:

    boss_hp0, boss_damage = parse_data(data)

    def __init__(self, player_hp=50, mana=500, boss_hp=boss_hp0, to_move='player', history=(), spent=0):
        self.player_hp = player_hp
        self.mana = mana
        self.boss_hp = boss_hp
        self.to_move = to_move
        self.history = list(history)
        self.spent = spent

    def __repr__(self):
        return 'GameState({}player={}+{}, {}boss={})'.format(
            {'player': '*', 'boss': ''}[self.to_move],
            self.player_hp, 
            self.mana, 
            {'player': '', 'boss': '*'}[self.to_move],
            self.boss_hp,
        )

    @property
    def winner(self):
        if self.player_hp <= 0:
            return 'boss'
        if self.boss_hp <= 0:
            return 'player'
        if self.to_move == 'player':
            if self.mana < cheapest_spell_cost and 'Recharge' not in self.active_spells:
                return 'boss'
        if self.to_move == 'boss':
            if 'Poison' in self.active_spells and self.boss_hp <= spells['Poison'].damage:
                return 'player'

    @property
    def active_spells(self):
        return {move for move, duration_left in self.history if duration_left > 0}

    def next_states(self, hard_mode=False):
        if self.winner is not None:
            return []

        player_hp = self.player_hp
        boss_hp = self.boss_hp
        mana = self.mana

        for h in self.history:
            move, duration_left = h
            if duration_left > 0:
                if move == 'Poison':
                    boss_hp -= spells['Poison'].damage
                elif move == 'Recharge':
                    mana += spells['Recharge'].mana
                h[1] -= 1

        if self.to_move == 'boss':
            if 'Shield' in self.active_spells:
                player_hp -= max(self.boss_damage - spells['Shield'].armor, 1)
            else:
                player_hp -= self.boss_damage
            return [
                GameState(
                    player_hp=player_hp, 
                    mana=mana, 
                    boss_hp=boss_hp, 
                    to_move='player', 
                    history=deepcopy(self.history),
                    spent=self.spent,
                )
            ]

        assert self.to_move == 'player'

        moves = []
        if hard_mode:
            player_hp -= 1
            if player_hp <= 0:
                return moves


        for spell_name in 'Shield', 'Poison', 'Recharge':
            spell = spells[spell_name]
            if mana - spell.cost >= 0 and spell.name not in self.active_spells:
                moves.append(
                    GameState(
                        player_hp=player_hp, 
                        mana=mana - spell.cost,
                        boss_hp=boss_hp,
                        to_move='boss',
                        history=deepcopy(self.history) + [[spell.name, spell.duration]],
                        spent=self.spent + spell.cost
                    )
                )

        for spell_name in 'Magic Missile', 'Drain':
            spell = spells[spell_name]
            if mana - spell.cost >= 0:
                moves.append(
                    GameState(
                        player_hp=player_hp + spell.healing, 
                        mana=mana - spell.cost,
                        boss_hp=boss_hp - spell.damage,
                        to_move='boss',
                        history=deepcopy(self.history) + [[spell.name, 0]],
                        spent=self.spent + spell.cost,
                    )
                )

        return moves


def bfs(state0, hard_mode=False):
    depth = 0
    queue = deque([(state0, depth)])
    min_spent = float('inf')
    best_fight = None
    i = 0
    print()
    while queue:
        i += 1
        if i % 10000 == 1:
            print('\rqueue length: {}       '.format(len(queue)), end='')
        state, this_depth = queue.popleft()
        if state.spent >= min_spent:
            continue
        depth = max(depth, this_depth)
        if state.winner == 'player':
            if state.spent < min_spent:
                best_fight = state
            min_spent = min(state.spent, min_spent)
        elif state.winner is None:
            children = state.next_states(hard_mode=hard_mode)
            queue.extend((child, depth + 1) for child in children)
    print()
    return min_spent, best_fight


min_spent, final_state = bfs(GameState())
min_spent_hard, final_state_hard = bfs(GameState(), hard_mode=True)

print(min_spent)  # part a: 1269
print(min_spent_hard)  # part b: 1309
