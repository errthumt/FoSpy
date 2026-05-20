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
        from . import unwrap_block
        blockDict = unwrap_block(blockDict)
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
    dispatch = {}
    def __init__(self, blockDict):
        super().__init__(blockDict)
    @classmethod
    def subclass(cls, blockDict):
        return cls(blockDict)
Treatment.dispatch["anneal"] = Annealing

class AnnealSection(SingleBlock):
    dispatch = {}

    @classmethod
    def subclass(cls, blockDict):
        from . import unwrap_block
        blockDict = unwrap_block(blockDict)
        t = blockDict.get("type")
        subclass = cls.dispatch.get(t,cls)
        return subclass(blockDict)
    
class Ramp(AnnealSection):
    dispatch = {}
AnnealSection.dispatch["ramp"] = Ramp

class Dwell(AnnealSection):
    dispatch = {}
AnnealSection.dispatch["dwell"] = Dwell

