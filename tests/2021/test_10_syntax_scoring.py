import pytest
import re

from aoc_wim.aoc2021 import q10


@pytest.mark.parametrize("line", [
    "()",
    "[]",
    "([])",
    "{()()()}",
    "<([{}])>",
    "[<>({}){}[([])<>]]",
    "(((((((((())))))))))",
])
def test_valid_syntax(line):
    parser = q10.Parser()
    parser(line)


@pytest.mark.parametrize("line", [
    "(]",
    "{()()()>",
    "(((()))}",
    "(<([]){()}[{}])",
])
def test_invalid_syntax(line):
    parser = q10.Parser()
    with pytest.raises(q10.ParserError):
        parser(line)


@pytest.mark.parametrize("example", """\
{([(<{}[<>[]}>{[]{[(<()> - Expected ], but found } instead.
[[<[([]))<([[{}[[()]]] - Expected ], but found ) instead.
[{[{({}]{}}([{[{{{}}([] - Expected ), but found ] instead.
[<(<(<(<{}))><([]([]() - Expected >, but found ) instead.
<{([([[(<>()){}]>(<<{{ - Expected ], but found > instead.
""".splitlines())
def test_syntax_error_messages(example):
    line, msg = example.split(" - ")
    parser = q10.Parser()
    with pytest.raises(q10.ParserError, match=re.escape(msg)) as cm:
        parser(line)
    assert str(cm.value) == example


@pytest.mark.parametrize("example,score", zip("""\
[({(<(())[]>[[{[]{<()<>> - Complete by adding }}]])})].
[(()[<>])]({[<{<<[]>>( - Complete by adding )}>]}).
(((({<>}<{<{<>}{[]{[]{} - Complete by adding }}>}>)))).
{<[[]]>}<{[{[{[]{()[[[] - Complete by adding ]]}}]}]}>.
<{([{{}}[<[[[<>{}]]]>[]] - Complete by adding ])}>.""".splitlines(), """\
}}]])})] - 288957 total points.
)}>]}) - 5566 total points.
}}>}>)))) - 1480781 total points.
]]}}]}]}> - 995444 total points.
])}> - 294 total points.""".splitlines()))
def test_completions(example, score):
    line, completion = example.split(" - ")
    expected_completion, total_points = score.split(" - ")
    assert completion == f"Complete by adding {expected_completion}."
    expected_score = int(total_points.split()[0])
    parser = q10.Parser()
    parser(line)
    assert parser.autocompletion == expected_completion
    assert parser.autocomplete_score == expected_score
