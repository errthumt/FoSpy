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
    for temp, time in [v.strip() for v in value.split("/")]:
        if temp not in allowed_units["temp"]:
            raise ValueError(f"Invalid temperature unit '{temp}' in rate '{value}'. Must be one of: {allowed_units['temp']}")
        if time not in allowed_units["time"]:
            raise ValueError(f"Invalid time unit '{time}' in rate '{value}'. Must be one of: {allowed_units['time']}")
    return value

def convert_time_unit(val, in_unit, out_unit):
    if in_unit == out_unit:
        return val
    if in_unit == "s":
        if out_unit == "min":
            return val / 60
        elif out_unit == "h":
            return val / 3600
    elif in_unit == "min":
        if out_unit == "s":
            return val * 60
        elif out_unit == "h":
            return val / 60
    elif in_unit == "h":
        if out_unit == "s":
            return val * 3600
        elif out_unit == "min":
            return val * 60
    raise ValueError(f"Cannot convert from '{in_unit}' to '{out_unit}'")