import json
import pytest

from aoc_wim.aoc2021.q18 import SnailfishNumber


@pytest.mark.parametrize("raw", """\
[1,2]
[[1,2],3]
[9,[8,7]]
[[1,9],[8,5]]
[[[[1,2],[3,4]],[[5,6],[7,8]]],9]
[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]
[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]""".splitlines())
def test_parsing(raw):
    # doesn't matter if we initialize from string or object - same result
    fromtxt = SnailfishNumber(raw)
    fromobj = SnailfishNumber(json.loads(raw))
    assert fromtxt == fromobj


def test_basic_addition():
    left = SnailfishNumber([1,2])
    right = SnailfishNumber([[3,4],5])
    expected = SnailfishNumber([[1,2],[[3,4],5]])
    assert left + right == expected


@pytest.mark.parametrize("eg", """\
[[[[[9,8],1],2],3],4] becomes [[[[0,9],2],3],4]
[7,[6,[5,[4,[3,2]]]]] becomes [7,[6,[5,[7,0]]]]
[[6,[5,[4,[3,2]]]],1] becomes [[6,[5,[7,0]]],3]
[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]] becomes [[3,[2,[8,0]]],[9,[5,[7,0]]]]""".splitlines())
def test_explode(eg):
    before, after = eg.split(" becomes ")
    n0 = SnailfishNumber(before)
    n0.reduce()
    assert str(n0) == after


def test_reduce():
    left = SnailfishNumber([[[[4,3],4],4],[7,[[8,4],9]]])
    right = SnailfishNumber([1,1])
    expected = SnailfishNumber([[[[0,7],4],[[7,8],[6,0]]],[8,1]])
    assert left + right == expected


@pytest.mark.parametrize("ns,expected", [
    ([[1,1],[2,2],[3,3],[4,4]],             "[[[[1,1],[2,2]],[3,3]],[4,4]]"),
    ([[1,1],[2,2],[3,3],[4,4],[5,5]],       "[[[[3,0],[5,3]],[4,4]],[5,5]]"),
    ([[1,1],[2,2],[3,3],[4,4],[5,5],[6,6]], "[[[[5,0],[7,4]],[5,5]],[6,6]]"),
])
def test_final_sums(ns, expected):
    actual = sum(SnailfishNumber(n) for n in ns)
    assert str(actual) == expected


def test_big_final_sum1():
    larger_example = """\
        [[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
        [7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
        [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
        [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
        [7,[5,[[3,8],[1,4]]]]
        [[2,[2,2]],[8,[8,1]]]
        [2,9]
        [1,[[[9,3],9],[[9,0],[0,7]]]]
        [[[5,[7,4]],7],1]
        [[[[4,2],2],6],[8,7]]"""
    sns = [SnailfishNumber(line.strip()) for line in larger_example.splitlines()]
    assert str(sum(sns)) == "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"


def test_big_final_sum2():
    larger_example = """\
        [[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
        [[[5,[2,8]],4],[5,[[9,9],0]]]
        [6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
        [[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
        [[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
        [[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
        [[[[5,4],[7,7]],8],[[8,3],8]]
        [[9,3],[[9,9],[6,[4,9]]]]
        [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
        [[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""
    sns = [SnailfishNumber(line.strip()) for line in larger_example.splitlines()]
    assert str(sum(sns)) == "[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]"


@pytest.mark.parametrize("eg", """\
[9,1] becomes 29
[1,9] becomes 21
[[9,1],[1,9]] becomes 129
[[1,2],[[3,4],5]] becomes 143
[[[[0,7],4],[[7,8],[6,0]]],[8,1]] becomes 1384
[[[[1,1],[2,2]],[3,3]],[4,4]] becomes 445
[[[[3,0],[5,3]],[4,4]],[5,5]] becomes 791
[[[[5,0],[7,4]],[5,5]],[6,6]] becomes 1137
[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]] becomes 3488""".splitlines())
def test_magnitude(eg):
    n, expected = eg.split(" becomes ")
    assert str(abs(SnailfishNumber(n))) == expected
