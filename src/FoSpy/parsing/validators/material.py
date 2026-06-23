from decimal import Decimal

def purity(block:str):
    def func(val):
        try:
            purity = Decimal(val)
        except Exception as e:
            raise ValueError(f"Unable to convert purity: '{val}' into a number for '{block}' block. Exception:\n{e}")
        if purity > 0 and purity <=1:
            return purity
        else:
            raise ValueError(f"Purity of '{val}' not allowed for '{block}' block. Purity must be a non-zero decimal between 0 and 1")
    return func