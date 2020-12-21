"""
--- Day 21: Allergen Assessment ---
https://adventofcode.com/2020/day/21
"""
from aocd import data
from bidict import bidict

d = {}
all_ingredients = []
for line in data.splitlines():
    ingredients, allergens = line.rstrip(")").split(" (contains ")
    ingredients = ingredients.split()
    all_ingredients += ingredients
    allergens = allergens.split(", ")
    for allergen in allergens:
        if allergen not in d:
            d[allergen] = set(ingredients)
        else:
            d[allergen] &= set(ingredients)

identified = bidict()
while d:
    for allergen, ingredients in d.items():
        if len(ingredients) == 1:
            break
    else:
        break
    [ingredient] = ingredients
    identified[allergen] = ingredient
    for ingredients in d.values():
        ingredients -= {ingredient}

print("part a:", sum(i not in identified.inv for i in all_ingredients))
print("part b:", ",".join(sorted(identified.inv, key=identified.inv.get)))
