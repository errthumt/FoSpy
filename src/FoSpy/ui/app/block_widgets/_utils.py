def _get_editor(value):
    from . import widget_map
    if type(value) in widget_map:
        editor, enabler = widget_map[type(value)]

        if not callable(enabler):
             def static_enabler(val, e=enabler):
                 return e
             enabler = static_enabler

        return editor, enabler

    if hasattr(value, "serialize") and callable(value.serialize):
        return _get_editor(value.serialize())

    return _get_editor(str(value))