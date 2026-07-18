from ..available import validate_ui, UINotAvailable
available = False
try:
    validate_ui("app")
    from . import window
    available = True
except UINotAvailable as e:
    import_e = e
except Exception as e:
    import_e = ImportError("App UI not available for unexpected exception")
    import_e.__cause__ = e

__all__ = ["window"]

def _import_gate():
    global available, import_e
    if not available:
        raise import_e
