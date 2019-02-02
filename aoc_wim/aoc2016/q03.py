from aocd import data
import numpy as np


A = np.fromstring(data, sep=' ', dtype=int)
R = A.reshape(-1, 3).T
C = R.reshape(-1, 3).T

for A in R, C:
    T  = (A[0] + A[1] > A[2])
    T &= (A[0] + A[2] > A[1])
    T &= (A[1] + A[2] > A[0])
    print(T.sum())
