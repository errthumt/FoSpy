def _prune_template_names(struct):
    if isinstance(struct, dict):
        struct = struct.copy()
        struct.pop("template_name", None)
        for key, val in struct.items():
            struct[key] = _prune_template_names(val)
    elif isinstance(struct, list):
        struct = struct.copy()
        struct = [_prune_template_names(v) for v in struct]

    return struct

def _calc_routine(func):
    """
    Decorator for `SingleBlock` or `ListBlock` methods that calculate values
    from existing attributes.

    `calc_routine` functions can be called at any time, but can also be queued
    to run at serialization, as in refreshing relevant calculated values before
    saving the file. See `SingleBlock.add_calc_routine()`
    """

    func._is_calc_routine = True
    func.__doc__ = (func.__doc__ or "") + "\nThis function is decorated as a calc_routine"

    return func


def _unwrap_block(struct):
    from .blocks import SingleBlock
    while isinstance(struct,list) and len(struct) == 1:
        struct = struct[0]

    if isinstance(struct,SingleBlock):
        struct = struct.serialize(keepListType=True)
        struct = _unwrap_block(struct)
    return struct

def _unwrap_listblock(struct, typ:type=None):
    from .blocks import ListBlock
    if isinstance(struct, ListBlock):
        return struct.serialize()
    if isinstance(struct, typ):
        return [struct]
    if not isinstance(struct, list):
        return [_unwrap_block(struct)]
    
    out = []
    for s in struct:
        out.extend(_unwrap_listblock(s, typ))
    return out


def _template_found(val):
    from FoSpy.blocks.template import TemplateField
    if val == TemplateField().serialize():
        return True

    if isinstance(val, list):
        for d in val:
            if _template_found(d):
                return True
        return False

    if isinstance(val, dict):
        for key, v in val.items():
            if key != "template_name" and _template_found(v):
                return True
        return False

    return False

def _is_full_template(val):
    from FoSpy.blocks.template import TemplateField
    if val == TemplateField().serialize():
        return True

    if isinstance(val, list):
        if len(val) != 1:
            return False
        if type(val[0]) is not dict:
            return False
        return _is_full_template(val[0])

    if isinstance(val, dict):
        for key, v in val.items():
            if key != "template_name" and not (key.startswith("_") or _is_full_template(v)):
                return False
        return True
    
def _get_block_classes(module):
    from .blocks import Block
    import inspect

    __block_classes__ = []

    for name, obj in inspect.getmembers(module, inspect.isclass):
        if obj.__module__ != module.__name__:
            continue

        if issubclass(obj, Block):
            __block_classes__.append(name)

    return __block_classes__

def _show_quick_pattern(df, ax, x, y):
    from matplotlib import pyplot as plt
    df.plot(ax=ax, x=x, y=y)
    plt.show()
