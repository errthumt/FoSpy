from FoSpy.blocks.synthesis import Synthesis
from FoSpy._debug import Debug, all_debugs_on
_debug = Debug()


mySyn = Synthesis.fromFile("tests/test_fos/start_synthesis.fos")
all_debugs_on()
anneal = mySyn.treatments[2]
anneal.show_plot()


pass