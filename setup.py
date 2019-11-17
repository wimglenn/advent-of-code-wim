from setuptools import find_packages
from setuptools import setup

from aoc_wim import __doc__
from aoc_wim import __version__


setup(
    name="advent-of-code-wim",
    version=__version__,
    description=__doc__,
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
        "advent-of-code-data >= 0.8.0",
        "anytree",
        "bidict",
        "numpy",
        "parse",
        "scipy",
        "fields",
        "networkx",
        "wimpy",
    ],
    packages=find_packages(),
    entry_points={
        "adventofcode.user": ["wim = aoc_wim:plugin"],
        "console_scripts": ["aocw = aoc_wim.cli:run_one"],
    },
)
