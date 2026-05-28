from pint import UnitRegistry, Quantity, Unit

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

allowed_units = {
    "mass" : [
        "g",
        "grams",
        "mg",
        "milligrams",
        "ug",
        "micrograms",
        "kg",
        "kilograms"
    ],
    "molar" : [
        "molar ratio",
        "mol ratio",
        "mole ratio",
        "moles",
        "mols",
        "mol"
    ],
    "volume": [
        "mL",
        "uL",
        "L",

    ],
    "time" : [
        "s",
        "min",
        "h"
    ],
    "temp" : [
        "K",
        "C",
        "F"
    ]
}

def attach_unit(value, value_key, cls, sourceDict):
    unit_key = f"{value_key}_unit"
    if unit_key not in sourceDict:
        raise ValueError(f"Could not find required unit for: '{value_key}'")
    
    unit = sourceDict[unit_key]
    
    validators = cls.build_validators()
    unit_validator = validators.get(unit_key, Unit)

    unit = unit_validator(unit)

    return FOSQuantity(value, unit)

    




def mass_unit(key:str):
    def func(unit:str):
        if unit in allowed_units["mass"]:
            return unit
        else:
            raise ValueError(f"'{unit}' is not a recognized mass unit for '{key}'")
    return func

def time_units(value):
    if value not in allowed_units["time"]:
        raise ValueError(f"Invalid time unit '{value}'. Must be one of: {allowed_units['time']}")
    return value

def temp_unit(value):
    if not value.startswith("deg"):
        value = f"deg{value}"
    return FOSUnit.enforce_dims("[temperature]")

def rate_units(value):
    temp, time = [v.strip() for v in value.split("/")]
    if temp not in allowed_units["temp"]:
        raise ValueError(f"Invalid temperature unit '{temp}' in rate '{value}'. Must be one of: {allowed_units['temp']}")
    if time not in allowed_units["time"]:
        raise ValueError(f"Invalid time unit '{time}' in rate '{value}'. Must be one of: {allowed_units['time']}")
    return value


time_conversions = {
    "s": {
        "min": lambda val: val / 60,
        "h": lambda val: val / 3600
    },
    "min": {
        "s": lambda val: val * 60,
        "h": lambda val: val / 60
    },
    "h": {
        "s": lambda val: val * 3600,
        "min": lambda val: val * 60
    }
}

def convert_time(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value
    if from_unit not in time_conversions:
        raise ValueError(f"Invalid 'from' time unit '{from_unit}'. Must be one of: {list(time_conversions.keys())}")
    if to_unit not in time_conversions[from_unit]:
        raise ValueError(f"Invalid 'to' time unit '{to_unit}'. Must be one of: {list(time_conversions[from_unit].keys())}")
    return time_conversions[from_unit][to_unit](value)

temp_conversions = {
    "C": {
        "K": lambda val: val + 273.15,
        "F": lambda val: (val * 9/5) + 32
    },
    "K": {
        "C": lambda val: val - 273.15,
        "F": lambda val: (val - 273.15) * 9/5 + 32
    },
    "F": {
        "C": lambda val: (val - 32) * 5/9,
        "K": lambda val: (val - 32) * 5/9 + 273.15
    }
}

def convert_temp(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value
    if from_unit not in temp_conversions:
        raise ValueError(f"Invalid 'from' temperature unit '{from_unit}'. Must be one of: {list(temp_conversions.keys())}")
    if to_unit not in temp_conversions[from_unit]:
        raise ValueError(f"Invalid 'to' temperature unit '{to_unit}'. Must be one of: {list(temp_conversions[from_unit].keys())}")
    return temp_conversions[from_unit][to_unit](value)