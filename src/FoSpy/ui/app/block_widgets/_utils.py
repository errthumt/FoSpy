from PySide6.QtWidgets import QLabel

def _widget_not_found(*_):
    return QLabel("ERROR: No Widget Found")

def _get_editor(value, blk_widget=None, prop=None):
    prop_map = blk_widget.prop_map if (
        blk_widget is not None and
        hasattr(blk_widget, "prop_map")
    ) else None

    builder = _get_widget(value, prop_map, prop)
    
    if builder is _widget_not_found:
        if hasattr(value, "serialize") and callable(value.serialize):
            return _get_editor(value.serialize())

        return _get_editor(str(value))

    editor, enabler = builder

    if not callable(enabler):
        def static_enabler(val, e=enabler):
            return e
        enabler = static_enabler

    return editor, enabler


def _get_widget(blk, prop_map=None, prop=None):
    if prop_map is not None:
        if prop in prop_map:
            return prop_map[prop]
        elif "__all__" in prop_map:
            return prop_map["__all__"]
        
    from . import widget_map
        
    for k, v in widget_map.items():
        if isinstance(blk, k):
            return v
        
    return _widget_not_found