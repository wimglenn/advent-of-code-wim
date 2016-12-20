from aocd import data
import numpy as np
import matplotlib.pyplot as plt
import itertools


test_data = '''Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3'''


def parse_data(data):
    ingredients = {}
    for line in data.splitlines():
        name, stats = line.split(': ')
        stats = stats.split()[1::2]
        ingredients[name] = np.array([int(s.rstrip(',')) for s in stats])
    return ingredients


ingredients = parse_data(test_data)
A = np.vstack(ingredients.values())[:,:-1]
n = len(A)
r = 100//n
R = np.array([r] * n).reshape(n, 1)

def score(R, A):
    A = A.copy()
    A *= R
    A = A.sum(axis=0)
    A[A<0] = 0
    return A.prod()

bestscore = 0

while True:
    for up, down in permutations(range(len(R)))
