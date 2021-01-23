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
        scores = self.scores
        e1, e2 = self.elf1, self.elf2
        prev_len = len(scores)
        while len(scores) < min_length:
            score1 = scores[e1]
            score2 = scores[e2]
            score = score1 + score2
            if score >= 10:
                scores.append(1)
                scores.append(score - 10)
            else:
                scores.append(score)
            e1 = (e1 + 1 + score1) % len(scores)
            e2 = (e2 + 1 + score2) % len(scores)
        self.elf1 = e1
        self.elf2 = e2
        self.scores_str += "".join([str(x) for x in scores[prev_len:]])


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
