from . import (
    SingleBlock, ListBlock, 
    TemplateBlock, TemplateList,
    calc_routine)

from .._debug import Debug
_debug = Debug()

class Treatment(SingleBlock):
    # Maps type strings to subclass constructors.
    # Populated after each subclass definition.
    dispatch = {}

    @classmethod
    def subclass(cls, blockDict):
        t = blockDict.get("type")
        subclass = cls.dispatch.get(t,cls)
        return subclass(blockDict)

    def __init__(self, blockDict):
        super().__init__(blockDict)
    
    @calc_routine
    def example_calc(self):
        _debug.msg(f"Running example routine for {self.type} treatment")
        return None

class Annealing(Treatment):
    def __init__(self, blockDict):
        super().__init__(blockDict)
Treatment.dispatch["anneal"] = Annealing

class AnnealSection(SingleBlock):
    def __init__(self, blockDict):
        super().__init__(blockDict)

