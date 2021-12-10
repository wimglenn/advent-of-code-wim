"""
--- Day 10: Syntax Scoring ---
https://adventofcode.com/2021/day/10
"""
from aocd import data

opens = "([{<"
closes = ")]}>"
weight_a = dict(zip(closes, [3, 57, 1197, 25137]))
weight_b = dict(zip(closes, range(1, 5)))
flip = dict(zip(opens + closes, closes + opens))


class ParserError(Exception):
    def __init__(self, line, expected, found):
        self.line = line
        self.expected = expected
        self.found = found
        self.syntax_error_score = weight_a[found]

    def __str__(self):
        return f"{self.line} - Expected {self.expected}, but found {self.found} instead."


class Parser:
    def __init__(self):
        self.pos = 0
        self.stack = []

    def __call__(self, line):
        while self.pos < len(line):
            found = line[self.pos]
            if found in opens:
                self.stack.append(found)
            elif found in closes:
                expected = flip[self.stack[-1]]
                if found != expected:
                    raise ParserError(line, expected, found)
                self.stack.pop()
            self.pos += 1

    @property
    def autocompletion(self):
        return "".join(flip[char] for char in reversed(self.stack))

    @property
    def autocomplete_score(self):
        result = 0
        for char in self.autocompletion:
            result *= 5
            result += weight_b[char]
        return result


a = 0
bs = []
for line in data.splitlines():
    parser = Parser()
    try:
        parser(line)
    except ParserError as err:
        a += err.syntax_error_score
    else:
        bs.append(parser.autocomplete_score)

bs.sort()
b = None
if bs:
    b = bs[len(bs)//2]

print("part a:", a)
print("part b:", b)
