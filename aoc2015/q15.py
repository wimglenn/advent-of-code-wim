from aocd import data
from itertools import permutations
import numpy as np


test_data = '''Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3'''


def parse_data(data):
    ingredients = {}
    for line in data.splitlines():
        name, stats = line.split(': ')
        stats = stats.split()[1::2]
        ingredients[name] = np.array([int(s.rstrip(',')) for s in stats])
    return ingredients


def score(R, A):
    A = A.copy()
    A *= R
    A = A.sum(axis=0)
    A[A<0] = 0
    score = A[:-1].prod()
    return score


def get_perturbations(R, calories_target=None):
    n = len(R)
    for up, down in permutations(range(n), 2):
        yield R + np.eye(n, 1, -up, dtype=int) - np.eye(n, 1, -down, dtype=int)


def get_best_score(data, calories_target=None):
    ingredients = parse_data(data)
    A = np.vstack(ingredients.values())
    n = len(A)
    r = 100//n
    R = np.array([r] * n).reshape(n, 1)

    best_score = 0
    while True:
        for R_ in get_perturbations(R, calories_target=calories_target):
            this_score = score(R_, A)
            if this_score > best_score:
                R = R_
                best_score = this_score
                break
        else:
            return best_score


assert get_best_score(test_data) == 62842880
# print(get_best_score(data))  # part a: 18965440
assert get_best_score(data) == 18965440

print(get_best_score(test_data, calories_target=500))
# assert get_best_score(test_data, calories_target=500) == 57600000

# print(test_data)
print(data)
