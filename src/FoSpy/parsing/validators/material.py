def purity(block:str):
    def func(val):
        try:
            purity = float(val)
        except:
            raise ValueError(f"Unable to convert purity: '{val}' into a number for '{block}' block.")
        if purity > 0 and purity <=1:
            return purity
        else:
            raise ValueError(f"Purity of '{val}' not allowed for '{block}' block. Purity must be a non-zero decimal between 0 and 1")
    return func
        
def ratio(val):
    try:
        ratio = float(val)
    except:
        raise ValueError(f"Unable to convert ratio: '{val}' into a number for 'Material' block.")
    
    if ratio >= 0:
        return ratio
    else:
        raise ValueError(f"Ratio of '{val}' not allowed for 'Material' block. Ratio must not be negative. If ratio is not relevant for this material, use 0.")