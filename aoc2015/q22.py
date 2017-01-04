from aocd import data
from fields import Fields


effects = '''
Magic Missile costs 53 mana. It instantly does 4 damage.
Drain costs 73 mana. It instantly does 2 damage and heals you for 2 hit points.
Shield costs 113 mana. It starts an effect that lasts for 6 turns. While it is active, your armor is increased by 7.
Poison costs 173 mana. It starts an effect that lasts for 6 turns. At the start of each turn while it is active, it deals the boss 3 damage.
Recharge costs 229 mana. It starts an effect that lasts for 5 turns. At the start of each turn while it is active, it gives you 101 new mana.
'''.strip()


class Spell(Fields.name.cost.duration[1].damage[0].healing[0].armor[0].mana[0]):
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


def bfs(state0):
    depth = 0
    queue = deque([(state0, depth)])
    while queue:
        state, this_depth = queue.popleft()
        depth = max(depth, this_depth)
        if winner(state):
            return depth
        children = list(valid_next_states(state))
        queue.extend((child, depth + 1) for child in children)


class GameState:

    boss_damage, boss_hp0 = parse_data(data)

    def __init__(self, player_hp=50, mana=500, boss_hp=boss_hp0, to_move='player', history=()):
        self.player_hp = player_hp
        self.mana = mana
        self.boss_hp = boss_hp
        self.to_move = to_move
        self.history = list(history)

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

    def active_spells(self):
        return {move for move, duration_left in self.history if duration_left > 0}

    def next_states(self):
        if self.winner is not None:
            return []

        if self.to_move == 'boss':
            if 'Shield' in active_spells:
                player_hp = self.player_hp - max(self.boss_damage - spells['Shield'].armor, 1)
            else:
                player_hp = self.player_hp - self.boss_damage
            new_history = []
            for move, duration_left in self.history:
                if duration_left > 0:


        assert self.to_move == 'player'



state0 = GameState()
print(state0.winner)
print(state0.next_states())


