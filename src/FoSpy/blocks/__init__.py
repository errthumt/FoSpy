

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

    def __init__(self, blockDict):
        from ..parsing.validation import required_keys, optional_keys
        from ..parsing.syntax import meta_keys as mk
        blockDict = blockDict.copy()
        
        self._meta = SubContainer()

        for attr, key in mk.items():
            setattr(self._meta, attr, blockDict.pop(key,None))

        validators = required_keys.get(self.__class__,{}) | optional_keys.get(self.__class__,{})

        self._key_order = []
        self.ext = SubContainer()

        for key, val in blockDict.items():
            self._key_order.append(key)
            if key in validators:
                validator = validators[key]
                if isinstance(validator, type) and issubclass(validator, SingleBlock):
                    if type(val) == list:
                        if len(val) > 1:
                            raise ValueError(f"Block '{key}' must be a single block. It can only be constructed from a list of length 1.")
                        val = val[0]
                setattr(self, key, validator(val))

            else:
                setattr(self.ext, key, val)

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
            return obj


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

        self.objs = []
        for blockDict in blockList:
            self.objs.append(cls.from_blockList(blockDict))

    def __getitem__(self, idx):
        return self.objs[idx]
    
    def __len__(self):
        return len(self.objs)
    
    def __iter__(self):
        return iter(self.objs)
        
    def serialize(self):
        return [obj.serialize()[0] for obj in self]
    

    
from .synthesis import *   
from .data import *
from .materials import *
from .metadata import *
from .treatments import *