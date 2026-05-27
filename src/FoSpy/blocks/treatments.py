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
                temp = int(round(float(section.temp.split(" ")[0])))
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
        return subclass.dispatch_subclass(blockDict)
    
class Ramp(AnnealSection):
    dispatch = {}

    @classmethod
    def dispatch_subclass(cls, blockDict):
        seeking = ["temp","time","rate"]
        found = []
        for key in blockDict:
            if key in seeking:
                found.append(key)
            if len(found) == 2:
                break
        if len(found) != 2:
            raise ValueError(f"Ramp section must have at least two of the following keys: {seeking}. Found: {found}")
        
        for key in seeking:
            if key not in found:
                subclass = cls.dispatch.get(key,None)
                if subclass is None:
                    raise ValueError(f"Ramp section missing required key '{key}' and no subclass found to handle this case.")
                return subclass(blockDict, _dispatched=True)
    def get_ramp_rate(self, units):
        


AnnealSection.dispatch["ramp"] = Ramp

class RampNoTemp(Ramp):
    pass
AnnealSection.dispatch["temp"] = RampNoTemp

class RampNoTime(Ramp):
    pass
AnnealSection.dispatch["time"] = RampNoTime

class RampNoRate(Ramp):
    pass
AnnealSection.dispatch["rate"] = RampNoRate

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