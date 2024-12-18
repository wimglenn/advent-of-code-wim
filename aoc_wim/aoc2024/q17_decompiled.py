prog = [2, 4, 1, 1, 7, 5, 1, 5, 4, 0, 0, 3, 5, 5, 3, 0]
As = [0o4_532_307_133_267_275]
for A in As:
    print(f"{oct(A)}: ", end="")
    while A:
        B = (A & 7) ^ 0b001
        C = A >> B
        out = ((B ^ 0b101) ^ C) & 7
        print(out, end=",")
        A >>= 3
    print()
