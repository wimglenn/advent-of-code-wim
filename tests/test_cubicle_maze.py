from aoc_wim.aoc2016 import q13


z0 = 1 + 1j
target = 7 + 4j


def test_path_length():
    grid = q13.ZGrid(q13.WallMap(fav_number=10), on=".", off="#")
    path_length = grid.bfs(target, z0)[target]
    assert path_length == 11


def test_draw(capsys):
    grid = q13.ZGrid(q13.WallMap(fav_number=10), on=".", off="#")
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
