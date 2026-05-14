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
    ]
}

def mass_unit(key:str):
    def func(unit:str):
        if unit in allowed_units["mass"]:
            return unit
        else:
            raise ValueError(f"'{unit}' is not a recognized mass unit for '{key}'")
    return func