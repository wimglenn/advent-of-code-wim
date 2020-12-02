import ast
from pathlib import Path

from aocd.models import Puzzle


here = Path(__file__).parent.resolve()


def get_module_docstring(path):
    """get a .py file docstring, without actually executing the file"""
    with open(path) as f:
        return ast.get_docstring(ast.parse(f.read()))


def set_module_docstring(path, text):
    prev = get_module_docstring(path)
    if prev == text:
        # nothing to do
        return
    if prev is not None:
        print(repr(text))
        print(repr(prev))
        raise Exception(f"refusing to clobber existing docstring on {path}")
    content = Path(path).read_text()
    Path(path).write_text(f'"""\n{text}\n"""\n{content}')


def set_docstrings():
    files = here.glob("aoc*/q*.py")
    for file in files:
        day = int(file.name[1:3])
        year = int(file.parent.name[3:])
        puzzle = Puzzle(year, day)
        docstring = f"--- Day {day}: {puzzle.title} ---\n"
        docstring += puzzle.url
        set_module_docstring(file, docstring)
