def _calc_routine(attach=True):
    """
    Decorator for `SingleBlock` or `ListBlock` methods that calculate values
    from existing attributes.

    `calc_routine` functions can be called at any time, but can also be queued
    to run at serialization, as in refreshing relevant calculated values before
    saving the file. See `SingleBlock.add_calc_routine()`
    """
    def decorator(func):
        func._is_calc_routine = True
        func.__doc__ = (func.__doc__ or "") + "\nThis function is decorated as a calc_routine"

        return func
    return decorator

def _unwrap_block(struct):
    from .blocks import SingleBlock
    while isinstance(struct,list) and len(struct) == 1:
        struct = struct[0]

    if isinstance(struct,SingleBlock):
        struct = struct.serialize(keepListType=True)
        struct = _unwrap_block(struct)
    return struct

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
