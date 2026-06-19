from .._utils import _ceil_to, _floor_to


def _round_spec(x, digits, key=None, include=True):
    if isinstance(x, list or tuple):
        return [_round_spec(xi, digits) for xi in x]
    elif key == "min":
        val = _floor_to(x, digits)
        if not include:
            val += 10**-digits
        return val
    elif key == "max":
        val = _ceil_to(x, digits)
        if not include:
            val -= 10**-digits
        return val
    elif key == "None":
        return round(x, digits)
    else:
        return round(x, digits) if x is not None else None