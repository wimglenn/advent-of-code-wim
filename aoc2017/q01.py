from aocd import data
import numpy as np

def f(data, roll=1):
    a = np.fromiter(data, dtype=int)
    b = np.roll(a, roll)
    return a[a==b].sum()

tests_a = {
    '1122': 3,
    '1111': 4,
    '1234': 0,
    '91212129': 9,
}
for test_data, expected in tests_a.items():
    assert f(test_data) == expected

tests_b = {
    '1212': 6,
    '1221': 0,
    '123425': 4,
    '123123': 12,
    '12131415': 4,
}
for test_data, expected in tests_b.items():
    assert f(test_data, roll=len(test_data)//2) == expected

print(f(data))  # part a: 1119
print(f(data, roll=len(data)//2))  # part b: 1420
