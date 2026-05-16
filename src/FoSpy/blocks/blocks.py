from .. import inherit_docstring
from ..parsing.syntax import meta_keys as mk
from ..parsing.syntax import meta_defaults as md


from ..parsing import (
    dict_from_file,
    write_dict_to_file
)


from .._debug import Debug
_debug = Debug()
_debug.on = True

class SubContainer:
    """
    A simple container for storing hidden or unexpected attributes of a
    `SingleBlock`
    
    Values are only assigned directly to `SingleBlock` attributes if they are an
    expected property. Otherwise they are assigned to a `SubContainer` at
    `SingleBlock.ext`. Also assigned to `SingleBlock._meta`.

    Example Usage: ```
    class SingleBlock:
        ... 
        def __setattr__(self, name, value):
            ... 
            if name not in expected:
                return setattr(self.ext, name, value)
    ```
    """
    def __init__(self):
        pass
    def __iter__(self):
        return iter(self.__dict__)
    
def calc_routine(func):
    """
    Decorator for `SingleBlock` or `ListBlock` methods that calculate values
    from existing attributes.

    `calc_routine` functions can be called at any time, but can also be queued
    to run at serialization, as in refreshing relevant calculated values before
    saving the file. See `SingleBlock.add_calc_routine()`
    """
    func._is_calc_routine = True
    return func

class SingleBlock:
    """
    Represents a single block of key:value pairs parsed from a FOS file.

    Subclasses are mapped to expected keys and validation routines in
    `FoSpy.parsing.validation`. Expected values are validated and assigned to
    attributes. Unexpected values are assigned to attributes of `self.ext`.

    Some notable subclasses:```
        FileBlock(SingleBlock)
        Synthesis(FileBlock)
        Reaction(SingleBlock)
        Material(SingleBlock)
        TemplateBlock(SingleBlock)
        MaterialTempBlock(Material, TemplateBlock)
    ```
    """
    @classmethod
    def subclass(cls, blockDict):
        """
        Recommended dispatcher to allow subclass delegation when constructing.
        
        Overridden in some subclasses
        """
        # Default: construct normally.
        return cls(blockDict)
    
    @classmethod
    def build_req_validators(cls):
        """
        Builds required keys and validators mapped to subclass.

        Walks all parent classes and builds a map of all keys that are required
        during `__init__`, and their respective validation routines. Subclasses
        are mapped to expected keys and validations in
        `FoSpy.parsing.validation`. Subclass validations override parent classes
        when applicable.

        Returns:
            a dict mapping required keys to validation routines. Routines may be
            a class constructor or a func taking one arg. Example:``` {
                "name": str,
                "type": str,
                "formula": ChemFormula, # class constructor
                "supplier": str,
                "cas": str,
                "form": str,
                "env": str,
                "ratio": validators.material.ratio # validator function
            }
            ```
        """
        from ..parsing.validation import required_keys
        merged = {}
        for base in reversed(cls.__mro__):
            merged.update(required_keys.get(base,{}))
        return merged

    @classmethod
    def build_validators(cls):
        """
        Builds expected keys and validators mapped to subclass.

        Walks all parent classes and builds a map of all keys that are allowed
        (required or optional), and their respective validation routines.
        Subclasses are mapped to keys and validations in
        `FoSpy.parsing.validation`. Subclass validations override parent classes
        when applicable. See `SingleBlock.build_req_validators()`
        """
        from ..parsing.validation import required_keys, optional_keys
        merged = {}
        for base in reversed(cls.__mro__):
            req = required_keys.get(base, {})
            opt = optional_keys.get(base, {})
            merged.update(req)
            merged.update(opt)
        return merged


    def __init__(self, blockDict:dict):
        """Constructs a SingleBlock object from a dictionary

        SingleBlocks are constructed recursively from an arbitrarily nested
        dictionary. All keys identified by `SingleBlock.build_req_validators()`
        must be present at the top level. Required keys at nested levels are
        handled by the recursed constructor.

        Args:
            blockDict:
                An arbitrarily nested dictionary mapping attribute names to
                values. 

                Unexpected attributes will be assigned under `self.ext` instead
                (see `SingleBlock.__setattr__`). 
                
                It is possible to pass a blockDict already containing objects,
                but validation routines will fail if objects are not the correct
                type. Best practice is to serialize all nested objects into
                lists, dicts, and strings to allow full type coersion.

        Raises:
            ValueError:
                A key required by `SingleBlock.build_req_validators()` is not
                present.

        """
        from ..parsing.validation import required_keys, optional_keys

        blockDict = blockDict.copy()

        req = self.build_req_validators()
        req.pop("ext",None)
        for key in req:
            if key not in blockDict:
                raise ValueError(f"Missing required property: '{key}' for '{type(self).__name__}' object.")
        
        self._meta = SubContainer()
        self._calc_comments = {}
        self._calc_routines = []

        for attr, key in mk.items():
            setattr(self._meta, attr, blockDict.pop(key,md[key]))

        self._key_order = []
        self.ext = SubContainer()

        for key, val in blockDict.items():
            self._key_order.append(key)
            setattr(self, key, val)

        
    @inherit_docstring(object)
    def __setattr__(self, name, value):
        """
        Assign an attribute with validation and controlled namespace behavior.

        Contract:
            `SingleBlock` enforces type correctness and validator execution for
            all public attributes defined by its subclass.

            Required types and validators are mapped by subclass in
            `FoSpy.parsing.validation`

        Rules:
            1. Private attributes (`_`-prefixed) bypass validation.
            2. Attributes with registered validators are processed through the
            validator before assignment.
            3. Attributes with required types are coerced by calling the type
            constructor when necessary.
                3a. If required type is a SingleBlock subclass and value is
                wrapped as a list, list is unwrapped to the first entry
            4. Unrecognized attribute names are redirected to `self.ext`.

        Raises:
            ValueError:
                Required `SingleBlock`s can be coerced from a dict or a list with
                a single dict entry. Error raised if a list of length > 1 is
                passed for a `SingleBlock` attribute.
        """

        validators = self.build_validators()
        if name.startswith("_"):
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
        """
        Check both self and self.ext for attribute before returning.
        """
        try:
            return getattr(self.ext, name)
        except AttributeError:
            raise AttributeError(
                f"{type(self).__name__} object: '{self.name if hasattr(self, "name") else '<name unknown>'}' "
                f"has no attribute {name!r}."
            )
        
    def serialize(self):
        from copy import deepcopy
        from ..parsing.format import format_calc_comment

        all_attrs = {}
        out = {}

        for routine in self._calc_routines:
            routine()

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
                out[key] = try_serial(val) if key != "embedded" else val
        
        for key, val in all_attrs.items():
            out[key] = try_serial(val) if key != "embedded" else val

        for attr, key in mk.items():
            val = getattr(self._meta,attr,md[key])
            out[key] = val

        out = deepcopy(out)

        # _debug.pmsg(self._calc_comments)
        for key, comments in self._calc_comments.items():
            for comment in comments.values():
                out[mk["comments"]][key].append(format_calc_comment(comment))
        
        return [out]
    
    def add_calc_comment(self, key, comment, calc_id):
        calc_comments = self._calc_comments.get(key, {})
        self._calc_comments[key] = calc_comments
        self._calc_comments[key][calc_id]=comment



    def _resolve_relative_path(self, path: str):
        import re

        _index_re = re.compile(r"^([A-Za-z_]\w*)\[(\d+)\]$")
        obj = self

        for part in path.split("."):

            # Case: attr[index]
            m = _index_re.match(part)
            if m:
                attr_name, idx_str = m.groups()
                idx = int(idx_str)

                # Get the ListBlock
                obj = getattr(obj, attr_name)

                # Index into its _objs
                obj = obj._objs[idx]
                continue

            # Case: simple attribute
            obj = getattr(obj, part)

        return obj
    
    def add_calc_routine(self, path, **kwargs):
        func = self._resolve_relative_path(path)
        if not getattr(func, "_is_calc_routine", False):
            raise TypeError(f"'{path}' is not a registered calc routine.")

        def wrapped():
            return func(**kwargs)

        self._calc_routines.append(wrapped)

    def list_calc_routines(self, recursive=False, prefix="", abbreviated=False):
        routines = []

        # Local routines
        for name in dir(self):
            attr = getattr(self, name)
            if callable(attr) and getattr(attr, "_is_calc_routine", False):
                routines.append(prefix + name)

        if recursive:
            for attr, val in self.__dict__.items():
                if attr.startswith("_"):
                    continue

                # Recurse into child blocks
                if hasattr(val, "list_calc_routines"):
                    child_prefix = f"{prefix}{attr}."
                    routines.extend(val.list_calc_routines(True, child_prefix, abbreviated))

        return routines
    
    def add_all_calc_routines(self, recursive=False):
        for path in self.list_calc_routines(recursive=recursive, abbreviated=False):
            self.add_calc_routine(path)

    def copy(self):
        cls = type(self)
        return cls.subclass(self.serialize())





class FileBlock(SingleBlock):
    def __init__(self, blockDict, _sourceFile=None):
        self._sourceFile = _sourceFile
        super().__init__(blockDict)

    @classmethod
    def fromFile(cls, filepath):
        blockDict = dict_from_file(filepath)
        return cls(blockDict, _sourceFile = filepath)
    
    def serialize(self):
        return super().serialize()[0]
    
    def save(self, filepath=None):
        if filepath is None:
            if self._sourceFile is None:
                raise ValueError("Synthesis object was constructed without a sourceFile. A save destination must be specified.")
            else:
                filepath = self._sourceFile
        
        self._sourceFile = filepath
        blockDict = self.serialize()

        write_dict_to_file(blockDict, filepath)


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
            self._objs.append(cls.subclass(blockDict))

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
    def append(self, obj):
        objs = self._objs.copy()
        objs.append(obj)
        self._objs = objs
        
        
        

    def __getitem__(self, idx):
        return self._objs[idx]
    
    def __len__(self):
        return len(self._objs)
    
    def __iter__(self):
        return iter(self._objs)
        
    def serialize(self):
        return [obj.serialize()[0] for obj in self]
    
    def list_calc_routines(self, recursive=False, prefix="", abbreviated=False):
        routines = []

        # Local routines on the ListBlock itself
        for name in dir(self):
            attr = getattr(self, name)
            if callable(attr) and getattr(attr, "_is_calc_routine", False):
                routines.append(prefix + name)

        if recursive:
            if abbreviated:
                obj_routines = {}
                idx_str = "i"
                idx_num = 0
                while f"[{idx_str}{idx_num if idx_num > 0 else ''}]" in prefix:
                    if idx_str == "z":
                        idx_str = "i"
                        idx_num += 1
                    else:
                        idx_str = chr(ord(idx_str)+1)

                idx_str = f"{idx_str}{idx_num if idx_num > 0 else ''}"

                for i, obj in enumerate(self._objs):
                    if hasattr(obj, "list_calc_routines"):
                        rtns = obj.list_calc_routines(True,f"{prefix[:-1]}[{idx_str}].",abbreviated=True)
                        for routine in rtns:
                            if routine not in obj_routines:
                                obj_routines[routine] = []
                            obj_routines[routine].append(i)
                for routine, i_list in obj_routines.items():
                    routines.append(f"{routine}; {idx_str} = {i_list}")
            else:
                for i, obj in enumerate(self._objs):
                    if hasattr(obj, "list_calc_routines"):
                        child_prefix = f"{prefix[:-1]}[{i}]."
                        routines.extend(obj.list_calc_routines(
                            recursive=True,
                            prefix=child_prefix,
                            abbreviated=False
                        ))

        return routines
    
    def copy(self):
        cls = type(self)
        return cls(self.serialize())
    
    def remove_any(self, **kwargs):
        if len(kwargs) != 1:
            raise TypeError("Exactly one keyword argument is required")
        
        key, val = next(iter(kwargs.items()))
        
        objs = self._objs.copy()
        removed = 0
        for obj in objs:
            if getattr(obj, key, None) == val:
                self._objs.remove(obj)
                removed += 1
        _debug.msg(f"Removed {removed} {self._reqCls.__name__} objects matching {key} = {val}.")
