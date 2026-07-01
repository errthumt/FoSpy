# Auto-generated __init__.py

from . import filenames
from . import material
from . import numbers
from . import rename
from . import units

__all__ = [
    "filenames",
    "material",
    "numbers",
    "rename",
    "units",
]

def _validator_rules(*args):
    from ..._docs.properties import val_rules    
    lst = ["- " + arg for arg in args]
    txt = "\n".join(lst)
    def decorator(func, txt=txt):
        val_rules[func] = txt
        return func
    return decorator
    