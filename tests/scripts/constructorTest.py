from pprint import pp

READ_PATH = "tests/test_fos/read_test.fos"
WRITE_PATH = "tests/test_fos/write_test.fos"

from FoSpy.synthesis import Synthesis

mySyn = Synthesis.fromFile(READ_PATH)

pass