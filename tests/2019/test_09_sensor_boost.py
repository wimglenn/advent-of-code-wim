from aoc_wim.aoc2019.q09 import compute


def test_sample_program_quine():
    quine = "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"
    assert compute(quine) == quine


def test_16_digit_number_output():
    result = compute("1102,34915192,34915192,7,4,7,99,0")
    assert int(result)
    assert len(result) == 16


def test_output_middle_number():
    src = "104,1125899906842624,99"
    result = compute(src)
    assert result == src.split(",")[1]
