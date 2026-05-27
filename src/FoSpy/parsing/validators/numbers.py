from decimal import Decimal

def positive_decimal(label):
    def func(val):
        try:
            decimal_val = Decimal(val)
        except:
            raise ValueError(f"Unable to convert '{label}: {val}' into a decimal number.")
        if decimal_val > 0:
            return decimal_val
        else:
            raise ValueError(f"Value for '{label}' must be a positive number.")
    return func
