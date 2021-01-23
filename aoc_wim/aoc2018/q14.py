"""
--- Day 14: Chocolate Charts ---
https://adventofcode.com/2018/day/14
"""
from aocd import data


class RecipeList:

    def __init__(self, initial=(3, 7)):
        self.scores = list(initial)
        self.scores_str = "".join([str(x) for x in self.scores])
        self.elf1 = 0
        self.elf2 = 1

    def grow(self, min_length):
        lookup = {n: [int(x) for x in str(n)] for n in range(19)}
        prev_len = len(self.scores)
        while len(self.scores) < min_length:
            score1 = self.scores[self.elf1]
            score2 = self.scores[self.elf2]
            self.scores.extend(lookup[score1 + score2])
            self.elf1 = (self.elf1 + 1 + score1) % len(self.scores)
            self.elf2 = (self.elf2 + 1 + score2) % len(self.scores)
        self.scores_str += "".join([str(x) for x in self.scores[prev_len:]])


recipes = RecipeList()

k = int(data)
if k < 10**6:
    recipes.grow(k + 10)
    print("part a:", "".join(str(n) for n in recipes.scores[k:k + 10]))

chunk = 2_000_000
i = -1
while i == -1:
    recipes.grow(min_length=len(recipes.scores) + chunk)
    i = recipes.scores_str.find(data, -chunk - len(data))
print("part b:", i)
