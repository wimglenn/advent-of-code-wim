from setuptools import setup, find_packages

setup(
    name="advent-of-code",
    version="0.1",
    description='Pluggable runner and my solutions for https://adventofcode.com/',
    url="https://github.com/wimglenn/advent-of-code",
    author="Wim Glenn",
    author_email="hey@wimglenn.com",
    license="WTFPL",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Games/Entertainment :: Puzzle Games",
    ],
    install_requires=[
        "advent-of-code-data >= 0.6",
        "numpy",
        "parse",
        "pebble",
        "scipy",
        "fields",
        "networkx",
        "wimpy",
        "pytz",
        "setuptools",
    ],
    packages=find_packages(),
    entry_points={
        "console_scripts": ["aoc = aoc:main"],
        # TODO: better names - aocr?  advent-of-code-user
        "aoc": ["wim = aoc:wim"],
    },
)
