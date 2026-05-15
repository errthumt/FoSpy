

from ..parsing.syntax import meta_keys as mk
from ..parsing.syntax import meta_defaults as md

from pprint import pp

from .._debug import Debug
_debug = Debug()
_debug.on = True

class SubContainer:
    def __init__(self):
        pass
    def __iter__(self):
        return iter(self.__dict__)


class SingleBlock:
    """
    A single key–value block parsed from a FOS file.

    Parameters
    ----------
    blockDict : dict
        Mapping of field names to scalar values. Subclasses perform
        validation and type conversion.
    """
    @classmethod
    def from_blockList(cls, blockDict):
        """
        Optional dispatcher to allow subclass delegation when constructing
        from ListBlock. Overridden in some subclasses
        """
        # Default: construct normally.
        return cls(blockDict)
    
    @classmethod
    def build_req_validators(cls):
        from ..parsing.validation import required_keys
        merged = {}
        for base in reversed(cls.__mro__):
            merged.update(required_keys.get(base,{}))
        return merged

    @classmethod
    def build_validators(cls):
        from ..parsing.validation import required_keys, optional_keys
        merged = {}
        for base in reversed(cls.__mro__):
            req = required_keys.get(base, {})
            opt = optional_keys.get(base, {})
            merged.update(req)
            merged.update(opt)
        return merged


    def __init__(self, blockDict):
        from ..parsing.validation import required_keys, optional_keys

        blockDict = blockDict.copy()

        req = self.build_req_validators()
        for key in req:
            if key not in blockDict:
                raise ValueError(f"Missing required property: '{key}' for '{type(self).__name__}' object.")
        
        self._meta = SubContainer()

        for attr, key in mk.items():
            setattr(self._meta, attr, blockDict.pop(key,md[key]))

        self._key_order = []
        self.ext = SubContainer()

        for key, val in blockDict.items():
            self._key_order.append(key)
            setattr(self, key, val)

        

    def __setattr__(self, name, value):
        validators = self.build_validators()
        if name == 'ext' or name.startswith("_"):
            return super().__setattr__(name, value)

        if name in validators:
            validator = validators[name]
            if isinstance(validator, type):
                if issubclass(validator, SingleBlock):
                    if isinstance(value, list):
                        if len(value) > 1:
                            raise ValueError(f"Block '{name}' must be a single block. It can only be constructed from a list of length 1.")
                        value = value[0]
                if isinstance(value, validator):
                    return super().__setattr__(name, value)
            return super().__setattr__(name, validator(value))
        else:
            return setattr(self.ext, name, value)

    def __getattr__(self, name):
        try:
            return getattr(self.ext, name)
        except AttributeError:
            raise AttributeError(
                f"{type(self).__name__} '{self.name if self.name else '<name unknown>'}'"
                f"has no attribute '{name!r}'."
            )
        
    def serialize(self):
        all_attrs = {}
        out = {}

        def try_serial(obj):
            serialize = getattr(obj, "serialize", None)
            if callable(serialize):
                return obj.serialize()
            return str(obj)

        for attr,val in self.__dict__.items():
            if attr == "ext" and val is not None:
                for ext_attr, ext_val in val.__dict__.items():
                    all_attrs[ext_attr] = ext_val
            elif not attr.startswith("_"):
                all_attrs[attr] = val

        
        for key in self._key_order:
            if key in all_attrs:
                val = all_attrs.pop(key)
                out[key] = try_serial(val)
        
        for key, val in all_attrs.items():
            out[key] = try_serial(val)

        for attr, key in mk.items():
            val = getattr(self._meta,attr,md[key])
            out[key] = val

        return [out]





class ListBlock:
    """
    A repeated‑entry block parsed from a FOS file.

    `blockList` contains a list of dictionaries, each of which must be
    processed into objects of the same class. ListBlock subclasses specify
    which Class is used.

    Parameters
    ----------
    blockDict : dict
        List of dictionaries mapping field names to values.
    cls : type
        Class used to construct each item. Validation is delegated to `cls`.
    """
    def __init__(self, blockList, cls):
        self._objs = []
        self._reqCls = cls
        for blockDict in blockList:
            self._objs.append(cls.from_blockList(blockDict))

    def __setattr__(self, name, value):
        if name == "_objs":
            if type(value) is not list:
                raise TypeError(f"{type(self).__name__}._objs must be a list of objects.")

            elif hasattr(self, "_reqCls"):
                typ = self._reqCls
                for obj in value:
                    if not isinstance(obj, typ):
                        raise TypeError(f"{type(self).__name__}._objs must be an empty list or list of {typ.__name__} objects.")
            return super().__setattr__(name, value)

        elif name.startswith("_"):
            return super().__setattr__(name,value)
        else:
            raise AttributeError(
                f"{type(self).__name__} does not allow setting attribute '{name}'. "
                f"Only private names starting with '_' can be used. "
                f"Each list item is an item in {type(self).__name__}._objs which can be edited individually, "
                f"Or you can replace {type(self).__name__}._objs with a new list of objects."
            )
        
        
        

    def __getitem__(self, idx):
        return self._objs[idx]
    
    def __len__(self):
        return len(self._objs)
    
    def __iter__(self):
        return iter(self._objs)
        
    def serialize(self):
        return [obj.serialize()[0] for obj in self]
    

    
from .synthesis import *   
from .data import *
from .materials import *
from .metadata import *
from .treatments import *