from .._utils import _ceil_to, _floor_to


def _round_spec(x, digits, key=None):
    if isinstance(x, list or tuple):
        return [_round_spec(xi, digits) for xi in x]
    elif key == "min":
        return _floor_to(x, digits)
    elif key == "max":
        return _ceil_to(x, digits)
    elif key == "None":
        return round(x, digits)
    else:
        return round(x, digits) if x is not None else None