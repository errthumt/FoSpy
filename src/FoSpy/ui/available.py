from importlib import util as imp_util

def _is_package_installed(package_name:str) -> bool:
    return imp_util.find_spec(package_name) is not None

def _check_requirement(req:str|list|tuple) -> bool:
    if isinstance(req, str):
        return _is_package_installed(req)
    
    if isinstance(req, tuple):
        return all(_is_package_installed(dep) for dep in req)
    
    if isinstance(req, list):
        return any(_is_package_installed(dep) for dep in req)
    
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

def validate_ui_selection(ui_name):
    ui_lower = ui_name.lower()
    if ui_lower not in _UI_REQUIREMENTS:
        valids = ", ".join(_UI_REQUIREMENTS.keys())
        raise ValueError(f"UI '{ui_name}' is not a valid UI. Valid options are: {valids}.")
    
    if ui_lower not in AVAILABLE_UIS:
        missing = [dep for dep in _UI_REQUIREMENTS[ui_lower] if not _is_package_installed(dep)]
        raise ImportError(
            f"The '{ui_name}' UI backend cannot be used because the following "
            f"dependencies are missing: {', '.join(missing)}. "
            "Please pip install them to unlock this interface."
        )