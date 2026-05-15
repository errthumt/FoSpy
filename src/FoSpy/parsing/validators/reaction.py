from decimal import Decimal

def nominal_mass(val):
    try:
        nominal_mass = Decimal(val)
    except:
        raise ValueError(f"Unable to convert 'nominal_mass: {val}' into a decimal number.")
    if nominal_mass > 0:
        return nominal_mass
    else:
        raise ValueError(f"Reaction value for 'nominal_mass' must be a positive number.")