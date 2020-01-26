from aoc_wim.aoc2016 import q04


def test_decrytion():
    assert q04.decrypt_name("qzmt-zixmtkozy-ivhz", 343) == "very encrypted name"
