from PySide6.QtWidgets import QLabel

def _widget_not_found(*_):
    return QLabel("ERROR: No Widget Found")

def _get_editor(value, blk_widget=None):
    widget_map = blk_widget.widget_map if hasattr(blk_widget, "widget_map") else None

    builder = _get_widget(value, widget_map)
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


def _get_widget(blk, widget_map=None):
    from . import widget_map as defaults

    if widget_map is None:
        widget_map = defaults
    else:
        for k, v in defaults.items():
            if k not in widget_map:
                widget_map[k] = v

    for k, v in widget_map.items():
        if isinstance(blk, k):
            return v
        
    return _widget_not_found