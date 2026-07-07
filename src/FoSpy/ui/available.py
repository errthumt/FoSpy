from importlib import util as imp_util, import_module
from types import ModuleType

class UINotAvailable(Exception):
    pass

def _is_package_installed(package_name:str) -> bool:
    return imp_util.find_spec(package_name) is not None

def _check_requirement(req:str|list|tuple) -> bool:
    if isinstance(req, str):
        return _is_package_installed(req)
    
    if isinstance(req, tuple):
        return all(_check_requirement(dep) for dep in req)
    
    if isinstance(req, list):
        return any(_check_requirement(dep) for dep in req)
    
    # shouldn't get here
    raise ValueError(f"Unknown logic structure for requirement: {type(req)}. "
                     "Expected str, list, or tuple.")

_UI_REQUIREMENTS = {
    "pyqtgraph": ("pyqtgraph", ["PySide6", "PyQt6", "PySide2", "PyQt5"]),
    "pyside6": "PySide6",
    "native": ("tkinter", "matplotlib")
}

AVAILABLE_UIS = [ui for ui, req in _UI_REQUIREMENTS.items() if _check_requirement(req)]

def get_available_uis():
    return AVAILABLE_UIS

def is_ui_available(ui_name):
    return ui_name.lower() in AVAILABLE_UIS

def _summarize_reqs(req:str|list|tuple, indent=0):
    txt = f"{'  '*indent}- [{'OK' if _check_requirement(req) else 'XX'}] "

    if isinstance(req, str):
        return txt + req
    
    if isinstance(req, (tuple, list)):
        txt += "ALL OF:\n" if isinstance(req, tuple) else "ONE OF:\n"
        return txt + "\n".join([_summarize_reqs(dep, indent+1) for dep in req])
        
    # shouldn't get here
    raise ValueError(f"Unknown logic structure for requirement: {type(req)}. "
                     "Expected str, list, or tuple.")


def validate_ui(ui_name):
    ui_lower = ui_name.lower()
    if ui_lower not in _UI_REQUIREMENTS:
        valids = ", ".join(_UI_REQUIREMENTS.keys())
        raise UINotAvailable(f"UI '{ui_name}' is not a valid UI. Valid options are: {valids}.")
    
    if ui_lower not in AVAILABLE_UIS:
        raise UINotAvailable(
            f"The '{ui_name}' UI backend cannot be used because it is missing dependencies. "
            "Refer to the summary below and install the missing dependencies to use this UI.\n\n"
            f"{_summarize_reqs(_UI_REQUIREMENTS[ui_lower])}"
        )
    
def discover_ui_options(target:str|ModuleType) -> dict[str, ModuleType]:
    ui_opts = {}

    base_package = target.__name__ if isinstance(target, ModuleType) else str(target)
    
    for ui_name in get_available_uis():
        absolute_name = f"{base_package}.{ui_name}"

        spec = imp_util.find_spec(absolute_name)
        if spec is not None:
            ui_opts[ui_name] = import_module(absolute_name)

    return ui_opts
    
def get_valid_ui(ui_name=None, options=None):
    from ..config import values as cfg
    from warnings import warn


    ui_name = ui_name or cfg.get("ui.default", "native")
    if options is None:
        options = _UI_REQUIREMENTS.keys()
    else:
        options = [o.lower() for o in options]

    if ui_name.lower() not in options:
        new_ui = options[0]
        warn(f"\n\nThe '{ui_name}' backend is not avaialable for the requested context. "
             f"Attempting to use '{new_ui}' instead.", RuntimeWarning)

        ui_name = new_ui

    available_options = [o for o in options if o in AVAILABLE_UIS]
    installable_options = {o: _UI_REQUIREMENTS[o] for o in options if o in _UI_REQUIREMENTS}

    try:
        validate_ui(ui_name)
        return ui_name
    except UINotAvailable as e:
        if len(available_options) > 0:
            fallback = available_options[0]

            warn(f"\n\nThe '{ui_name}' UI backend is not available (exception below). "
                    f"Using the first available UI,'{fallback}', instead.\n\n{e}", RuntimeWarning)

            return fallback
        # proceed to raise if no fallback is available
    
    # Only reached on UINotAvailable and no fallback 
    summary = (f"The '{ui_name}' UI backend is not available. There are no "
                "available UIs to fallback to.\n"
                "Refer to the dependency summaries below and install the "
                "missing dependencies for your UI of choice.\nNOTE: The "
                "'native' UI is the most lightweight and is recommended for "
                "users looking for a simple UI or who don't use the UI "
                "often.\n\n")

    for ui, req in installable_options.items():
        summary += f"===== DEPENDENCIES FOR '{ui.upper()}' UI =====\n"
        summary += _summarize_reqs(req)
        summary += "\n\n"

    raise UINotAvailable(summary)


