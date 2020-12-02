from aoc_wim.aoc2015 import q21


def test_battle():
    player = q21.Player(name="player", hp=8, damage=5, armor=5)
    boss = q21.Player(name="boss", hp=12, damage=7, armor=2)
    winner = q21.battle_winner(attacker=player, defender=boss)
    assert winner is player
    assert winner.hp == 2
