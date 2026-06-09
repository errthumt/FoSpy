import pkgutil
import importlib
import sys
from ._blockUtils import _get_block_classes

from .._debug import Debug
_debug = Debug()
_debug.on = True

__all__ = []

package = sys.modules[__name__]

names = [name for _, name, ispkg in pkgutil.iter_modules(package.__path__) if not ispkg]

for name in sorted(names):
    module = importlib.import_module(f"{__name__}.{name}")
    
    module.__block_classes__ = _get_block_classes(module)

    for cls_name in module.__block_classes__:
        __all__.append(cls_name)

        globals()[cls_name] = getattr(module, cls_name)

