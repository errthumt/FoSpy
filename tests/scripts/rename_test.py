from FoSpy.blocks.synthesis import Synthesis
from FoSpy._debug import Debug, all_debugs_on

_debug = Debug()


mySyn = Synthesis.fromFile("tests/test_fos/start_synthesis.fos")

_debug.on = True
_debug.pmsg(mySyn.reagents)



pass