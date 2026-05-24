from .blocks import (
    SingleBlock, ListBlock
)
from ._blockUtils import _calc_routine
from .template import TemplateBlock, TemplateList

from .._debug import Debug
_debug = Debug()

class Treatment(SingleBlock):
    # Maps type strings to subclass constructors.
    # Populated after each subclass definition.
    dispatch = {}

    @classmethod
    def dispatch_subclass(cls, blockDict):
        from .blocks import _unwrap_block
        blockDict = _unwrap_block(blockDict)
        t = blockDict.get("type", None)
        subclass = cls.dispatch.get(t,cls)
        return subclass(blockDict, _dispatched=True)
 
    @_calc_routine
    def example_calc(self):
        _debug.msg(f"Running example routine for {self.type} treatment")
        return None

class Annealing(Treatment):
    dispatch = {}
    def __init__(self, blockDict, _dispatched=False):
        super().__init__(blockDict, _dispatched=_dispatched)
        self.build_profile()
    
    def build_profile(self, **kwargs):
        from cif2xrd.furnace import Profile #type: ignore
        import matplotlib.pyplot as plt

        furnace = Profile(**kwargs)

        for section in self.program:
            if section.type == "ramp":
                temp = int(section.temp.split(" ")[0])
                furnace.ramp(temp, section.time)
            elif section.type == "dwell":
                furnace.dwell(section.time)
            elif section.type == "quench":
                furnace.quench(section.medium)

        self._profile = furnace
    
    def update_profile(self, **kwargs):
        return self._profile.update_params(**kwargs)

    def show_plot(self, **kwargs):
        self.update_profile(**kwargs)
        return self._profile.plot(show=True)
    
    def interactive_plot(self, **kwargs):
        self.update_profile(**kwargs)
        return self._profile.interactive()
Treatment.dispatch["anneal"] = Annealing

class AnnealSection(SingleBlock):
    dispatch = {}

    @classmethod
    def dispatch_subclass(cls, blockDict):
        from .blocks import _unwrap_block
        blockDict = _unwrap_block(blockDict)
        t = blockDict.get("type",None)
        subclass = cls.dispatch.get(t,cls)
        return subclass(blockDict,_dispatched=True)
    
class Ramp(AnnealSection):
    dispatch = {}
AnnealSection.dispatch["ramp"] = Ramp

class Dwell(AnnealSection):
    dispatch = {}
AnnealSection.dispatch["dwell"] = Dwell

class Quench(AnnealSection):
    dispatch = {}
AnnealSection.dispatch["quench"] = Quench

class AnnealProgram(ListBlock):
    _reqCls = AnnealSection
    def append(self, obj):
        super().append(obj)
        if hasattr(self, "_parent_block") and self._parent_block is not None:
            self._parent_block.build_profile()