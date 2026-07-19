from .blocks import (
    SingleBlock, ListBlock
)
from ._blockUtils import _calc_routine

from .. import _errors as err

from .._debug import Debug
_debug = Debug()

class Treatment(SingleBlock):
    _id_key = "type"


@Treatment.set_dispatch("composition", from_key="type")
class CompChange(Treatment):
    pass

@Treatment.set_dispatch("anneal")
class Annealing(Treatment):
    def __init__(self, blockDict, _dispatched=False):
        super().__init__(blockDict, _dispatched=_dispatched)
        self.build_profile()
    
    def build_profile(self, **kwargs):
        from .template import TemplateBlock
        if isinstance(self, TemplateBlock):
            from warnings import warn
            warn("Cannot build profile for a template annealing block. Skipping profile build.")
            return None
        
        try:
            # TODO: use importlib.util.find_spec to test for availability
            from cif2xrd.furnace import Profile #type: ignore
            import matplotlib.pyplot as plt  # noqa: F401
        except ImportError as e:
            from warnings import warn
            warn(f"Could not import furnace module. Skipping profile build. Exception:\n{e}", RuntimeWarning)
            return None

        furnace = Profile(**kwargs)

        for section in self.program:
            if section.type == "ramp":
                temp = section.get_temp("C").magnitude
                furnace.ramp(temp, f"{section.get_time('h').magnitude} h")
            elif section.type == "dwell":
                furnace.dwell(f"{section.get_time('h').magnitude} h")
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


class AnnealSection(SingleBlock):
    _id_key = "type"
    
    @_calc_routine
    def add_missing_parameter(self):
        return
    
    def get_time(self, time_units="h"):
        from ..parsing.validators.units import FOSQuantity, FOSUnit
        if not hasattr(self, "time"):
            raise ValueError("This Anneal section does not have a 'time' attribute.")
        
        time = FOSQuantity(float(self.time.magnitude), self.time.units)
        value = time.to(FOSUnit(time_units))
        return value

@AnnealSection.set_dispatch("ramp", from_key="type", allow_self=False)   
class Ramp(AnnealSection):
    def __init__(self, blockDict, _dispatched=False):
        super().__init__(blockDict, _dispatched=_dispatched)

    @AnnealSection.make_dispatch
    def dispatch_subclass(cls, blockDict, **kwargs):

        seeking = cls.dispatch.keys()
        found = {}
        for key in seeking:
            found_val = blockDict.pop(key,None)
            if found_val is not None and len(found) < len(seeking)-1:
                found[key] = found_val

        missing = [k for k in seeking if k not in found]

        if len(missing) > 1:
            raise err.MissingPropertyError(' or '.join(missing), cls, blockDict=blockDict)
        
        missing = missing[0]
        
        blockDict.update(found)
        blockDict[cls.dispatch_key] = missing
            
        return super(AnnealSection, cls)
            
    def get_rate(self, temp_units="C", time_units="h"):
        from ..parsing.validators.units import FOSTempUnit, FOSUnit, FOSQuantity
        if not hasattr(self, "rate"):
            raise ValueError("Ramp section does not have a 'rate' attribute. Conisder reclassifying this section as a RampNoRate section.")
        new_unit = FOSUnit(f"{FOSTempUnit(temp_units)}/{FOSUnit(time_units,'[time]')}")
        rate = FOSQuantity(float(self.rate.magnitude),self.rate.units)
        value = rate.to(new_unit)
        return value
    
    def get_temp(self, temp_units="C"):
        from ..parsing.validators.units import FOSTempUnit, FOSQuantity
        if not hasattr(self, "temp"):
            raise ValueError("Ramp section does not have a 'temp' attribute. Conisder reclassifying this section as a RampNoTemp section.")
        temp = FOSQuantity(float(self.temp.magnitude),self.temp.units)
        value = temp.to(FOSTempUnit(temp_units))
        return value
    

@Ramp.set_dispatch("temp", from_key="_ramp_missing", allow_self=False)
class RampNoTemp(Ramp):
    def get_temp(self, temp_units="C"):
        from ..parsing.validators.units import FOSQuantity, FOSTempUnit, _to_decimal
        try:
            ramp_set = self._parent_block.get_any(type="ramp")
            self_idx = ramp_set.index(self)
            if self_idx == 0:
                last_temp = self._parent_block._parent_block.start_temp
            else:
                last_temp = ramp_set[self_idx-1].get_temp(temp_units)
        #TODO: decrease exception scope to avoid hiding other exceptions
        except Exception:
            last_temp = FOSQuantity(25,FOSTempUnit(temp_units))

        last_temp = _to_decimal(last_temp)

        rate = _to_decimal(self.get_rate(temp_units, "h"))
        time = _to_decimal(self.get_time("h"))

        temp = last_temp + rate * time
        return temp

    @_calc_routine
    def add_missing_parameter(self):
        temp_unit = [v.strip() for v in self.rate_units.split("/")][0]
        temp = self.get_temp(temp_unit)
        self.add_calc_comment("time", f"Temperature after ramp: {temp} {temp_unit}", "missing temp")

@Ramp.set_dispatch("time")
class RampNoTime(Ramp):
    def get_time(self, time_units="h"):
        from ..parsing.validators.units import FOSQuantity, FOSTempUnit, _to_decimal
        try:
            ramp_set = self._parent_block.get_any(type="ramp")
            self_idx = ramp_set.index(self)
            if self_idx == 0:
                last_temp = self._parent_block._parent_block.start_temp
            else:
                last_temp = ramp_set[self_idx-1].get_temp("K")
        #TODO: decrease exception scope to avoid hiding other exceptions
        except Exception:
            last_temp = FOSQuantity(float(25),FOSTempUnit("K"))

        last_temp = _to_decimal(last_temp)
        rate = _to_decimal(self.get_rate("K", time_units))
        temp = _to_decimal(self.get_temp("K"))

        time = (temp - last_temp) / rate
        return time
    
    @_calc_routine
    def add_missing_parameter(self):
        time_unit = [v.strip() for v in self.rate_units.split("/")][1]
        time = self.get_time(time_unit)
        self.add_calc_comment("temp", f"Time for ramp: {time} {time_unit}", "missing time")

@Ramp.set_dispatch("rate")
class RampNoRate(Ramp):
    def get_rate(self, temp_units="C", time_units="h"):
        from ..parsing.validators.units import FOSQuantity, FOSTempUnit, _to_decimal
        try:
            ramp_set = self._parent_block.get_any(type="ramp")
            self_idx = ramp_set.index(self)
            if self_idx == 0:
                last_temp = self._parent_block._parent_block.start_temp
            else:
                last_temp = ramp_set[self_idx-1].get_temp(temp_units)
        #TODO: decrease exception scope to avoid hiding other exceptions
        except Exception:
            last_temp = FOSQuantity(25,FOSTempUnit("C"))

        last_temp = _to_decimal(last_temp)

        delta_temp = self.get_temp(temp_units)-last_temp
        time = self.get_time(time_units)
        rate = delta_temp / time
        return rate
    
    @_calc_routine
    def add_missing_parameter(self):
        rate = self.get_rate()
        self.add_calc_comment("temp", f"Rate for ramp: {rate}", "missing rate")

@AnnealSection.set_dispatch("dwell")
class Dwell(AnnealSection):
    pass
    

@AnnealSection.set_dispatch("quench")
class Quench(AnnealSection):
    pass


class AnnealProgram(ListBlock):
    _reqCls = AnnealSection
    def append(self, obj):
        super().append(obj)
        if hasattr(self, "_parent_block") and self._parent_block is not None:
            self._parent_block.build_profile()
    
    @_calc_routine
    def add_all_missing_parameters(self):
        for section in self:
            if hasattr(section, "add_missing_parameter"):
                section.add_missing_parameter()


TreatmentList = ListBlock.Simple(Treatment)
"""
A [simple list][FoSpy.blocks.blocks.ListBlock.Simple] of
[`Treatment` objects][FoSpy.blocks.treatments.Treatment].
"""


class GasFlow(SingleBlock):
    pass


FlowList = ListBlock.Simple(GasFlow)

