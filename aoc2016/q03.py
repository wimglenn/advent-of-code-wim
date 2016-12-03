from aocd import data
import numpy as np


A = np.fromstring(data, sep=' ', dtype=int)
N = len(A)//3
R = A.reshape(N, 3).T
C = R.reshape(N, 3).T

for A in R, C:
    T  = (A[0] + A[1] > A[2])
    T &= (A[0] + A[2] > A[1])
    T &= (A[1] + A[2] > A[0])
    print(T.sum())
