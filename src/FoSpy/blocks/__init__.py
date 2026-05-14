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
        validators = required_keys.get(self.__class__,{}) | optional_keys.get(self.__class__,{})

        self.sourceDict = {}
        self.extras = {}

        for key, val in blockDict.items():
            if key in validators:
                validator = validators[key]
                if isinstance(validator, type) and issubclass(validator, SingleBlock):
                    if type(val) == list:
                        if len(val) > 1:
                            raise ValueError(f"Block '{key}' must be a single block. It can only be constructed from a list of length 1.")
                        val = val[0]
                self.sourceDict[key] = validator(val)
                setattr(self, key, validator(val))

            else:
                self.sourceDict[key] = val
                self.extras[key] = val


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

        self.items = []
        for blockDict in blockList:
            self.items.append(cls.from_blockList(blockDict))

    def __getitem__(self, idx):
        return self.items[idx]
    
    def __len__(self):
        return len(self.items)
    
    def __iter__(self):
        return iter(self.items)
    
    
from .data import *
from .materials import *
from .metadata import *
from .treatments import *