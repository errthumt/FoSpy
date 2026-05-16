from . import (
    SingleBlock, ListBlock, 
    TemplateBlock, TemplateList,
    calc_routine)
from .._debug import Debug

_debug = Debug()
_debug.on = True

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
    
class TreatmentTemplate(Treatment, TemplateBlock):
    def __init__(self, blockDict):
        super().__init__(blockDict)

class Annealing(Treatment):
    def __init__(self, blockDict):
        super().__init__(blockDict)
Treatment.dispatch["anneal"] = Annealing

class AnnealSection(SingleBlock):
    def __init__(self, blockDict):
        super().__init__(blockDict)

class AnnealProgram(ListBlock):
    def __init__(self, blockList):
        # _debug.msg("Constructing annealing program")
        super().__init__(blockList, AnnealSection)

class TreatmentList(ListBlock):
    def __init__(self, blockList, cls=Treatment):
        super().__init__(blockList, cls)

class TreatTempList(TreatmentList, TemplateList):
    def __init__(self, blockList):
        super().__init__(blockList, cls=TreatmentTemplate)