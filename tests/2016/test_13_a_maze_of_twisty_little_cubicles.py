from aoc_wim.aoc2016 import q13


def test_render(capsys):
    z0 = 1 + 1j
    target = 7 + 4j

    grid = q13.make_grid("10")
    grid.draw(window=9 + 6j, pretty=False)
    out, err = capsys.readouterr()
    expected1 = """
    0 .#.####.##
    1 ..#..#...#
    2 #....##...
    3 ###.#.###.
    4 .##..#..#.
    5 ..##....#.
    6 #...##.###
      0   5    9"""
    assert out.rstrip() == expected1

    grid.draw_path(z=target, z0=z0, pretty=False)
    out, err = capsys.readouterr()
    expected2 = """
    0 .#.####.##
    1 .O#..#...#
    2 #xxx.##...
    3 ###x#.###.
    4 .##xx#xT#.
    5 ..##xxx.#.
    6 #...##.###
      0   5    9"""
    assert out.rstrip() == expected2
