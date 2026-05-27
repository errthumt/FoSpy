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

def temp_units(value):
    if value not in allowed_units["temp"]:
        raise ValueError(f"Invalid temperature unit '{value}'. Must be one of: {allowed_units['temp']}")
    return value

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