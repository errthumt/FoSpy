from decimal import Decimal
from .units import attach_unit

def positive_decimal(label, value_key, require_unit=False):
    def func(val):
        try:
            decimal_val = Decimal(val)
        except Exception as e:
            raise ValueError(f"Unable to convert '{label}: {val}' into a decimal number. Exception:\n{e}")
        if not decimal_val > 0:
            raise ValueError(f"Value for '{label}' must be a positive number.")
        return decimal_val
    
    if require_unit:
        def unit_func(val, cls, sourceDict):
            return attach_unit(func(val), value_key, cls, sourceDict)
        return unit_func
    return func
            

def decimal_range(label, value_key, lower=0, upper=1, include_lower=False, include_upper=True, require_unit=False):
    def func(val, sourceDict):
        try:
            value = Decimal(val)
        except Exception as e:
            raise ValueError(f"Unable to convert value: '{val}' into a decimal for '{label}'. Exception:\n{e}")
        if any((
            value < lower or value > upper,
            value == lower and not include_lower,
            value == upper and not include_upper
        )):
            raise ValueError(
                f"'{val}' not allowed for '{label}'. Value must be in range: "
                f"{lower}{'<=' if include_lower else '<'}"
                f"val{'<=' if include_upper else '<'}{upper}"
            )
        return value
    
    if require_unit:
        def unit_func(val, cls, sourceDict):
            return attach_unit(func(val), value_key, cls, sourceDict)
        return unit_func
    return func

def any_decimal(label, value_key, require_unit=False):
    def func(val, sourceDict):
        try:
            value = Decimal(val)
        except Exception as e:
            raise ValueError(f"Unable to convert value: '{val}' into a decimal for '{label}'. Exception:\n{e}")
        return value
    
    if require_unit:
        def unit_func(val, cls, sourceDict):
            return attach_unit(func(val), value_key, cls, sourceDict)
        return unit_func
    return func

