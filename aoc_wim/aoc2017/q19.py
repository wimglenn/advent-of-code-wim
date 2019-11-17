from itertools import count

import numpy as np
from aocd import data

test_data = """\
     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ 
                """


def tubemaze(data):
    A = np.fromiter(data.replace("\n", ""), dtype="U1")
    A = A.reshape(len(data.splitlines()), -1)
    x = np.array([-1, A[0].argmax()], dtype=int)
    v = np.array([1, 0], dtype=int)
    letters = ""
    for i in count():
        x += v
        a = A[tuple(x)]
        if a == "+":
            v = v[::-1]
            if A[tuple(x + v)] == " ":
                v *= -1
        elif a not in "-| ":
            letters += a
        elif a == " ":
            return letters, i


assert tubemaze(test_data) == ("ABCDEF", 38)

a, b = tubemaze(data)
print("part a:", a)
print("part b:", b)
