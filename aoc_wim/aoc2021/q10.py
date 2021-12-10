"""
--- Day 10: Syntax Scoring ---
https://adventofcode.com/2021/day/10
"""
from aocd import data
from statistics import median


class ParserError(Exception):
    def __init__(self, line, expected, found):
        self.line = line
        self.expected = expected
        self.found = found
        self.syntax_error_score = [3, 57, 1197, 25137][")]}>".index(found)]

    def __str__(self):
        return f"{self.line} - Expected {self.expected}, but found {self.found} instead."


class Parser:

    lookup = dict(zip("([{<", ")]}>"))

    def __init__(self):
        self.pos = 0
        self.stack = []

    def __call__(self, line):
        while self.pos < len(line):
            found = line[self.pos]
            if found in self.lookup:
                self.stack.append(found)
            else:
                expected = self.lookup[self.stack[-1]]
                if found != expected:
                    raise ParserError(line, expected, found)
                self.stack.pop()
            self.pos += 1

    @property
    def autocompletion(self):
        return "".join(self.lookup[char] for char in reversed(self.stack))

    @property
    def autocomplete_score(self):
        result = 0
        for char in self.autocompletion:
            result *= 5
            result += ")]}>".index(char) + 1
        return result


a = b = 0
bs = []
for line in data.splitlines():
    parser = Parser()
    try:
        parser(line)
    except ParserError as err:
        a += err.syntax_error_score
    else:
        bs.append(parser.autocomplete_score)

if bs:
    b = median(bs)

print("part a:", a)
print("part b:", b)
