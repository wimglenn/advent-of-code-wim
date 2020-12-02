from aocd import data

a = b = 0
for line in data.splitlines():
    xy, char, passwd = line.split()
    char = char.rstrip(":")
    x, y = xy.split("-")
    x = int(x)
    y = int(y)
    a += x <= passwd.count(char) <= y
    b += (passwd[x - 1] + passwd[y - 1]).count(char) == 1

print(a)
print(b)
