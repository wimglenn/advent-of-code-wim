import itertools as it

prog = [2, 4, 1, 1, 7, 5, 1, 5, 4, 0, 0, 3, 5, 5, 3, 0]
As = [0o4133267275]
for A in As:
    A0 = A
    print(f"{A:o}:", end=" ")
    outs = []
    while A:
        B = (A % 8) ^ 0b001
        C = A >> B
        out = ((B ^ 0b101) ^ C) % 8
        print(out, end=",")
        outs.append(out)
        A >>= 3
    print()
    if outs == prog:
        print(A, oct(A))
        break
