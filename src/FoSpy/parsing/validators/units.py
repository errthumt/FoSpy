from pint import Quantity, Unit
import numpy as np

class FOSUnit(Unit):
    def __init__(self, unitlike, allow_dims=[]):
        super().__init__(units=unitlike)
        if not isinstance(allow_dims, list):
            allow_dims = [allow_dims]
        if len(allow_dims) != 0 and not any([self.dimensionality == dim for dim in allow_dims]):
            raise ValueError(f"Unit: '{unitlike}' is not a valid dimension. Valid dimensions are: "
                             f"{allow_dims}")
        
    @classmethod
    def enforce_dims(cls, allow_dims=[]):
        def constructor(unitlike):
            return cls(unitlike, allow_dims=allow_dims)
        return constructor
    
class FOSTempUnit(FOSUnit):
    def __init__(self, unitlike, rate=False, **kwargs):
        unitlike = str(unitlike)
        if not ("deg" in unitlike or "k" in unitlike.lower()):
            unitlike = f"deg{unitlike}"
        super().__init__(unitlike, allow_dims="[temperature]" if not rate else "[temperature]/[time]")
    
    @classmethod
    def enforce_dims(cls, **kwargs):
        return cls
    
def temp_rate_unit(unitlike):
    one = FOSQuantity(1, FOSTempUnit(unitlike, rate=True))
    zero = FOSQuantity(0, FOSTempUnit(unitlike, rate=True))
    diff = one - zero
    return diff.units

class FOSQuantity(Quantity):
    def serialize(self, **kwargs):
        return str(self.magnitude)

def attach_unit(value, value_key, cls, sourceDict):
    unit_key = f"{value_key}_unit"
    if unit_key not in sourceDict:
        raise ValueError(f"Could not find required unit for: '{value_key}'")
    
    unit = sourceDict[unit_key]
    
    validators = cls.build_validators()
    unit_validator = validators.get(unit_key, Unit)

    unit = unit_validator(unit)

    return FOSQuantity(value, unit)

def _to_decimal(quantity):
    typ = type(quantity)
    return typ(np.float64(quantity.magnitude), quantity.units)
