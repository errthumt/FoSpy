import json
import types
import sys
import os
import copy
from . import _load as load
from ._enforce import enforce_config

module = sys.modules[__name__]

DEFAULT_FILE = load.get_default_file()
USER_FILE = load.get_user_file()

def save_all(filepath=None, prompt=True):
    global values

    if (filepath == USER_FILE and 
        prompt and 
        input("WARNING: Saving the config will overwrite the existing user config "
              "and restart the session. Consider exporting the current user "
              "overrides with save(filepath) before saving.\n"
              "Proceed with saving? (y/n): ").lower() != "y"):
        return
    
    values.save(filepath)

def load_user(filepath=None):
    global values
    if filepath is None:
        filepath = USER_FILE
    else:
        filepath = os.path.abspath(filepath)
    with open(filepath, 'r') as f:
        new_config = _deep_merge(values.to_dict(), json.load(f))
    
    values = NestedConfig(new_config, "values")

def revert(prompt=True):
    global values
    if prompt and input("WARNING: Reverting the config to the last saved user config will "
                        "lose any unsaved changes.\n"
                        "Proceed with reversion? (y/n): ").lower() != "y":
        return
    values.revert()

def reset(prompt=True):
    global values
    if prompt and input("WARNING: Resetting the config to default values will delete the "
                        "existing user config and restart the session. Consider exporting "
                        "the current user overrides with save(filepath) before resetting. "
                        "You can also revert to the start of the session with revert().\n"
                        "Proceed with reset? (y/n): ").lower() != "y":
        return
    with open(USER_FILE, 'w') as f:
        f.write("{}")
    
    values._load_from(_load_defaults())

def _restart_session():
    global values

    if values is None:
        values = NestedConfig(_load(), "values")
    else:
        values.revert()


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
        out = _deep_merge(out, json.load(f) or {})

    return out


class NestedConfig(types.ModuleType):
    def __init__(self, config_dict, name, *args, parent_name =__name__, path=None, **kwargs):
        super().__init__(f"{parent_name}.{name}", *args, **kwargs)
        self.__package__ = parent_name
        self.__file__ = __file__
        self.__all__ = []
        self._enforced = {}

        self._path = path.copy() if path is not None else []
        self._path.append(name)
        
        self._load_from(config_dict)

    def _load_from(self, config_dict):
        cached = copy.deepcopy(config_dict)
        self._cached = cached
        for key, val in cached.items():
            setattr(self, key, val)

    def save(self, filepath=None):
        if filepath is None:
            filepath = USER_FILE
        else:
            filepath = os.path.abspath(filepath)

        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    user_data = json.load(f) or {}
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid user config file: {filepath}\n"
                    "The specified file exists but is not readable as an "
                    "existing config file.") from e
            
        local_data = self.to_dict()

        root_key = "values"
        user_data = {root_key: user_data}
        current_level = user_data

        for key in self._path[:-1]:
            current_level = current_level.setdefault(key, {})

        current_level[self._path[-1]] = local_data
        user_data = user_data[root_key]

        defaults = _load_defaults()

        self._cached = copy.deepcopy(user_data)

        extracted = _extract_user(defaults, user_data) or {}

        with open(filepath, 'w') as f:
            json.dump(extracted, f, indent=4)      

    def revert(self):
        for key in list(self.__all__):
            if hasattr(self, key):
                delattr(self, key)
        self.__all__.clear()
        self._load_from(self._cached)

    def __getattr__(self, key):
        # only falls back to this method if the attribute doesn't already exist

        if key.startswith("_"):
            raise ValueError(f"Config attribute '{key}' does not exist, and you cannot create a nested config module with a name that starts with an underscore.")

        # Auto-create nested modules
        mod = NestedConfig({}, key, parent_name=self.__name__, path=self._path)
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
                val = NestedConfig(val, key, parent_name=self.__name__, path=self._path)

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
        if "." in key:
            parent, children = key.split(".", 1)
            return getattr(self, parent).get(children, default)
        val = getattr(self, key)
        if isinstance(val, NestedConfig):
            if val() == {}:
                return default
            return val()
        return val
    
    def update(self, key, value):
        if "." in key:
            parent, children = key.split(".", 1)
            return getattr(self, parent).update(children, value)
        setattr(self, key, value)
    
    def __call__(self):
        return self.to_dict()
    
values = None
    
_restart_session()

sys.modules[values.__name__] = values

__all__ = ["values"]

enforce_config()
