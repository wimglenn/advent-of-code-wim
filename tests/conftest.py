import sys

Module = type(sys)
mock_aocd = Module("aocd")
mock_aocd.data = ""
sys.modules["aocd"] = mock_aocd
