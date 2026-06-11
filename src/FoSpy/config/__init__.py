import json
import types
import sys
import os
from . import _load as load
from ._enforce import enforce_config

module = sys.modules[__name__]

DEFAULT_FILE = load.get_default_file()
USER_FILE = load.get_user_file()

def save_all(filepath=None, prompt=True):
    current = module.values.to_dict()
    defaults = _load_defaults()

    if filepath is None:
        filepath = USER_FILE
    else:
        filepath = os.path.abspath(filepath)

    if (filepath == USER_FILE and 
        prompt and 
        input("WARNING: Saving the config will overwrite the existing user config "
              "and restart the session. Consider exporting the current user "
              "overrides with save(filepath) before saving.\n"
              "Proceed with saving? (y/n): ").lower() != "y"):
        return

    with open(filepath, 'w') as f:
        json.dump(_extract_user(defaults, current), f, indent=4)

    if filepath == USER_FILE:
        _restart_session()

def load_user(filepath=None):
    if filepath is None:
        filepath = USER_FILE
    else:
        filepath = os.path.abspath(filepath)
    with open(filepath, 'r') as f:
        new_config = _deep_merge(module.values.to_dict(), json.load(f))
    
    module.values = NestedConfig(new_config, "values")

def revert(prompt=True):
    if prompt and input("WARNING: Reverting the config to the last saved user config will "
                        "lose any unsaved changes.\n"
                        "Proceed with reversion? (y/n): ").lower() != "y":
        return
    module.values = NestedConfig(SESSION_START, "values")

def reset(prompt=True):
    if prompt and input("WARNING: Resetting the config to default values will delete the "
                        "existing user config and restart the session. Consider exporting "
                        "the current user overrides with save(filepath) before resetting. "
                        "You can also revert to the start of the session with revert().\n"
                        "Proceed with reset? (y/n): ").lower() != "y":
        return
    with open(USER_FILE, 'w') as f:
        f.write("{}")
    
    _restart_session()

def _restart_session():
    global SESSION_START
    SESSION_START = _load()
    module.values = NestedConfig(SESSION_START, "values")


def _load_defaults():
    with open(DEFAULT_FILE, 'r') as f:
        return json.load(f)
    
def _deep_merge(a, b):
    out = a.copy()
    for k, v in b.items():
        if k in out and isinstance(out[k], dict) and isinstance(v, dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out

def _extract_user(defaults, current):
    """
    Return only the parts of `current` that differ from `defaults`,
    in a structure that can be merged back over `defaults` to recover `current`.
    """


    if isinstance(defaults, dict) and isinstance(current, dict):
        out = {}
        keys = set(defaults) | set(current)
        for k in keys:
            if k not in defaults:

                out[k] = current[k]
            elif k in current:
                sub = _extract_user(defaults[k], current[k])
                if sub is not None:
                    out[k] = sub
        return out or None


    if isinstance(defaults, list) and isinstance(current, list):
        return current if defaults != current else None


    return current if defaults != current else None

def _load():
    out = _load_defaults()

    with open(USER_FILE, 'r') as f:
        out = _deep_merge(out, json.load(f))

    return out


class NestedConfig(types.ModuleType):
    def __init__(self, config_dict, name, *args, parent_name =__name__,**kwargs):
        super().__init__(f"{parent_name}.{name}", *args, **kwargs)
        self.__package__ = parent_name
        self.__file__ = __file__
        self.__all__ = []
        self._enforced = {}
        for key, val in config_dict.items():
            setattr(self, key, val)

    def __getattr__(self, key):
        # Auto-create nested modules
        mod = NestedConfig({}, key, parent_name=self.__name__)
        setattr(self, key, mod)
        return mod
    
    def __setattr__(self, key, val):
        # Convert dicts to nested modules automatically
        if not key.startswith("_"):
            if key in self._enforced:
                goodchecks, badchecks, hint=self._enforced[key]
                if (
                    not any(check(val) for check in goodchecks) or
                    any(check(val) for check in badchecks)
                ):
                    raise ValueError(f"Error setting config value '{key}': {hint}")
            if key not in self.__all__:
                self.__all__.append(key)

            if isinstance(val, dict):
                val = NestedConfig(val, key, parent_name=self.__name__)

        super().__setattr__(key, val)

    def __iter__(self):
        return iter(self())

    def to_dict(self):
        out = {}
        for key in self.__all__:
            val = getattr(self, key)
            if isinstance(val, NestedConfig):
                out[key] = val.to_dict()
            else:
                out[key] = val
        return out
    
    def get(self, key, default=None):
        val = getattr(self, key)
        if isinstance(val, NestedConfig):
            if val() == {}:
                return default
            return val()
        return val
    
    def __call__(self):
        return self.to_dict()
    
SESSION_START = None
values = None
    
_restart_session()

sys.modules[values.__name__] = values

__all__ = ["values"]

enforce_config()
