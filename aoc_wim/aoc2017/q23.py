from aocd import data


def exe(a0=0):
    d = dict.fromkeys("abcdefgh", 0)
    d["a"] = a0
    i = 0
    n_mul = 0
    while i < len(lines):
        line = lines[i]
        op, k, n = line.split()
        n = d[n] if n in d else int(n)
        if op == "set":
            d[k] = n
        elif op == "sub":
            d[k] -= n
        elif op == "mul":
            d[k] *= n
            n_mul += 1
        elif op == "jnz":
            k = d[k] if k in d else int(k)
            i += n - 1 if k else 0
        elif op == "wtf":
            d[k] = all(n % i for i in range(2, n))
        i += 1
    return d["h"] if a0 else n_mul


lines = data.splitlines()
print("part a:", exe())
lines[8:10] = ["wtf f b", "jnz 1 15"]
print("part b:", exe(a0=1))
