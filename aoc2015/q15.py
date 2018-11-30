from aocd import data
from itertools import permutations
from collections import Counter
import numpy as np


test_data = '''Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3'''


def ways(total, coins=(1,2,5,10,20,50,100)):
    ways = [[Counter()]] + [[] for _ in range(total)]
    for coin in coins:
        for i in range(coin, total + 1):
            ways[i] += [way + Counter({coin: 1}) for way in ways[i-coin]]
    return ways[total]


def parse_data(data):
    ingredients = {}
    for line in data.splitlines():
        name, stats = line.split(': ')
        stats = stats.split()[1::2]
        ingredients[name] = np.array([int(s.rstrip(',')) for s in stats])
    return ingredients


def score(R, A):
    A = (R*A).sum(axis=0)
    A[A<0] = 0
    return A[:-1].prod()


def get_perturbations(R0):
    n = len(R0)
    for up, down in permutations(range(n), 2):
        R = R0 + np.eye(n, 1, -up, dtype=int) - np.eye(n, 1, -down, dtype=int)
        if (R >= 0).all():
            yield R


def get_best_score(data):
    ingredients = parse_data(data)
    A = np.vstack(ingredients.values())
    n = len(A)
    r = 100//n
    R = np.array([r] * n).reshape(n, 1)

    best_score = 0
    while True:
        for R_ in get_perturbations(R):
            this_score = score(R_, A)
            if this_score > best_score:
                R = R_
                best_score = this_score
                break
        else:
            return best_score


def get_best_score_for_calories(data, n_teaspoons=100, calories=500):
    ingredients = parse_data(data)
    A = np.vstack(ingredients.values())
    n = len(A)
    cals = A[:,-1]
    best_score = 0
    for combo in ways(total=calories, coins=cals):
        R = np.array([combo.get(x, 0) for x in cals]).reshape(n,1)
        if R.sum() == n_teaspoons:
            this_score = score(R, A)
            best_score = max(best_score, this_score)
    return best_score


assert get_best_score(test_data) == 62842880
print(get_best_score(data))  # part a: 18965440

assert get_best_score_for_calories(test_data) == 57600000
print(get_best_score_for_calories(data))  # part b: 15862900
