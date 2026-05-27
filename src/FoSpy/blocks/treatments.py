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
 
    @_calc_routine(attach=False)
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
                temp = section.get_temp("C")
                furnace.ramp(temp, f"{section.get_time('h')} h")
            elif section.type == "dwell":
                furnace.dwell(f"{section.get_time('h')} h")
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
        if subclass is cls:
            return cls(blockDict, _dispatched=True)
        return subclass.dispatch_subclass(blockDict)
    
    @_calc_routine()
    def add_missing_parameter(self):
        return
    
class Ramp(AnnealSection):
    dispatch = {}

    def __init__(self, blockDict, _dispatched=False):
        super().__init__(blockDict, _dispatched=_dispatched)

    @classmethod
    def dispatch_subclass(cls, blockDict):
        from ._blockUtils import _unwrap_block
        blockDict = _unwrap_block(blockDict)
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
                blockDict.pop(key,None)
                subclass = cls.dispatch.get(key,None)
                if subclass is None:
                    raise ValueError(f"Ramp section missing required key '{key}' and no subclass found to handle this case.")
                return subclass(blockDict, _dispatched=True)
            
    def get_rate(self, temp_units="C", time_units="h"):
        from ..parsing.validators.units import convert_temp, convert_time
        if not hasattr(self, "rate"):
            raise ValueError("Ramp section does not have a 'rate' attribute. Conisder reclassifying this section as a RampNoRate section.")
        
        current_temp, current_time = [v.strip() for v in self.rate_units.split("/")]
        value = self.rate()
        value = convert_temp(value, current_temp, temp_units)
        value = convert_time(value, time_units, current_time)
        return value
    
    def get_temp(self, temp_units="C"):
        from ..parsing.validators.units import convert_temp
        if not hasattr(self, "temp"):
            raise ValueError("Ramp section does not have a 'temp' attribute. Conisder reclassifying this section as a RampNoTemp section.")
        
        current_temp = self.temp_units
        value = self.temp()
        value = convert_temp(value, current_temp, temp_units)
        return value
    
    def get_time(self, time_units="h"):
        from ..parsing.validators.units import convert_time
        if not hasattr(self, "time"):
            raise ValueError("Ramp section does not have a 'time' attribute. Conisder reclassifying this section as a RampNoTime section.")
        
        current_time = self.time_units
        value = self.time()
        value = convert_time(value, current_time, time_units)
        return value
    



AnnealSection.dispatch["ramp"] = Ramp

class RampNoTemp(Ramp):
    dispatch = {}
    def get_temp(self, temp_units="C"):
        from ..parsing.validators.units import convert_temp
        current_temp, current_time = [v.strip() for v in self.rate_units.split("/")]
        rate = self.get_rate(current_temp, current_time)
        time = self.get_time(current_time)
        temp = rate * time
        temp = convert_temp(temp, current_temp, temp_units)
        return temp
    @classmethod
    def dispatch_subclass(cls, blockDict):
        return cls(blockDict, _dispatched=True)

    @_calc_routine()
    def add_missing_parameter(self):
        temp_unit = [v.strip() for v in self.rate_units.split("/")][0]
        temp = self.get_temp(temp_unit)
        self.add_calc_comment("time", f"Temperature after ramp: {temp} {temp_unit}", "missing temp")

Ramp.dispatch["temp"] = RampNoTemp

class RampNoTime(Ramp):
    dispatch = {}
    def get_time(self, time_units="h"):
        from ..parsing.validators.units import convert_time
        current_temp, current_time = [v.strip() for v in self.rate_units.split("/")]
        rate = self.get_rate(current_temp, current_time)
        temp = self.get_temp(current_temp)
        time = temp / rate
        time = convert_time(time, current_time, time_units)
        return time
    @classmethod
    def dispatch_subclass(cls, blockDict):
        return cls(blockDict, _dispatched=True)
    
    @_calc_routine()
    def add_missing_parameter(self):
        time_unit = [v.strip() for v in self.rate_units.split("/")][1]
        time = self.get_time(time_unit)
        self.add_calc_comment("temp", f"Time for ramp: {time} {time_unit}", "missing time")
Ramp.dispatch["time"] = RampNoTime

class RampNoRate(Ramp):
    dispatch = {}
    def get_rate(self, temp_units="C", time_units="h"):
        temp = self.get_temp(temp_units)
        time = self.get_time(time_units)
        rate = temp / time
        return rate
    
    @classmethod
    def dispatch_subclass(cls, blockDict):
        return cls(blockDict, _dispatched=True)
    
    @_calc_routine()
    def add_missing_parameter(self):
        temp_unit = self.temp_units
        time_unit = self.time_units
        rate = self.get_rate(temp_unit, time_unit)
        self.add_calc_comment("temp", f"Rate for ramp: {rate} {temp_unit}/{time_unit}", "missing rate")
Ramp.dispatch["rate"] = RampNoRate

class Dwell(AnnealSection):
    dispatch = {}
    def get_time(self, time_units="h"):
        from ..parsing.validators.units import convert_time
        current_time = self.time_units
        value = self.time
        value = convert_time(value, current_time, time_units)
        return value
    
    @classmethod
    def dispatch_subclass(cls, blockDict):
        return cls(blockDict, _dispatched=True)
    
AnnealSection.dispatch["dwell"] = Dwell

class Quench(AnnealSection):
    dispatch = {}
    @classmethod
    def dispatch_subclass(cls, blockDict):
        return cls(blockDict, _dispatched=True)
AnnealSection.dispatch["quench"] = Quench

class AnnealProgram(ListBlock):
    _reqCls = AnnealSection
    def append(self, obj):
        super().append(obj)
        if hasattr(self, "_parent_block") and self._parent_block is not None:
            self._parent_block.build_profile()
    
    @_calc_routine()
    def add_all_missing_parameters(self):
        for section in self:
            if hasattr(section, "add_missing_parameter"):
                section.add_missing_parameter()