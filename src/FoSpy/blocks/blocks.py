import os

from .. import inherit_docstring, inherit_class_doc, attach_doc
from ..parsing.syntax import (
    meta_keys as mk,
    meta_defaults as md,
)

from ..parsing import (
    dict_from_file,
    write_dict_to_file
)

import tempfile
import atexit
from pathlib import Path


from .._debug import Debug
_debug = Debug()

def unwrap_block(struct):
    while isinstance(struct,list) and len(struct) == 1:
        struct = struct[0]

    if isinstance(struct,SingleBlock):
        struct = struct.serialize(keepListType=True)
        struct = unwrap_block(struct)
    return struct

class SimpleWrapper:
    def __init__(self, value):
        self._value = value

    def __iter__(self):
        return self._value.__iter__()
    
    def __str__(self):
        return str(self._value)

    def __repr__(self):
        return repr(self._value)

    def __eq__(self, other):
        return self._value == other
    
    def __call__(self):
        return self._value

    def __getattr__(self, name):
        return getattr(self._value, name)

class Block:
    def find_fileblock(self):
        blk = self
        while blk is not None:
            if isinstance(blk, FileBlock):
                return blk
            if hasattr(blk,"_parent_block"):
                blk = blk._parent_block
            else:
                blk = None
        raise LookupError("Could not find a FileBlock containing the current object")
    
    def find_tempdir(self):
        fileblock = self.find_fileblock()
        if hasattr(fileblock, "_tempdir"):
            return fileblock._tempdir
        else:
            raise AttributeError("Could not find a temporary directory attached to this object's FileBlock")
    
    def find_temppath(self):
        fileblock = self.find_fileblock()
        if hasattr(fileblock, "_temppath"):
            return fileblock._temppath
        if hasattr(fileblock, "_temppdir"):
            raise AttributeError("This object's FileBlock has a temporary directory but no path mapped to it. "
                                 "Use obj.find_tempdir() instead")
        raise AttributeError("Could not find a temporary directory object or path "
                             "attached to this object's FileBlock.")

    def _subprocess(self, target, args=(), **kwargs):
        from multiprocessing import Process

        if kwargs is None:
            kwargs={}

        p = Process(target=target, args=args, kwargs=kwargs)
        p.start()
        

class SubContainer:
    """
    A simple container for storing hidden or unexpected attributes of a
    `SingleBlock`
    
    Values are only assigned directly to `SingleBlock` attributes if they are an
    expected property. Otherwise they are assigned to a `SubContainer` at
    `SingleBlock.ext`. Also assigned to `SingleBlock._meta`.

    Example Usage:
    ```
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
    
def calc_routine(attach=True):
    """
    Decorator for `SingleBlock` or `ListBlock` methods that calculate values
    from existing attributes.

    `calc_routine` functions can be called at any time, but can also be queued
    to run at serialization, as in refreshing relevant calculated values before
    saving the file. See `SingleBlock.add_calc_routine()`
    """
    def decorator(func):
        func._is_calc_routine = True
        func.__doc__ = (func.__doc__ or "") + "\nThis function is decorated as a calc_routine"
        if attach:
            func = attach_doc(SingleBlock.add_calc_routine, label="Related")(func)
        return func
    return decorator
    

class SingleBlock(Block):
    """
    Represents a single block of key:value pairs parsed from a FOS file.

    Subclasses are mapped to expected keys and validation routines in
    `FoSpy.parsing.validation`. Expected values are validated and assigned to
    public attributes. Unexpected values are assigned to attributes of
    `self.ext` for safety, but can still be accessed as an attribute of the
    SingleBlock obj if not overridden.

    Some notable subclasses:
    ```
        FileBlock(SingleBlock)
        Synthesis(FileBlock)
        Reaction(SingleBlock)
        Material(SingleBlock)
        TemplateBlock(SingleBlock)
        MaterialTempBlock(Material, TemplateBlock)
    ```
    Private Attributes:
        _meta:
            `SubContainer` object containing meta data extracted from `blockDict`
            during construction. See `FoSpy.parsing.syntax.meta_keys`

        _calc_comments:
            dict mapping attribute names to `{"comment_ID":"comment_text"}`
            values. Calculated comments are for user information when reading a
            FOS file. On serialization, they are formatted to be skipped by the
            parser and attached to their respective attributes. See
            `SingleBlock.add_calc_comment()` and
            `SingleBlock.add_calc_routine()`.

        _calc_routines:
            List of `calc_routine()`-decorated methods to be run during
            serialization to populate _calc_comments.

        _key_order: 
            Maintains order that attributes were read during construction to be
            repeated during serialization
    """
    dispatch = {}
    _aliases = None
    @classmethod
    def subclass(cls, blockDict:dict):
        """
        Recommended dispatcher to allow subclass delegation when constructing.
        
        Overridden in some subclasses
        """
        # k: construct normally.
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
            a class constructor or a func taking one arg. Example:
            ``` 
            {
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
            base_reqs = required_keys.get(base,{})
            for key, validator in base_reqs.items():
                # allow subclasses to remove parent requirements.
                if validator is False:
                    merged.pop(key, None)
                else:
                    merged[key] = validator
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
            for key_set in (required_keys, optional_keys):
                base_reqs = key_set.get(base,{})
                for key, validator in base_reqs.items():
                    # allow subclasses to remove parent requirements.
                    if validator is False:
                        merged.pop(key, None)
                    else:
                        merged[key] = validator

        return merged
    
    @classmethod
    def TemplateClass(cls,*args:str):
        from .template import TemplateBlock, TemplateField, TemplateList
        from ..parsing.validation import required_keys, optional_keys
        class SubTemplate(TemplateBlock, cls):
            dispatch = {}
            def __init__(self, blockDict):
                super().__init__(blockDict)
                self._full_class = cls

        required_keys[SubTemplate] = {}
        optional_keys[SubTemplate] = {}
        required_validators = cls.build_req_validators()
        all_validators = cls.build_validators()
        for key in args:
            req_val = required_validators.get(key,None)
            val = all_validators.get(key,None) or req_val

            if isinstance(val,type) and issubclass(val,SingleBlock):
                all_fields = list(val.build_req_validators().keys())
                field = val.TemplateClass(*all_fields)

            elif isinstance(val,type) and issubclass(val, ListBlock):
                field = TemplateList.Simple(val._reqCls)
            else:
                field = TemplateField

            if req_val:
                required_keys[SubTemplate][key] = field
            else:
                optional_keys[SubTemplate][key] = field

        finished_reqs = required_keys[SubTemplate]
        finished_opts = optional_keys[SubTemplate]
        for typ, sub in cls.dispatch.items():
            dispatched_sub = sub.TemplateClass(*args)
            SubTemplate.dispatch[typ] = dispatched_sub

            required_keys[dispatched_sub] = finished_reqs
            optional_keys[dispatched_sub] = finished_opts

        SubTemplate.__name__ = f"{cls.__name__}Template"
        SubTemplate.__qualname__ = f"{cls.__name__}.Template"
        SubTemplate.__module__ = cls.__module__

        return SubTemplate
    
    def make_template(self,template_name,*args:str):
        from ..parsing import format_field

        serial = self.serialize(keepListType=True)
        validators = self._rename_validators()
        for key in args:
            val = validators.get(key, None)
            if isinstance(val,type) and (issubclass(val, SingleBlock) or issubclass(val, ListBlock)):
                serial[key] = []
            else:
                serial[key] = format_field("template")
        serial["template_name"] = template_name
        return type(self).TemplateClass(*args)(serial)

    @classmethod
    def Template_from_dict(cls, blockDict):
        from ..parsing.format import format_field
        template_keys = []
        blockDict = unwrap_block(blockDict)
        temp_dict = blockDict.copy()
        for key in cls.build_req_validators():
            if key != 'ext' and key not in temp_dict:
                template_keys.append(key)
        for key, val in blockDict.items():
            if val == format_field("template"):
                if key not in template_keys:
                    template_keys.append(key)
                temp_dict.pop(key, None)
        pass
        return cls.TemplateClass(*template_keys)
        
    @classmethod
    def reflex(cls, **kwargs):
        from .template import FlexTemplate
        class Flex(FlexTemplate, cls):
            _baseReq = cls
        
        kwargs.setdefault("template_name", f"Empty {cls.__name__}")

        empty = Flex.subclass(kwargs)
        return empty.serialize()

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

        from ..parsing.validation import aliases as als
        new_als = als.copy()
        new_als.update(self._aliases or {})
        self._aliases = new_als
        self._reserved = ['ext']

        from copy import deepcopy
        blockDict = unwrap_block(blockDict)
        self._sourceDict = blockDict.copy()

        if not isinstance(blockDict, dict):
            raise TypeError("A SingleBlock must be constructed from either a dictionary or another SingleBlock. "
                            "The passed source can optionally be wrapped in lists of length == 1.")

        blockDict = blockDict.copy()

        rename = blockDict.pop("rename",None)
        if rename:
            setattr(self, "rename", unwrap_block(rename))

        req = self._rename_validators(required=True)
        req.pop("ext",None)
        for key, validator in req.items():
            if key not in blockDict:
                from .template import TemplateBlock, TemplateList, TemplateField, FlexTemplate
                if issubclass(validator, TemplateField):
                    blockDict[key] = ""
                elif issubclass(validator, FlexTemplate):
                    blockDict[key] = {"template_name": f"Empty {self._baseReq.__name__} Template"}
                elif issubclass(validator, TemplateBlock):
                    blockDict[key] = validator.reflex()
                elif issubclass(validator, TemplateList):
                    blockDict[key] = []
                else:
                    raise ValueError(f"Missing required property: '{key}' for '{type(self).__name__}' object.")
        
        self._meta = SubContainer()
        self._calc_comments = {}
        self._calc_routines = []
        self._key_overrides = {}

        for attr, key in mk.items():
            try:
                k = md[key].copy()
            except:
                k = md[key]
            setattr(self._meta, attr, blockDict.pop(key,k))

        self._key_order = []
        self.ext = SubContainer()

        for key, val in blockDict.items():
            self._key_order.append(key)
            setattr(self, key, val)
    
    def _rename_validators(self, required=False):
        validators = self.build_req_validators() if required else self.build_validators()
        if hasattr(self, "rename"):
            for name, rename in self.rename.items():
                if name in validators and rename not in validators:
                    val = validators.pop(name)
                    validators[rename] = val
        return validators

    def _assign_and_inject_comments(self, name, value, extended=False):
        if name == 'ext':
            return super().__setattr__('ext', value)
        if not hasattr(value, "__dict__"):
            value = SimpleWrapper(value)

        if extended:
            setattr(self.ext, name, value)
        else:
            super().__setattr__(name, value)
        
        attr_obj = getattr(self.ext if extended else self, name)

        setattr(attr_obj, "_parent_block", self)

        def _make_bound(attr_name):
            def add_comments_to_parent(self_attr, *comments):
                parent_comments = self_attr._parent_block._meta.comments
                parent_comments.setdefault(attr_name,[])
                for comment in comments:
                    parent_comments[attr_name].append(str(comment))
            
            def clear_comments_from_parent(self_attr):
                parent_comments = self_attr._parent_block._meta.comments
                parent_comments[attr_name] = []

            return (add_comments_to_parent, "add_comments"), (clear_comments_from_parent, "clear_comments")
        attr_obj._reserved = ['ext'] if not hasattr(attr_obj,"_reserved") else attr_obj._reserved
        for method, mthd_name in _make_bound(name):
            attr_obj._reserved.append(mthd_name)
            bound = method.__get__(attr_obj, type(attr_obj))
            setattr(attr_obj, mthd_name, bound)
        
    @inherit_docstring(object)
    def __setattr__(self, name:str, value):
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
        from ..parsing.format import format_field
        from .template import TemplateField, TemplateBlock

        from inspect import signature as sign

        if name.startswith("_") or name in self._reserved:
            return super().__setattr__(name, value)
        
        validators = self._rename_validators()
        
        if "$" in name:
            try:
                name, alias = name.split("$")
            except:
                raise ValueError(f"Unable to parse a block alias from key: '{name}'.")
            
            try:
                val = self._aliases[alias]
            except KeyError:
                raise ValueError(f"Unrecognized block alias: '{alias}'")
            
            if name in validators and val != validators[name]:
                raise ValueError(f"Key: '{name}' is already reserved for '{validators[name].__name__}' validator, "
                                 f"it cannot be overwritten to '{val.__name__}'.")
            if name not in validators:
                from ..parsing.validation import optional_keys
                validators[name] = val
                self._key_overrides[name] = val
                optional_keys.setdefault(type(self),{})
                optional_keys[type(self)][name] = val

        if name in validators:
            validator = validators[name]
            val_kwargs = {}
            for kw, arg in (("sourceDict", self._sourceDict),("cls", type(self))):
                try:
                    if kw in sign(validator).parameters:
                        val_kwargs[kw] = arg
                except:
                    pass
                

            if isinstance(validator, type):
                if issubclass(validator, SingleBlock):
                    if isinstance(value, list):
                        if len(value) > 1:
                            raise ValueError(f"Block '{name}' must be a single block. It can only be constructed from a list of length 1.")
                        value = value[0]
                    elif isinstance(value,SingleBlock):
                        value = value.serialize(keepListType=True)

                elif issubclass(validator, ListBlock):
                    try: 
                        value = [block.serialize(keepListType=True) for block in value]
                    except Exception as e:
                        if isinstance(value, ListBlock):
                            value = value.serialize()
                elif value == format_field("template") and not issubclass(validator, TemplateField):
                    if isinstance(self,TemplateBlock):
                        validator = TemplateField
                    else:       
                        raise ValueError(f"You cannot create a '{type(self).__name__}' object with an un-filled '{name}' template field.")
                if isinstance(value, validator):
                    return self._assign_and_inject_comments(name, value)




            return self._assign_and_inject_comments(name,
                                                    validator(value,**val_kwargs)
                                                    if val_kwargs != {}
                                                    else validator(value))
        else:
            return self._assign_and_inject_comments(name, value, extended=True)
    
    def add_comments(self, *comments):
        """
        Default Behavior. If a `SingleBlock` is stored in another `SingleBlock`,
        this method will be overwritten by the parent's `__setattr__`
        """
        keys = list(self._rename_validators(required=True).keys())

        keys = [k for k in keys if k != "metadata"]
        fallback = [k for k in self._key_order if k != "metadata"]
        if not (keys or fallback):
            raise ValueError("This object has not been correctly attached to a parent block "
                             "and could not identify a required key to attach to.")

        first = keys[0] if keys else fallback[0]

        self._meta.comments.setdefault(first, [])
        for comment in comments:
            self._meta.comments[first].append(comment)

    def __getattr__(self, name:str):
        """
        Check both self and self.ext for attribute before returning.
        """
        try:
            if name != 'ext':
                return getattr(self.ext, name)
            raise AttributeError()
        except AttributeError:
            raise AttributeError(
                f"{type(self).__name__} object "
                f"has no attribute {name!r}."
            )
    
    def add_block(self, block_name, type_alias, value=[]):
        if hasattr(self,block_name):
            raise ValueError(f"This object already has attribute: '{block_name}'.")
        return setattr(self, f"{block_name}${type_alias}", value)

    def __eq__(self, other, suppress_routine_paths=False):
        from .._debug import deep_diff as dd, _debug as db
        try:
            db.msg("Serializing Blocks to check equality:", module = "SingleBlock.__eq__()")
            diffs = dd(self.serialize(), other.serialize(), suppress_routine_paths=suppress_routine_paths)
            passed = len(diffs) == 0
            if not passed:
                db.pmsg(diffs,module = "SingleBlock.__eq__()")
            return passed
        except Exception as e:
            db.msg(f"Equality failed by exception: {e}",module = "SingleBlock.__eq__()")
            return False
        
    def __hash__(self):
        return id(self)
        
    def serialize(self, keepListType=False, shallow=False):
        """
        Return a recursively serialized `[dict]` representation of itself.

        Fully serialized `SingleBlock`s are a single dict wrapped in a list that
        can be passed to another constructor or emitted into lines for a FOS
        file. Serialized values at any nest level are either dicts, lists, or
        strings to allow full type-coersion when reconstructing or simplified
        emission when writing files.

        Serialized dict is deep copied to prevent object mutation.

        Private attributes starting with "_" are either skipped or unpacked in
        special cases:
            _key_order:
                attributes are added to the serialized dict in the order
                they appear in this list.
            
            _calc_comments:
                calculated comments are attached to their mapped attribute after
                serialization to avoid mutation of object comments

            _meta:
                attributes of this container are given their own private `_key`s
                mapped by `FoSpy.parsing.syntax.meta_keys` in the serialized
                dict.
        """
        from copy import deepcopy
        from ..parsing.format import format_calc_comment

        val_to_alias = {v:k for k,v in self._aliases.items()}

        all_attrs = {}
        out = {}

        for routine in self._calc_routines:
            routine()

        def add_alias(key):
            if key in self._key_overrides:
                alias = val_to_alias[self._key_overrides[key]]
                return f"{key}${alias}"
            return key


        def try_serial(obj):
            serialize = getattr(obj, "serialize", None)
            if callable(serialize) and not shallow:
                return obj.serialize()
            return str(obj)

        for attr,val in self.__dict__.items():
            if attr == "ext" and val is not None:
                for ext_attr, ext_val in val.__dict__.items():
                    all_attrs[ext_attr] = ext_val
            elif not (attr.startswith("_") or attr in self._reserved):
                all_attrs[attr] = val

        
        for key in self._key_order:
            if key in all_attrs:
                val = all_attrs.pop(key)
                out[add_alias(key)] = try_serial(val)
        
        for key, val in all_attrs.items():
            out[add_alias(key)] = try_serial(val)

        for attr, key in mk.items():
            try:
                k = md[key].copy()
            except:
                k = md[key]
            val = getattr(self._meta,attr,k)
            out[key] = val

        out = deepcopy(out)

        # _debug.pmsg(self._calc_comments)
        for key, comments in self._calc_comments.items():
            for comment in comments.values():
                out[mk["comments"]].setdefault(add_alias(key),[])
                out[mk["comments"]][add_alias(key)].append(format_calc_comment(comment))
        
        if not keepListType:
            out[mk["list_type"]] = "explicit"

        return out
    
    def add_calc_comment(self, key:str, comment:str, calc_id:str):
        """
        Add a calculated comment to be injected during serialization.

        WARNING: This function can leave outdated calculations in comments after
        serialization. Recommended to use `add_calc_routine()` instead.
        
        Calculated comments are for user information and will be formatted to be
        skipped by the parser when reading the file. This is useful for comments
        that should be recalculated and refreshed during saving/serialization,
        like weight percentages or summaries.

        Args:
            key:
                attribute to attach the calculated comment to. Comments appear
                above their attached attributes in FOS files.
            comment:
                comment text without comment formatting (like // or !)
            calc_id:
                unique identifier for the calculated comment. If it matches an
                existing comment (like when refreshing a value), the comment is
                overwritten

        """
        calc_comments = self._calc_comments.get(key, {})
        self._calc_comments[key] = calc_comments
        self._calc_comments[key][calc_id]=comment



    def _resolve_relative_path(self, path: str):
        """
        Resolves a relative object path string into an object or function.

        Example:
        ```
            mySyn._resolve_relative_path("materials[1].ratio")
            ## returns mySyn.materials[1].ratio
        ```
        """
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
    
    def add_calc_routine(self, path:str, **kwargs):
        """
        Appends a `calc_routine()`-decorated function to `self._calc_routines`
        to be run at serialization.

        Used to add calculated comments that should be refreshed during
        serialization.

        Args:
            path:
                a relative path string that can be resolved into a
                `calc_routine()`-decorated function
            kwargs:
                optional key word arguments to be passed to the function at
                path.

        Raises:
            TypeError: the attr or method at path is not registered as a
            calc_routine

        Example:
        ```
            mySyn.add_calc_routine("materials.add_weight_pcts", typ="reagent")
            ## mySyn.materials.add_weight_pcts(typ="reagent") will be run before
            ## serialization.
        ```
        """
        from functools import wraps

        func = self._resolve_relative_path(path)
        if not getattr(func, "_is_calc_routine", False):
            raise TypeError(f"'{path}' is not a registered calc routine.")

        self._meta.routine_paths.append(path)

        @wraps(func)
        def wrapped():
            __name__ = func.__name__
            return func(**kwargs)

        self._calc_routines.append(wrapped)

    def list_avail_routines(self, recursive=False, prefix="", abbreviated=False):
        """
        Lists all calc routines available to be added to `self._calc_routines`.

        Non-abbreviated calc routine strings can be passed directly to
        `self.add_calc_routine()`

        Args:
            recursive:
                If True, recursively walks all attributes and appends results
                from `self.attr.list_avail_routines()` to result. Otherwise only
                identifies methods of `self`.

            prefix: Used during recursion to build relative paths
            abbreviated:
                optionally abbreviate recursively repeated routines for similar
                objects into one line. This line cannot be passed to
                `self.add_calc_routine()`

        Returns: list of strings

        Example:
        ```
            mySyn.list_avail_routines()
            ## returns []
            mySyn.list_avail_routines(recursive=True)
            ## returns [
            ##     'reaction.add_nom_MW',
            ##     'materials.add_weight_pcts',
            ##     'materials[0].add_MW',
            ##     'materials[1].add_MW',
            ##     ... 6 total materials with the same calc_routine
            ##     'materials[5].add_MW'
            ## ]
            mySyn.list_avail_routines(recursive=True, abbreviated=True)
            ## returns [
            ##     'reaction.add_nom_MW',
            ##     'materials.add_weight_pcts',
            ##     'materials[i].add_MW; i = [0, 1, 2, 3, 4, 5]'
            ## ]
        ```
        """
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
                if hasattr(val, "list_avail_routines"):
                    child_prefix = f"{prefix}{attr}."
                    routines.extend(val.list_avail_routines(True, child_prefix, abbreviated))

        return routines
    
    def add_all_calc_routines(self, recursive=False):
        """
        Adds all available calc_routines to `self._calc_routines` using
        `self.list_avail_routines()` and `self.add_calc_routine()`.
        
        Optional recursion. See `SingleBlock.list_avail_routines()`
        """
        for path in self.list_avail_routines(recursive=recursive, abbreviated=False):
            self.add_calc_routine(path)

    def copy(self):
        """
        Returns a deep-copy of itself by serializing and reconstructing.
        
        _calc_comments are not preserved during copy, but _calc_routines are.
        This prevents mutation of the comments when reconstructing.
        """
        cls = type(self)
        c_cmts = self._calc_comments.copy()
        self._calc_comments = {}

        new_obj =  cls.subclass(self.serialize(keepListType=True))
        self._calc_comments = c_cmts

        return new_obj
    
    def _meta_to_front(self):
        try:
            meta_idx =self._key_order.index("metadata")
            self._key_order.pop(meta_idx)
        except:
            pass
        self._key_order.insert(0,"metadata")
    
    def keys_to_front(self,*args):
        try:
            meta_idx = args.index("metadata")
            args.pop(meta_idx)
        except:
            pass
        
        new_order = []
        for key in args:
            new_order.append(key)
        for key in self._key_order:
            if key not in new_order:
                new_order.append(key)
        self._key_order = new_order
        self._meta_to_front()

    def default_key_order(self):
        new_order = []
        for key in self._rename_validators():
            if key != "ext" and key in self.serialize(shallow=True):
                new_order.append(key)
        for key in self._key_order:
            if key not in new_order:
                new_order.append(key)
        self._key_order = new_order
        self._meta_to_front()

    def keys_to_end(self, *args):
        for key in args:
            try:
                idx = self._key_order.index(key)
                self._key_order.pop(idx)
            except:
                pass
            self._key_order.append(key)
        self._meta_to_front()
        
    def key_to_idx(self, key, idx):
        self._meta_to_front()
        try:
            old_idx = self._key_order.index(key)
            self._key_order.pop(old_idx)
        except:
            pass
        self._key_order.insert(idx, key)

    def clear_comments(self):
        self._meta.comments = {}
        
    def rename_block(self, old, new):
        validators = self._rename_validators()
        req = self._rename_validators(required=True)
        alias = None
        if new not in validators:
            val = validators[old]
            val_to_alias = {v:k for k,v in self._aliases.items()}
            try:
                alias = val_to_alias[val]
            except KeyError:
                raise ValueError(f"Could not find alias for '{val.__name__}' for '{old}' property.")
            new_alias = f"{new}${alias}"
        if old in req:
            raise ValueError(f"You cannot rename '{old}' to '{new}' without replacing it first. "
                             f"'{old}' is a required property for this object. Try:\n"
                             f"stored = obj.{old}\n"
                             f"obj.{old} = new_value\n"
                             f"{f'obj.{new} = stored' if not alias else f'obj.add_block(\'{new}\',\'{alias}\', stored)'}\n")
        
        setattr(self, new_alias, getattr(self, old))
        delattr(self, old)
        idx = self._key_order.index(old)
        self._key_order[idx] = new_alias





@inherit_class_doc(SingleBlock)
class FileBlock(SingleBlock):
    """
    Represents a set of blocks loaded from a file.

    All public attributes of `FileBlock` objects are either `SingleBlock` or
    `ListBlock` objects. Attributes without a header at the start of the file
    are parsed into `{"metadata": blockDict}` before passing to `FileBlock`.
    
    Noteable Subclasses:
    ```
    Synthesis(FileBlock)
    TemplateSet(FileBlock)
    ```
    """
    @inherit_docstring(SingleBlock)
    def __init__(self, blockDict, _sourceFile=None):
        """
        Optionally specify _sourceFile before constructing from blockDict using parent `SingleBlock` constructor.
        """
        self._sourceFile = _sourceFile

        self._tempdir = tempfile.TemporaryDirectory()
        self._temppath = Path(self._tempdir.name)
        atexit.register(self.cleanup)

        super().__init__(blockDict)
    
    def cleanup(self):
        if self._tempdir is not None:
            self._tempdir.cleanup()

    @classmethod
    def fromFile(cls, filepath):
        abspath = os.path.abspath(filepath)
        blockDict = dict_from_file(abspath)
        return cls(blockDict, _sourceFile = abspath)
    
    def save(self, filepath:str=None):
        """
        Sends a serialized dict to be written to file.

        Args:
            filepath:
                If specified, writes serialized dict to filepath. ks to `self._sourceFile`.

        Raises:
            ValueError:
                If _sourceFile is not specified (if `FileBlock` was copied from
                another object or constructed directly from a blockDict),
                filepath must be specified.
        """
        from warnings import warn
        saving_as = filepath is not None
        try:
            if filepath is None:
                if self._sourceFile is None:
                    raise ValueError("Synthesis object was constructed without a sourceFile. A save destination must be specified.")
                else:
                    filepath = self._sourceFile
            
            self._sourceFile = os.path.abspath(filepath)
            blockDict = self.serialize()

            write_dict_to_file(blockDict, self._sourceFile)
        except Exception as e:
            if not saving_as:
                warn(f"Could not save file: {e}", RuntimeWarning)
                return e
            else:
                raise e
        return True
    
    def matches_file(self):
        reloaded = self.fromFile(self._sourceFile)

        return self.__eq__(reloaded, suppress_routine_paths=True)
        



class ListBlock(Block):
    """
    Represents multiple similar blocks of key:value pairs parsed from a FOS File

    `ListBlock`s are used to group multiple `SingleBlock`s of the same subclass
    together and define methods that modify or access information from multiple
    `SingleBlock`s at once. `SingleBlocks` contained within a `ListBlock` can be
    indexed and iterated over directly instead of calling `ListBlock._objs`

    Attributes:
        _objs: List containing the stored `SingleBlock` objects.
        _reqCls:
            Specifies which `SingleBlock` subclass the objects in `_objs` must belong to.

    Notable Subclasses:
    ```
    MaterialList(ListBlock) # Contains Material(SingleBlock) objects
    TreamentList(ListBlock) # Contains Treatment(SingleBlock) objects
    ```
    """
    _reqCls = None
    def __init__(self, blockList:list):
        """
        Constructs a `ListBlock` from a list of serialized dictionaries.

        Each dict in blockList is passed directly to the constructor of the
        required `SingleBlock` class. To construct a `ListBlock` from a list of
        previously-constructed `SingleBlock` objects, use
        `ListBlock.fromBlocks()` instead.

        Args:
            blockList:
                A list of serialized dictionaries. Each dictionary is passed to
                the `SingleBlock` constructor specified by `cls`
            cls:
                The `SingleBlock` subclass enforced during construction. This is
                usually passed in subclass definitions. 
        """
        self._objs = []
        for blockDict in blockList:
            obj = self._reqCls.subclass(blockDict)
            obj._parent_block = self
            self._objs.append(obj)
    
    @classmethod
    def fromBlocks(cls, blockList:list):
        """
        Constructs a `ListBlock` from a list of previously-constructed `SingleBlock` objects.

        Args:
            blockList:
                A list of `SingleBlock` objects. All entries must match the
                class defined in `ListBlock` subclass definition.

        Raises:
            TypeError: this function can only be called from a subclass that has
            already defined the required `SingleBlock` subclass.

        Example:
        ```
            # Entries already constructed as Material(SingleBlock) objects
            matList = [zinc, antimony, barium]
            # MaterialList(ListBlock) enforces only Material(SingleBlock) objects.
            materials = MaterialList(matList) 
        ```
        """
        try:
            obj = cls([])
        except TypeError as e:
            raise TypeError(f"Please note: you must call fromBlocks from a subclass (such as MaterialList.fromBlocks()).\n{e}")
        obj._objs = blockList.copy()
        return obj
    
    @classmethod
    def Simple(cls, reqCls=SingleBlock):
        if not issubclass(reqCls, SingleBlock):
            raise TypeError("reqCls must be a subclass of SingleBlock")
        if cls._reqCls is not None:
            raise TypeError("You cannot create a simple subclass of another ListBlock subclass.")
        
        class SimpleSub(cls):
            _reqCls = reqCls

        name = f"{reqCls.__name__}List"
        qualname = f"{cls.__name__}.Simple.{name}"
        module = cls.__module__

        SimpleSub.__name__ = name
        SimpleSub.__qualname__ = qualname
        SimpleSub.__module__ = module

        return SimpleSub


    def __setattr__(self, name, value):
        """
        Only private attributes starting with "_" can be set.
        
        Items in self._objs can be edited individually by indexing with self[i],
        or self._objs can be replaced with a new list, which is re-validated and
        coerced to the correct `SingleBlock` subclass specified by _reqCls
        """
        if name == "_objs":
            if type(value) is not list:
                raise TypeError(f"{type(self).__name__}._objs must be a list of objects.")

            elif hasattr(self, "_reqCls"):
                typ = self._reqCls
                for obj in value:
                    if not isinstance(obj, typ):
                        try:
                            obj=typ.subclass(obj.serialize())
                            obj._parent_block = self
                        except:
                            raise TypeError(f"{type(self).__name__}._objs must be an empty list or list of {typ.__name__} objects.")
            return super().__setattr__(name, value)

        elif name.startswith("_") or name in self._reserved:
            return super().__setattr__(name,value)
        else:
            raise AttributeError(
                f"{type(self).__name__} does not allow setting attribute '{name}'. "
                f"Only private names starting with '_' can be used. "
                f"Each list item is an item in {type(self).__name__}._objs which can be edited individually, "
                f"Or you can replace {type(self).__name__}._objs with a new list of objects."
            )
    def append(self, obj:SingleBlock):
        """
        Append a `SingleBlock` object of the correct class to `self._objs` and revalidate.
        """
        objs = self._objs.copy()
        objs.append(obj)
        self._objs = objs
    
    def insert(self, idx, obj:SingleBlock):
        objs = self._objs.copy()
        objs.insert(idx,obj)
        self._objs = objs

    def remove_idx(self, from_idx:int=None, to_idx:int=None):
        if from_idx is None and to_idx is None:
            self._objs = []

        objs = self._objs.copy()

        if from_idx is None:
            objs = objs[to_idx:]
        elif to_idx is None:
            objs = objs[:from_idx]
        else:
            objs = objs[:from_idx] + objs[to_idx:]

        self._objs = objs   

    def __getitem__(self, idx):
        return self._objs[idx]
    
    def __len__(self):
        return len(self._objs)
    
    def __iter__(self):
        return iter(self._objs)
    
    def __eq__(self, other):
        from .._debug import deep_diff
        try:
            return len(deep_diff(self.serialize(), other.serialize()))==0
        except:
            return False
        
    def __hash__(self):
        return id(self)
    
    def set_list_type(self,typ="explicit"):
        if typ not in ("explicit", "looped"):
            raise ValueError("List type must be 'single' or 'looped'.")
        for obj in self:
            obj._meta.list_type = typ
        
    def serialize(self):
        for obj in self:
            if obj._meta.list_type == "explicit":
                self.set_list_type("explicit")
                break
        return [obj.serialize(keepListType=True if len(self)>1 else False) for obj in self]
    
    @inherit_docstring(SingleBlock, label="Related")
    def list_avail_routines(self, recursive=False, prefix="", abbreviated=False):
        """
        Lists all methods decorated as calc routines.

        Methods are resolved as path strings relative to self, including
        indexing for recursively searched methods within self._objs. When
        returned back to a parent `ListBlock` object's call, these strings
        produce paths that can be resolved back into function calls relative to
        the parent object. See `SingleBlock.list_avail_routines()`.

        This method is usually only used in a recursive call from a
        `SingleBlock` object where one of its attributes is a `ListBlock`.

        Example:
        ```
        mySyn.materals.list_avail_routines(recursive=True)
        ## returns [
        ##     'add_weight_pcts',
        ##     '[0].add_MW',
        ##     '[1].add_MW',
        ##     ... 6 total materials with the same calc_routine
        ##     '[5].add_MW'
        ## ]
        
        # Resursive call from `SingleBlock` mySyn object:
        mySyn.list_avail_routines(recursive=True)
        ## returns [
        ##     'reaction.add_nom_MW',
        ##     'materials.add_weight_pcts',
        ##     'materials[0].add_MW',
        ##     'materials[1].add_MW',
        ##     ... 6 total materials with the same calc_routine
        ##     'materials[5].add_MW'
        ## ]
        ```
        """
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
                    if hasattr(obj, "list_avail_routines"):
                        rtns = obj.list_avail_routines(True,f"{prefix[:-1]}[{idx_str}].",abbreviated=True)
                        for routine in rtns:
                            if routine not in obj_routines:
                                obj_routines[routine] = []
                            obj_routines[routine].append(i)
                for routine, i_list in obj_routines.items():
                    routines.append(f"{routine}; {idx_str} = {i_list}")
            else:
                for i, obj in enumerate(self._objs):
                    if hasattr(obj, "list_avail_routines"):
                        child_prefix = f"{prefix[:-1]}[{i}]."
                        routines.extend(obj.list_avail_routines(
                            recursive=True,
                            prefix=child_prefix,
                            abbreviated=False
                        ))

        return routines
    
    def copy(self):
        """Returns a deep copy by serializing and then reconstructing."""
        cls = type(self)
        return cls(self.serialize(keepListType=True))
    
    def remove_any(self, **kwargs):
        """
        Remove any objects from self._objs with attributes matching `kwargs`
        
        Args:
            **kwargs:
                A single keyword argument can be passed. Any objects with
                attr:value matching kw:arg are removed.

        Raises:
            TypeError: Exactly one keyword argument is required.

        Example:
        ```
        mySyn.materials.remove_any(supplier="sigma")
        ## removes any obj from mySyn.materials._objs where
        ## obj.supplier == "sigma"
        ```
        """
        if len(kwargs) != 1:
            raise TypeError("Exactly one keyword argument is required")
        
        key, val = next(iter(kwargs.items()))
        
        objs = self._objs.copy()
        removed = 0
        for obj in objs:
            if getattr(obj, key, None) == val:
                for i, existing in enumerate(self._objs):
                    if existing is obj:
                        del self._objs[i]
                        removed += 1
                        break
        _debug.msg(f"Removed {removed} {self._reqCls.__name__} objects matching {key} = {val}.")
    
    def get_any(self, **kwargs):
        if len(kwargs) != 1:
            raise TypeError("Exactly one keyword argument is required")
        
        key, val = next(iter(kwargs.items()))
        found = []
        for obj in self._objs:
            if getattr(obj, key, None) == val:
                found.append(obj)
        return found
    
    def get_first(self, **kwargs):
        return self.get_any(**kwargs)[0]
