import inspect
from ._containers import SimpleWrapper, SubContainer
from ..config import values as cfg
from ..parsing.syntax import (
    meta_keys as mk,
    meta_defaults as md,
)

from .. import _errors as err

from ._blockUtils import _unwrap_block

from .._debug import Debug
_debug = Debug()

def _add_comments_to_parent(attr_name):
    """
    Generate an attachable method to add comments to a parent block.

    Returned function is attachable to any attribute-bound
    [`Block`][FoSpy.blocks.blocks.Block] instance [as `add_comments(self,
    *comments)`][FoSpy.blocks.blocks.Block.add_comments].

    Returns:
        (function): `func(self_attr, *comments)`
    """
    def func(self_attr, *comments):
        """
        Attach comments to self in the parent block.

        Mutates the parent block's comments metadata under the assigned attribute name.

        Args:
            *comments (str):
                Comments to attach to the assigned attribute name in
                the parent block's metadata. Comments are printed above
                their attached attribute when saving in the FOS format.
        """
        parent_comments = self_attr._parent_block._meta.comments
        parent_comments.setdefault(attr_name,[])
        for comment in comments:
            parent_comments[attr_name].append(str(comment))
    return func


def _clear_comments_from_parent(attr_name):
    """
    Generate an attachable method to clear comments from a parent block.

    Returned function is attachable to any attribute-bound
    [`Block`][FoSpy.blocks.blocks.Block] instance [as
    `clear_comments(self)`][FoSpy.blocks.blocks.Block.clear_comments].

    Returns:
        (function): `func(self_attr)`
    """
    def func(self_attr):
        """
        Remove comments attached to self in the parent block.

        Clears parent block's comments metadata under the assigned attribute name.
        """
        parent_comments = self_attr._parent_block._meta.comments
        parent_comments[attr_name] = []
    return func

class Block:
    """
    The base class for any set of data found in a FOS file.
    """
    @classmethod
    def inspect(self):
        # for breaking to debugger from gui
        raise Exception("put a break point here")

    def find_fileblock(self):
        """
        Finds the parent file object.

        Walks upward through `_parent_block` attributes until a
        [`FileBlock`][FoSpy.blocks.files.FileBlock] instance is found and
        returns that instance.
        """
        from .files import FileBlock
        from .._errors import FileBlockNotFoundError

        blk = self
        while blk is not None:
            if isinstance(blk, FileBlock):
                return blk
            if hasattr(blk,"_parent_block"):
                blk = blk._parent_block
            else:
                blk = None
        raise FileBlockNotFoundError("Could not find a FileBlock containing the current object")
    
    def get_prop_path(self):
        from .files import FileBlock

        if not hasattr(self, "_parent_block"):
            if isinstance(self, FileBlock):
                root_path = f"<{str(self.get_file_name())}>"
            else:
                root_path = f"<Root {type(self).__name__}"
                if isinstance(self, SingleBlock):
                    id_key, id_txt = self.get_id()
                    if id_key is not None:
                        root_path += f" ({id_key}={id_txt})"
                root_path += ">"
            return root_path
        
        parent_path = self._parent_block.get_prop_path()
        parent_prop = self.get_parent_prop()

        if "[" not in parent_prop:
            return parent_path + "." + parent_prop
        
        return parent_path + parent_prop
    
    def get_parent_prop(self):
        if not hasattr(self, "_parent_block"):
            return None
        parent_blk = self._parent_block
        
        if isinstance(parent_blk, SingleBlock):
            for prop, val in parent_blk.get_prop_dict().items():
                if val is self:
                    return prop
        
            raise err.FoSpyStructureError(f"Block {self} points to a parent block {parent_blk} that does not contain it as a property.")
        
        elif isinstance(parent_blk, ListBlock):
            return f"[{parent_blk.get_idx(self)}]"
        
        raise err.FoSpyStructureError(f"Block {self} has an unknown parent block type: {type(parent_blk)}")
    
    def add_comments(self, *comments):
        """
        Attach comments to self in the parent block.

        Mutates the parent block's comments metadata under the assigned
        attribute name.

        Args:
            *comments (str):
                Comments to attach to the assigned attribute name in
                the parent block's metadata. Comments are printed above
                their attached attribute when saving in the FOS format.

        Example:
            ```
            >>> my_synthesis.materials.add_comments("A comment on the materials header")
            >>> my_synthesis._meta.comments 
            {"materials":
                [
                    "an older comment", 
                    "A comment on the materials header"
                ]
            }
            ```
        """
        # placeholder. Method is injected by _add_comments_to_parent when this
        # block is assigned as an attribute of another block
        return
    
    def clear_comments(self_attr):
        """
        Remove comments attached to self in the parent block.

        Clears parent block's comments metadata under the assigned attribute name.

        Example:
            ```
            >>> my_synthesis._meta.comments["materials"]
            ["This comment was read from a FOS file"]

            >>> my_synthesis.materials.clear_comments()
            >>> my_synthesis._meta.comments["materials"]
            []
            ```
        """
        # placeholder. Method is injected by _clear_comments_from_parent when this
        # block is assigned as an attribute of another block
        return
    
    def find_tempdir(self):
        """
        Find the parent file object's temporary directory.

        Finds the temporary directory created by the
        [`FileBlock`][FoSpy.blocks.files.FileBlock] instance containing this
        block as one of its attributes. 
        
        Returns:
            tempdir (tempfile.TemporaryDirectory):
                The temporary directory created by the parent file object
        """
        fileblock = self.find_fileblock()
        if hasattr(fileblock, "_tempdir"):
            return fileblock._tempdir
        else:
            raise AttributeError("Could not find a temporary directory attached to this object's FileBlock")
    
    def find_temppath(self):
        """
        Find the parent file object's temporary directory path.

        Similar to [`find_tempdir`][FoSpy.blocks.blocks.Block.find_tempdir] but
        returns the corresponding `pathlib.Path` object instead.
        """
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

    def track_attachments(self, new_copy="prompt",overwrite="prompt", **kwargs):
        self._att_new_copy = new_copy
        self._att_overwrite = overwrite
        
class SingleBlock(Block):
    """
    Represents a single block of key:value pairs parsed from a FOS file.

    Subclasses are mapped to expected keys and validation routines in
    [`..parsing.validation`][FoSpy.parsing.validation]. Expected values are validated and assigned to
    public attributes. Unexpected values are assigned to attributes of
    `self.ext` for safety, but can still be accessed as an attribute of the
    SingleBlock object if not overwritten

    Notable Subclasses:
    [`FileBlock(SingleBlock)`][FoSpy.blocks.files.FileBlock]
    [`Synthesis(FileBlock)`][FoSpy.blocks.synthesis.Synthesis]
    [`Reaction(SingleBlock)`][FoSpy.blocks.metadata.Reaction]
    [`Material(SingleBlock)`][FoSpy.blocks.materials.Material]
    [`TemplateBlock(SingleBlock)`][FoSpy.blocks.template.TemplateBlock]
    """
    dispatch = {}
    dispatch_key = None
    dispatch_default = None
    dispatch_allow_self = True
    _aliases = None
    _id_key = None

    @classmethod
    def print_summary(cls, mode="cli"):
        from .._docs.properties import get_summary

        print(get_summary(cls, mode=mode))

    @classmethod
    def TemplateClass(cls,*args:str):
        """
        Create a template for a subclass of `SingleBlock`.

        Generates a hybridized subclass of the current block class and
        [`TemplateBlock`][FoSpy.blocks.template.TemplateBlock]. Template
        subclasses override original expected validators with either a
        [`TemplateField`][FoSpy.blocks.template.TemplateField],
        [`TemplateBlock`][FoSpy.blocks.template.TemplateBlock], or
        [`TemplateList`][FoSpy.blocks.template.TemplateList] depending on the
        type of the original validator.

        Args:
            *args: A list of properties to override as template types.
        """
        from .template import TemplateBlock, TemplateField, TemplateList
        from ..parsing.validation import required_keys, optional_keys
        if issubclass(cls, TemplateBlock):
            class ExtendedTemplate(cls):
                pass
            SubTemplate = ExtendedTemplate
        else:
            class NewTemplate(TemplateBlock, cls):
                dispatch = {}
                def __init__(self, blockDict, _dispatched=False):
                    super().__init__(blockDict, _dispatched=_dispatched)
                    self._full_class = cls
            SubTemplate = NewTemplate
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
   
    @classmethod
    def reflex(cls, serialize=True, include_temp_names=True, clean=False, **kwargs:dict):
        """
        Generate a flexible template for the current class.

        Flexibly generates a template for the current class where any required
        properties missing from `kwargs` are automatically converted to template
        types (See
        [`FlexTemplate`][FoSpy.blocks.template.FlexTemplate]).
        Returns an instance of the flexible template constructed from `kwargs`,
        or a serial dictionary of that instance.
        
        Args:
            serialize (bool):
                Whether to return the serialized dictionary of the reflexed
                template, or the object itself.
            **kwargs (str): Known properties to pass to the template constructor.
        """
        from .template import FlexTemplate
        class Flex(FlexTemplate, cls):
            _baseReq = cls
        
        kwargs.setdefault("template_name", f"Reflexed {cls.__name__}")

        empty = Flex.dispatch_subclass(kwargs)
        if serialize:
            serial = empty.serialize(clean=clean)
            if not include_temp_names:
                from ._blockUtils import _prune_template_names
                serial = _prune_template_names(serial)
            return serial
        return empty
    
    @staticmethod
    def make_dispatch(func):
        @classmethod
        def dispatcher(cls, blockDict, _visited=None, **kwargs):
            if _visited is None:
                _visited = []
            elif cls in _visited:
                return cls(blockDict, _dispatched=True, **kwargs)
            else:
                _visited.append(cls)

            dispatch_from = getattr(cls, "dispatch_from", None)
            if dispatch_from is not None and dispatch_from not in _visited:
                full_block = dispatch_from.dispatch_subclass(blockDict, **kwargs)
                if not isinstance(full_block, cls):
                    from .. import _errors as err
                    raise err.FoSpyStructureError(f"Attempted to construct the blockDict below into a {cls.__name__} "
                                                  "object, but it was dispatched to a different subclass "
                                                  f"({full_block.__class__.__name__})\n\n{blockDict}")

                return full_block

            blockDict = _unwrap_block(blockDict)
                
            dispatched = func(cls, blockDict, **kwargs)
            if dispatched in _visited:
                return dispatched(blockDict, _dispatched=True, **kwargs)

            # call original return's method, not the extracted class
            return dispatched.dispatch_subclass(blockDict, _visited=_visited, **kwargs)
        
        return dispatcher

    @make_dispatch
    def dispatch_subclass(cls, blockDict:dict, _visited=None, **kwargs:any):
        """
        Recommended dispatcher to allow subclass delegation when constructing.
        
        Overridden in some subclasses, usually to assign subclass based on the
        value of one or more properties.

        Default behavior passes `blockDict` and `**kwargs` to `__init__`
        constructor.
        """
        from .. import _errors as err
        blockDict = _unwrap_block(blockDict).copy()

        dispatch_val = blockDict.get(cls.dispatch_key, None)
        dispatched_cls = cls.dispatch.get(dispatch_val, None)

        if dispatched_cls is None:
            if not cls.dispatch_default:
                if not cls.dispatch_allow_self:
                    raise err.FailedValidatorError(
                        cls.dispatch_key, cls,
                        Exception("This block type must be dispatched to another subclass."),
                        blockDict=blockDict,
                        hint=f"Could not find a valid dispatch value for {cls.dispatch_key} = {dispatch_val}.")
                else:
                    dispatched_cls = cls
            else:
                dispatched_cls = cls.dispatch_default

        return dispatched_cls
    
    @classmethod
    def build_req_validators(cls):
        """
        Builds required keys and validators mapped to subclass.

        Walks all parent classes and builds a map of all keys that are required
        during `__init__`, and their respective validation routines. Subclasses
        are mapped to expected keys and validations in
        [`parsing.validation`][FoSpy.parsing.validation]. Subclass validations
        override parent classes when applicable.

        Returns:
            merged (dict):
                Maps required keys to validation routines. Routines may be
                a class constructor or a func taking one arg.
        Example:
            ``` 
            >>> SingleBlock.build_req_validators()
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
        from ._blockUtils import _get_prop_mro, _merge_vals
        merged = {}
        # mro = list(reversed(cls.__mro__))
        # for i, base in enumerate(mro):
        #     base_reqs = required_keys.get(base,{})
        #     for key, validator in base_reqs.items():
        #         # allow subclasses to remove parent requirements.
        #         if not validator:
        #             merged.pop(key, None)
        #         else:
        #             merged[key] = validator

        req_mro = _get_prop_mro(cls, required_keys)
        for i in range(len(req_mro)):
            merged = _merge_vals(merged, req_mro, i)

        merged.pop("__all__")

        return merged

    @classmethod
    def build_validators(cls):
        """
        Builds expected keys and validators mapped to subclass.

        Walks all parent classes and builds a map of all keys that are expected
        (required or optional), and their respective validation routines.
        Subclasses are mapped to keys and validations in
        [`parsing.validation`][FoSpy.parsing.validation]. Subclass validations
        override parent classes when applicable.

        See
        [`build_req_validators`][FoSpy.blocks.blocks.SingleBlock.build_req_validators]
        """
        from ..parsing.validation import required_keys, optional_keys
        from ._blockUtils import _merge_vals, _get_prop_mro
        from .._docs.properties import _validator_rules
        merged = {}
        # for base in reversed(cls.__mro__):
        #     for key_set in (required_keys, optional_keys):
        #         base_reqs = key_set.get(base,{})
        #         for key, validator in base_reqs.items():
        #             # allow subclasses to remove parent requirements.
        #             if validator is False:
        #                 merged.pop(key, None)
        #             else:
        #                 merged[key] = validator
        req_mro = _get_prop_mro(cls, required_keys)
        opt_mro = _get_prop_mro(cls, optional_keys)

        for i in range(len(req_mro)): # req_mro and opt_mro are the same length
            merged = _merge_vals(merged, req_mro, i)
            merged = _merge_vals(merged, opt_mro, i)

        universal_val = merged.pop("__all__")

        @_validator_rules(inherit_from=universal_val)
        def universal_val_method(cls, *_, _m=universal_val, **__):
            return _m(*_, **__)

        cls.universal_val = universal_val_method

        return merged
    
    def get_validators(self):
        """
        Overrides class validators with any renamed properties.

        Similar to class method:
        [`build_validators`][FoSpy.blocks.blocks.SingleBlock.build_validators],
        but uses
        [`_rename_validators`][FoSpy.blocks.blocks.SingleBlock._rename_validators]
        to align any renamed properties with their original validators. Also
        adds any optional key overrides added by key$alias syntax.

        Returns:
            vals (dict): maps expected keys to validation routines.
        """
        vals = self._rename_validators(self.build_validators())
        if hasattr(self, "_key_overrides"):
            for key, val in self._key_overrides.items():
                vals[key] = val
        return vals
    
    def get_req_validators(self):
        """
        Overrides class validators with any renamed properties.

        Similar to class method:
        [`build_req_validators`][FoSpy.blocks.blocks.SingleBlock.build_req_validators],
        but uses
        [`_rename_validators`][FoSpy.blocks.blocks.SingleBlock._rename_validators]
        to align any renamed properties with their original validators.
        """
        return self._rename_validators(self.build_req_validators())

    def __init__(self, blockDict:dict, _dispatched=False):
        """
        Constructs a SingleBlock object from a dictionary.

        Avoid using this constructor for unfamiliar block classes, it may bypass
        subclass delegation. Use
        [`dispatch_subclass`][FoSpy.blocks.blocks.SingleBlock.dispatch_subclass]
        instead.

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
            _dispatched:
                Flag passed by
                [`dispatch_subclass`][FoSpy.blocks.blocks.SingleBlock.dispatch_subclass]
                to signal that the safer construction method was used. Warning
                issued for False


        Raises:
            ValueError:
                A key required by `SingleBlock.build_req_validators()` is not
                present.
            TypeError:
                The value passed as `blockDict` was not able to be unwrapped
                into a dict, either by serialization of a passed `Block` object
                or by list index.

        """
        from .metadata import Rename, MetaData
        self._staged_templates = {}
        self._constructed = False
        property_errors = []

        if not _dispatched:
            from warnings import warn
            warn(f"You should avoid directly constructing a {type(self).__name__} object. Use the dispatch_subclass() "
                 "method instead to allow for subclass delegation when constructing.", stacklevel=2)

        self.track_attachments(**cfg.track_attachments())

        from ..parsing.validation import aliases as als
        new_als = als.copy()
        new_als.update(self._aliases or {})
        self._aliases = new_als
        self._reserved = ['ext']

        blockDict = _unwrap_block(blockDict)
        self._sourceDict = blockDict.copy()

        if not isinstance(blockDict, dict):
            raise TypeError("A SingleBlock must be constructed from either a dictionary or another SingleBlock. "
                            "The passed source can optionally be wrapped in lists of length == 1.")

        blockDict = blockDict.copy()

        rename = blockDict.pop("rename",None)
        if rename:
            setattr(self, "rename", _unwrap_block(rename))
        elif not isinstance(self, (Rename, MetaData)):
            setattr(self, "rename", {})

        req = self.get_req_validators()
        req.pop("ext",None)
        for key, validator in req.items():
            if key not in blockDict:
                from .template import TemplateBlock, TemplateList, TemplateField, FlexTemplate
                is_type = isinstance(validator, type)
                if is_type and issubclass(validator, TemplateField):
                    blockDict[key] = ""
                elif is_type and issubclass(validator, FlexTemplate):
                    blockDict[key] = {"template_name": f"Empty {self._baseReq.__name__} Template"}
                elif is_type and issubclass(validator, TemplateBlock):
                    blockDict[key] = validator.reflex()
                elif is_type and issubclass(validator, TemplateList):
                    blockDict[key] = []
                else:
                    property_errors.append(err.MissingPropertyError(key, self, blockDict=blockDict))
        
        self._meta = SubContainer()
        self._calc_comments = {}
        self._calc_routines = []
        self._key_overrides = {}

        for attr, key in mk.items():
            try:
                k = md[key].copy()
            except AttributeError:
                k = md[key]
            setattr(self._meta, attr, blockDict.pop(key,k))

        self._key_order = []
        self.ext = SubContainer()

        for key, val in blockDict.items():
            self._key_order.append(key)
            try:
                setattr(self, key, val)
            except err.PropertyError as e:
                property_errors.append(e)

        if property_errors:
            raise err.PropertyErrorGroup(self, blockDict=blockDict, errors=property_errors)
        
        self._constructed = True

    def _update_src(self):
        if self._constructed and self._props_changed:
            self._sourceDict = self.serialize(clean=True)
            self._props_changed = False

        return self._sourceDict   
     
    def __setattr__(self, name:str, value):
        """
        Assign an attribute with validation and controlled namespace behavior.

        Contract:
            `SingleBlock` enforces type correctness and validator execution for
            all public attributes defined for its subclass.

            Required types and validators are mapped by subclass in
            [`parsing.validation`][FoSpy.parsing.validation]

            Comment-mutating methods are attached to every object assigned to an
            attribute. (See
            [`add_comments`][FoSpy.blocks.blocks._add_comments_to_parent])

        Rules:
            1. Private attributes (`_`-prefixed) bypass validation.
            2. Attributes with registered validators are processed through the
            validator before assignment.
            3. Attributes with required types are coerced by calling the type
            constructor when necessary.
            4. Unrecognized attributes can be assigned to a validator mapped to
            an alias in [`parsing.validation`][FoSpy.parsing.validation], using
            the syntax `name="name$alias"`.
            5. Unrecognized attribute names are redirected as attributes of
            `self.ext`.

        Raises:
            ValueError:
                - If a required `SingleBlock` is passed as a list with length > 1.
                - If a block alias cannot be parsed from a key containing `$`.
                - If a block alias is unrecognized.
                - If a template field is found when constructing a non-template
                  subclass.
        """
        if name.startswith("_") or name in self._reserved:
            return super().__setattr__(name, value)
        
        from ..parsing.format_fos import format_field
        from .template import TemplateField, TemplateBlock
        
        validators = self.get_validators()
        
        if "$" in name:
            try:
                name, alias = name.split("$")
            except Exception:
                self._update_src()
                raise err.PropertyAliasError(name, self, blockDict=self._update_src(), hint="Unable to parse a block alias from key containing '$' character: ")
            
            try:
                val = self._aliases[alias]
            except KeyError:
                self._update_src()
                raise err.PropertyAliasError(name, self, blockDict=self._update_src(),
                                             hint=f"Unrecognized block alias: '{alias}' assigned to property: ",
                                             posthint=f"Valid aliases: {list(self._aliases.keys())}")
            
            if name in validators and val != validators[name]:
                self._update_src()
                raise err.PropertyAliasError(name, self, blockDict=self._update_src(),
                                             hint=f"Cannot apply '{alias}' alias override to property: ",
                                             posthint="That property is already assigned to a validator. "
                                             f"The following properties are reserved: {list(validators.keys())}")
            if name not in validators:
                validators[name] = val
                self._key_overrides[name] = val

        if name in validators:
            universal_val = self.universal_val

            validator = validators[name]
            # val_kwargs = {}
            # for kw, arg_func in (("sourceDict", self._update_src),("cls", lambda:type(self))):
            #     try:
            #         if kw in sign(validator).parameters:
            #             val_kwargs[kw] = arg_func()
            #     #TODO: find a better way to handle this
            #     except Exception:
            #         pass

            val_kwargs = {
                "sourceDict": self._update_src(),
                "blk_cls": type(self),
                "prop_name": name
            }
                
            value = universal_val(value, **val_kwargs)

            if isinstance(validator, type):
                if issubclass(validator, SingleBlock):
                    validator = validator.dispatch_subclass
                    val_kwargs = {}
                    value = _unwrap_block(value)
                    pass
                elif issubclass(validator, ListBlock):
                    val_kwargs = {}

                elif value == format_field("template") and not issubclass(validator, TemplateField):
                    if isinstance(self,TemplateBlock):
                        validator = TemplateField
                    else:       
                        e = ValueError("You cannot assign a template field as a property for a non-template object.")
                        raise err.FailedValidatorError(name, self, e, blockDict=self._update_src(), hint="Template field passed to non-template property: ")
                if isinstance(validator, type) and isinstance(value, validator):
                    return self._assign_and_inject(name, value)
            
            try:
                sig = inspect.signature(validator)
                needs_kwargs = any(
                    p.kind==p.VAR_KEYWORD for p in sig.parameters.values()
                )
            except Exception:
                needs_kwargs = False

            try:  
                val = validator(value, **val_kwargs) if needs_kwargs else validator(value)
            except Exception as e:
                raise err.FailedValidatorError(name, self, e, blockDict=self._update_src())
                
            return self._assign_and_inject(name, val)
        else:
            return self._assign_and_inject(name, value, extended=True)

    def __getattr__(self, name:str):
        """
        Check both `self` and `self.ext` for attribute before returning.
        
        A matching attribute of `self` will be returned first, but if `self` has
        no matching attribute, a matching attribute of `self.ext` can be
        returned instead.
        """

        try:
            if name not in ("rename", "ext") and hasattr(self, "rename"):
                rename_dict = self.rename.serialize(shallow=True, clean=True)
                if name in rename_dict:
                    return getattr(self, rename_dict[name])
                
            if name != 'ext':
                return getattr(self.ext, name)
            
            raise AttributeError()
        except AttributeError:
            raise AttributeError(
                f"{type(self).__name__} object "
                f"has no attribute {name!r}."
            )

    def __eq__(self, other, suppress_routine_paths:bool=False):
        """
        Check equality of two `SingleBlock` objects.
         
        Equality is checked by a deep difference of their
        [serialized][FoSpy.blocks.blocks.SingleBlock.serialize] dictionaries.

        Args:
            suppress_routine_paths:
                Optional flag to still return true if the only differences found
                are in [calculation
                routine][FoSpy.blocks.blocks.SingleBlock.add_calc_routine]
                metadata. Calculation routines are for user information only and
                may not be relevant for equality.
        """
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

    def stage_template(self, prop_name, template:Block|dict=None):
        from .template import TemplateBlock
        if template is None:
            template = {}

        if not isinstance(template, (TemplateBlock, dict)):
            raise ValueError("Template must be a TemplateBlock or dictionary. To 'stage' a ListBlock, "
                             "you can stage a SingleBlock template with a ListBlock alias. This creates "
                             "a non-template ListBlock with the template staged as its first entry.")
        
        alias_validator = None
        if "$" in prop_name:
            prop_name, alias = prop_name.split("$",1)
            try:
                alias_validator = self._aliases[alias]
            except KeyError as e:
                raise err.PropertyAliasError(prop_name, self, blockDict={prop_name: "<staged template>"},
                                             hint=f"Unrecognized block alias: '{alias}' assigned to property: ",
                                             posthint=f"Valid aliases: {list(self._aliases.keys())}") from e

        if hasattr(self, prop_name):
            raise ValueError(f"Property {prop_name} already exists. You cannot stage a template for a property that already exists.")
        
        validators = self.build_validators()
        validator = validators.get(prop_name, None)

        if validator is not None:
            alias = None

        if alias_validator is not validator and None not in (validator, alias_validator):
            raise ValueError(f"Property {prop_name} already has a validator. You cannot alias a different validator for the same property.")
        
        validator = next(v for v in (validator, alias_validator) if v is not None)

        if validator is None:
            try:
                if not isinstance(template, TemplateBlock):
                    raise TypeError("Dictionary templates must be staged with an alias.")

                alias = next(k for k, v in self._aliases.items() if isinstance(template, v))
                validator = self._aliases[alias]
            except (TypeError,StopIteration) as e:
                raise ValueError(f"Property {prop_name} is unexpected. In order to stage a template "
                                "for and unexpected property, you must specify the validator with a '$' alias "
                                "in the property name, or stage a pre-constructed template of an aliasable validator."
                                ) from e

        if isinstance(validator, type) and issubclass(validator, ListBlock):
            # let setattr handle ListBlock construction using alias
            # this creates an empty ListBlock under self.prop_name
            # (alias stripped during setattr)
            setattr(self, prop_name+"$"+alias if alias is not None else prop_name, [])
            empty_lb = getattr(self, prop_name)
            return empty_lb.stage_template("entry0", template)

        if isinstance(template, dict):
            # reflex returns a TemplateBlock subclassed from the validator
            template = validator.reflex(serialize=False, include_temp_names=True, clean=False, **template)
            template.template_name = prop_name

        elif not isinstance(template, validator):
            val_nm = validator.__name__
            if alias is None:
                error_msg = f"The provided template is not compatible with the validator expected for property '{prop_name}' ({val_nm})."
            else:
                error_msg = f"The provided template is not compatible with the validator specified by alias '{alias}' ({val_nm})."
            raise ValueError(error_msg)


        template._staged_parent = self

        if alias is not None:
            self._key_overrides[prop_name] = validator
            
        self._staged_templates[prop_name] = template

        return prop_name, template
    
    def fill_staged_template(self, prop_name, **kwargs):
        from .template import TemplateBlock
        prop_key = prop_name.split("$")[0] if "$" in prop_name else prop_name

        template = self._staged_templates.pop(prop_key, None)
        if template is None:
            prop_name, _ = self.stage_template(prop_name)
            return self.fill_staged_template(prop_name, **kwargs)

        prop_name = prop_key

        try:
            filled = template.fill(staged=True,**kwargs)
        except Exception:
            partial = template.fill(staged=True,incomplete=True, **kwargs)
            self._staged_templates[prop_name] = partial
            partial._staged_parent = self
            return prop_name, partial
        
        try:
            setattr(self, prop_name, filled)
        except Exception as e:
            raise Exception(f"Template was filled but could not be assigned {prop_name}") from e
        
        filled = getattr(self, prop_name)

        if isinstance(self, TemplateBlock):
            self.fill()
        
        return prop_name, filled

    def has_staged(self):
        if len(self._staged_templates) > 0:
            return True
        
        for val in self.get_prop_dict().values():
            if hasattr(val, "has_staged") and val.has_staged():
                return True

    def rename_dict(self):
        if not hasattr(self, "rename"):
            return {}
        return self.rename.serialize(shallow=True, clean=True)
    
    def get_id(self):
        """Returns an easily recognizable identifier for self. Non-unique."""
        id_txt = str(getattr(self, self._id_key)) if self._id_key is not None else type(self).__name__
        return self._id_key, id_txt
    
    def get_prop_dict(self):
        """Returns a dictionary mapping property names to their live object values."""
        serial = self.serialize(shallow=True, clean=True)
        out = {}
        for prop in serial:
            if "$" in prop:
                prop = prop.split("$")[0]
            out[prop] = getattr(self, prop)
        return out
    
    def _rename_validators(self, validators:dict):
        """
        Realigns any [renamed][FoSpy.blocks.blocks.SingleBlock.rename_block]
        attributes with their expected validator.

        Args:
            validators:
                A dictionary mapping attribute names to validators, returned by
                either
                [`build_validators`][FoSpy.blocks.blocks.SingleBlock.build_validators]
                or
                [`build_req_validators`][FoSpy.blocks.blocks.SingleBlock.build_req_validators]
        """
        if hasattr(self, "rename"):
            for name, rename in self.rename.serialize(shallow=True, clean=True).items():
                if name in validators and rename not in validators:
                    val = validators.pop(name)
                    validators[rename] = val
        return validators

    def _assign_and_inject(self, name, value, extended=False):
        """
        Attaches attributes and methods to any value before assigning it as an
        attribute of `self` or `self.ext`.

        Attributes Attached to Object:
            `_parent_block`: refers to `self`

        Methods Attached to Object:
            [`add_comments_to_parent`][FoSpy.blocks.blocks._add_comments_to_parent]
            [`clear_comments_from_parent`][FoSpy.blocks.blocks._clear_comments_from_parent]
        """
        from .attachments import Attachment

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

        if isinstance(attr_obj, Attachment):
            attr_obj._get_filepath()
        elif hasattr(attr_obj, "refresh_attachments"):
            attr_obj.refresh_attachments()

        methods = ((_add_comments_to_parent(name), "add_comments"),
                (_clear_comments_from_parent(name), "clear_comments"))
        
        attr_obj._reserved = ['ext'] if not hasattr(attr_obj,"_reserved") else attr_obj._reserved
        for method, method_name in methods:
            attr_obj._reserved.append(method_name)
            bound = method.__get__(attr_obj, type(attr_obj))
            setattr(attr_obj, method_name, bound)

        self._props_changed = True
        
    
    def add_comments(self, *comments):
        """
        Default behavior to be overwritten when attached to a parent block.
        
        If a `SingleBlock` is stored as an attribute of another `SingleBlock`,
        this method will be overwritten by the parent's `__setattr__`.
        """
        keys = list(self.get_req_validators())

        keys = [k for k in keys if k != "metadata"]
        fallback = [k for k in self._key_order if k != "metadata"]
        if not (keys or fallback):
            raise ValueError("This object has not been correctly attached to a parent block "
                             "and could not identify a required key to attach to.")

        first = keys[0] if keys else fallback[0]

        self._meta.comments.setdefault(first, [])
        for comment in comments:
            self._meta.comments[first].append(comment)
    
    def add_block(self, block_name:str, type_alias:str, value=[]):
        """
        Adds an unexpected attribute with a validator mapped by `type_alias`.
        Unexpected attributes not requiring a validator can be set directly
        without using this method.

        Args:
            block_name: new unexpected attribute name
            type_alias:
                Alias mapped to the desired validator in
                [`parsing.validation.aliases`][FoSpy.parsing.validation.aliases].
                For more information on how aliases are used, see
                [`__setattr__`][FoSpy.blocks.blocks.SingleBlock.__setattr__].
        """
        if hasattr(self,block_name):
            raise ValueError(f"This object already has attribute: '{block_name}'.")
        return setattr(self, f"{block_name}${type_alias}", value)
        
    def serialize(self, keepListType:bool=False, shallow:bool=False, clean:bool=False):
        """
        Return a recursively serialized `dict` representation of `self`.

        Fully serialized `SingleBlock`s are a single dict that can be passed to
        another constructor or emitted into lines for a FOS file. Serialized
        values at any nest level are either dicts, lists, or strings to allow
        full type-coersion when reconstructing or simplified emission when
        writing files.

        Serialized dict is deep copied to prevent object mutation.

        Args:
            keepListType:
                When True, maintains its current FOS printing mode (looped keys
                or explicit key:value lines), instead of explicit default

            shallow:
                When True, no recursive serialization occurs. Recommended when
                serialization is used only to inspect top-level keys.

            clean:
                When True, no FOS format read/write metadata is included in the
                serial. Recommended for sending output to other formats like
                JSON.

        Private attributes starting with "_" are either skipped or unpacked in
        special cases:

        * `_key_order`:
            attributes are added to the serialized dict in the order they
            appear in this list.

        * `_calc_comments`:
            calculated comments are attached to their mapped attribute after
            serialization to avoid mutation of object comments

        * `_calc_routines`:
            A list of functions scheduled to be called right before
            serialization to update _calc_comments. Scheduling calc routines
            ensures that their calculated values are up-to-date.

        * `_meta`:
            attributes of this container are given their own private `_key`s
            mapped by `FoSpy.parsing.syntax.meta_keys` in the serialized
            dict.

        * `_key_overrides`:
            per-instance override mapping that tracks which unexpected
            attributes require $alias suffixes.

        * `_aliases`:
            maps attribute names to alias tags used to emit $alias suffixed
            keys.

        * `_reserved`:
            attribute names in reserved are non-private attributes which
            should *not* be serialized. This usually applies to the `ext`
            attribute or methods attached after construction.
        """
        from copy import deepcopy
        from ..parsing.format_fos import format_calc_comment
        from .template import TemplateBlock

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
            if isinstance(obj, SimpleWrapper):
                obj = obj()
            serialize = getattr(obj, "serialize", None)
            if callable(serialize) and not shallow:
                return obj.serialize(clean=clean)
            if isinstance(obj, list):
                return [try_serial(item) for item in obj]
            if isinstance(obj, dict):
                return {k:try_serial(v) for k,v in obj.items()}
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
            except AttributeError:
                k = md[key]
            val = getattr(self._meta,attr,k)
            out[key] = val
        
        comments = {}
        for key, comment_list in out[mk["comments"]].items():
            comments[add_alias(key)] = comment_list
        out[mk["comments"]] = comments

        out = deepcopy(out)

        # _debug.pmsg(self._calc_comments)
        for key, comments in self._calc_comments.items():
            for comment in comments.values():
                out[mk["comments"]].setdefault(add_alias(key),[])
                out[mk["comments"]][add_alias(key)].append(format_calc_comment(comment))
        
        if not keepListType:
            out[mk["list_type"]] = "explicit"

        if "template_name" in out and not isinstance(self, TemplateBlock):
            out.pop("template_name")

        if clean:
            scan = out.copy()
            for key, val in scan.items():
                if key.startswith("_") or val is None:
                    out.pop(key)

        if not any(k for k in out.get("rename", {}) if not k.startswith("_")):
            out.pop("rename", None)

        return out
    
    def to_json(self, filepath=None, clean:bool=True, indent:int=4, **kwargs):
        """
        Converts `self` into a JSON-formatted string or file.

        [Serializes][FoSpy.blocks.blocks.SingleBlock.serialize] and either
        returns as a JSON-formatted string or saves to a JSON file.

        Args:
            filepath (pathlike):
                JSON file save destination. If `None`, returns JSON-formatted
                string instead.

            clean:
                When True, no FOS format read/write metadata is included in the
                serial. FOS metadata has no impact on JSON format but may be
                useful to view in JSON for troubleshooting.

            indent:
                `indent` value passed to `json.dump` for file saving.

            **kwargs (any):
                other arguments passed to `json.dump` for file saving.
        """
        import json
        serial = self.serialize(clean=clean)

        if filepath is None:
            return json.dumps(serial)
        
        with open(filepath, "w") as f:
            json.dump(serial, f, indent=indent, **kwargs)
    
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
                above their attached attributes in FOS format.
            comment:
                comment text without comment formatting (don't include // or !)
            calc_id:
                unique identifier for the calculated comment. If it matches an
                existing comment (like when refreshing a value), the comment is
                overwritten

        """
        calc_comments = self._calc_comments.get(key, {})
        self._calc_comments[key] = calc_comments
        self._calc_comments[key][calc_id]=comment

    def make_template(self,template_name:str,*args:str):
        """
        Converts `self` into a template of its original subclass.

        Returns a copy of `self` as a template of its original subclass, with
        specified fields replaced with template types. See
        [`TemplateClass`][FoSpy.blocks.blocks.SingleBlock.TemplateClass] for
        more information on template generation.

        Args:
            template_name: All templates require an identifying name.
            *args: properties to clear and replace with template types.
        """

        from ..parsing.format_fos import format_field

        serial = self.serialize(keepListType=True)
        validators = self.get_validators()
        for key in args:
            val = validators.get(key, None)
            if isinstance(val,type) and (issubclass(val, SingleBlock) or issubclass(val, ListBlock)):
                serial[key] = []
            else:
                serial[key] = format_field("template")
        serial["template_name"] = template_name
        return type(self).TemplateClass(*args).dispatch_subclass(serial)

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
        Schedules a calculated comment.

        Appends a
        [`_calc_routine()`][FoSpy.blocks._blockUtils._calc_routine]-decorated
        function to `self._calc_routines` to be run at
        [serialization][FoSpy.blocks.blocks.SingleBlock.serialize].

        Used to add calculated comments that should be refreshed during
        serialization.

        Args:
            path:
                a relative path string that can be resolved into a
                `_calc_routine()`-decorated function
            **kwargs (any):
                optional key word arguments to be passed to the function at
                path.

        Raises:
            TypeError:
                the attr or method at path is not registered as a
                _calc_routine

        Example:
        ```
            mySyn.add_calc_routine("materials.add_weight_pcts", typ="reagent")
            ## mySyn.materials.add_weight_pcts(typ="reagent") is now scheduled
            ## to run at serialization
        ```
        """

        func = self._resolve_relative_path(path)
        if not getattr(func, "_is_calc_routine", False):
            raise TypeError(f"'{path}' is not a registered calc routine.")

        self._meta.routine_paths.append(path)

        def wrapped(f=func, k=kwargs):
            return f(**k)

        self._calc_routines.append(wrapped)

    def list_avail_routines(self, recursive:bool=False, prefix:str="", abbreviated:bool=False):
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

        Returns:
            routines (list): 
                list of strings describing _calc_routine-decorated methods.
                Non-abbreviated calc routine strings can be passed directly to
                `self.add_calc_routine()`

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
    
    def add_all_calc_routines(self, recursive:bool=False):
        """
        Schedule all available calculation routines.

        Adds all available calc_routines to `self._calc_routines` using
        [`list_avail_routines()`][FoSpy.blocks.blocks.SingleBlock.list_avail_routines]
        and
        [`add_calc_routine()`][FoSpy.blocks.blocks.SingleBlock.add_calc_routine].
        
        Args:
            recursive:
                Optional recursion. See `SingleBlock.list_avail_routines()`
        """
        for path in self.list_avail_routines(recursive=recursive, abbreviated=False):
            self.add_calc_routine(path)

    def copy(self):
        """
        Returns a deep-copy of `self` by serializing and reconstructing.
        
        _calc_comments are not preserved during copy, but _calc_routines are.
        This prevents mutation of the comments when reconstructing.
        """
        cls = type(self)
        c_cmts = self._calc_comments.copy()
        self._calc_comments = {}

        new_obj =  cls.dispatch_subclass(self.serialize(keepListType=True))
        self._calc_comments = c_cmts

        return new_obj
    
    def _meta_to_front(self):
        """
        Moves metadata to the front of `_key_order`. Metadata will always be
        serialized first, but being elsewhere in the order leads to unexpected
        results when moving other keys to desired indices.
        """
        try:
            meta_idx =self._key_order.index("metadata")
            self._key_order.pop(meta_idx)
        # TODO: Better handling
        except Exception:
            pass
        self._key_order.insert(0,"metadata")
    
    def keys_to_front(self,*args):
        """
        Reorder attributes for serialization.

        Move any attribute names in `*args` to the front of _key_order to be
        serialized first. Order within `*args` is maintained in result.
        """
        try:
            meta_idx = args.index("metadata")
            args.pop(meta_idx)
        # TODO: Better handling
        except Exception:
            pass
        
        new_order = []
        for key in args:
            new_order.append(key)
        for key in self._key_order:
            if key not in new_order:
                new_order.append(key)
        self._key_order = new_order
        self._meta_to_front()

    def default_key_order(self, deep:bool=False):
        """
        Set to default attribute order for serialization.

        Rearrange attribute order to the default order assigned by
        [`build_validators`][FoSpy.blocks.blocks.SingleBlock.build_validators]

        Args:
            deep:
                When true, recursively calls `default_key_order` on any other
                `SingleBlock` objects stored in attributes.
        """
        new_order = []
        for key in self.get_validators():
            if key != "ext" and key in self.serialize(shallow=True):
                new_order.append(key)
        for key in self._key_order:
            if key not in new_order:
                new_order.append(key)
        self._key_order = new_order
        self._meta_to_front()

        if deep:
            for name, obj in self.__dict__.items():
                if not name.startswith("_") and hasattr(obj, "default_key_order"):
                    obj.default_key_order(deep=True)

    def keys_to_end(self, *args):
        """
        Reorder attributes for serialization.

        Move any attribute names in `*args` to the end of _key_order to be
        serialized last. Order within `*args` is maintained in result.
        """
        def remove_alias(key):
            return key.split("$")[0] if "$" in key else key
        for key in self.serialize(shallow=True):
            if not key.startswith("_") and remove_alias(key) not in self._key_order:
                self._key_order.append(remove_alias(key))
        for key in args:
            try:
                idx = self._key_order.index(key)
                self._key_order.pop(idx)
            # TODO: Better handling
            except Exception:
                pass
            self._key_order.append(key)
        self._meta_to_front()
        
    def key_to_idx(self, key:str, idx:int):
        """
        Reorder attributes for serialization.

        Move any attribute name to a specific index in `_key_order` for
        serialization order. The invisible `"metadata"` key is always refreshed
        to the front of the list, so indices are effectively 1-based.

        Args:
            key: name of attribute to reorder
            idx: new index in _key_order
        """
        self._meta_to_front()
        try:
            old_idx = self._key_order.index(key)
            self._key_order.pop(old_idx)
        # TODO: Better handling
        except Exception:
            pass
        self._key_order.insert(idx, key)

    def clear_comments(self):
        """
        Clear comments attached to top-level attributes only.
        """
        self._meta.comments = {}
        
    def rename_block(self, old, new):
        validators = self.get_validators()
        req = self.get_req_validators()
        if any(name.startswith("_") for name in (old, new)):
            raise ValueError("You cannot set private attributes (starting with '_') using obj.rename_block()")
        
        if old in req and new in validators:
            raise ValueError(f"You cannot rename '{old}' to '{new}'. '{old}' is a required property that "
                                f"can only be renamed to an unregistered key; '{new}' is already registered "
                                "as an expected property.")
        
        if hasattr(self, new):
            raise ValueError(f"'{new}' is already a property for this object, you cannot overwrite it with "
                             "obj.rename_block()")
        
        if "rename" in (old, new):
            raise ValueError("obj.rename property cannot be set or changed by obj.rename_block()")
        
        if hasattr(self, "rename") and hasattr(self.rename, old):
            old = getattr(self.rename, old)()

        if old in self._key_overrides:
            val = self._key_overrides.pop(old)
            self._key_overrides[new] = val

        else:
            if not hasattr(self,"rename"):
                self.rename = {}

            rename_dict = self.rename_dict()
            rename_from = {v:k for k,v in rename_dict.items()}
            if old in rename_from:
                base = rename_from[old]
            else:
                base = old

            _debug.msg(f"Registering '{base}':'{new}' into rename block")
            setattr(self.rename, base, new)
        _debug.msg(f"Moving '{old}' over to '{new}'.")
        setattr(self,new,getattr(self, old))
        delattr(self,old)
            
        try:
            idx = self._key_order.index(old)
            self._key_order[idx] = new
        # TODO: Better handling
        except Exception:
            self._key_order.append(new)

    def __delattr__(self, attr):
        if attr in self.get_req_validators():
            raise AttributeError(f"Cannot delete property: '{attr}'. It is registered as a required property for this object.")
        return super().__delattr__(attr)
    
    def clear_all_comments(self):
        self._meta.comments = {}
        for attr, val in self.__dict__.items():
            if attr.startswith("_") or attr in self._reserved:
                continue
            if hasattr(val, "clear_all_comments"):
                val.clear_all_comments()

    def refresh_attachments(self, new_copy=None, overwrite=None, **kwargs):
        from .attachments import Attachment

        if new_copy is None:
            new_copy = self._att_new_copy
        if overwrite is None:
            overwrite = self._att_overwrite

        for propDict in self.__dict__, self.ext.__dict__:
            for key, val in propDict.items():
                if key.startswith("_") or key in self._reserved:
                    continue
                if hasattr(val, "refresh_attachments"):
                    val.refresh_attachments(new_copy=new_copy, overwrite=overwrite, **kwargs)
                elif isinstance(val, Attachment) and hasattr(val, "refresh"):
                    val.refresh(new_copy=new_copy, overwrite=overwrite, **kwargs)

    def find_attachments(self):
        attachments = []
        for propVal in self.get_prop_dict().values():
            if isinstance(propVal, ListBlock):
                for obj in propVal._objs:
                    attachments.extend([
                        o for o in obj.find_attachments()
                        if o not in attachments
                    ])
            elif isinstance(propVal, SingleBlock):
                attachments.extend([
                    o for o in propVal.find_attachments()
                    if o not in attachments
                ])
        return attachments

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
    ```python
    MaterialList(ListBlock) # Contains Material(SingleBlock) objects
    TreamentList(ListBlock) # Contains Treatment(SingleBlock) objects
    ```
    """
    _reqCls: type[SingleBlock] = None
    def __init__(self, blockList:list):
        """
        Constructs a `ListBlock` from a list of objects or serialized dictionaries.

        Each item in blockList is checked against the `SingleBlock` subclass
        specified for the `ListBlock` subclass. If the item is not the correct
        subclass, it is passed to the `SingleBlock` subclass's
        `dispatch_subclass` method for coersion.

        Args:
            blockList:
                A list containing either `dicts` or `SingleBlock` objects (Mixing
                is allowed).
        Raises:
            TypeError:
                `ListBlock` instances can only be constructed from subclasses with an assigned _reqCls, not the parent `ListBlock` class.
        """
        #self._objs = []
        if not (isinstance(self._reqCls, type) and issubclass(self._reqCls, SingleBlock)):
            raise TypeError(f"ListBlock instances can only be constructed from subclasses with an assigned _reqCls. {self.__class__} has no _reqCls.")
        self.track_attachments(**cfg.track_attachments())
        if not isinstance(blockList, list):
            blockList = [blockList]
        self._objs = blockList
        self._staged_templates = {}

        
        # for blockDict in blockList:
        #     obj = self._reqCls.dispatch_subclass(blockDict)
        #     obj._parent_block = self
        #     self._objs.append(obj)
    
    
    @classmethod
    def Simple(cls, reqCls=SingleBlock):
        """
        Creates a simple subclass of `ListBlock`

        Creates a subclass of `ListBlock` that only accepts objects of the
        specified `SingleBlock` subclass.

        Simple ListBlocks are used when no specialized methods or attributes are
        needed.

        Args:
            reqCls:
                The subclass of `SingleBlock` that this `ListBlock` subclass
                accepts.
        """
        from .._docs.properties import _validator_rules
        from ._blockUtils import _get_docs_link

        if not issubclass(reqCls, SingleBlock):
            raise TypeError("reqCls must be a subclass of SingleBlock")
        if cls._reqCls is not None:
            raise TypeError("You cannot create a simple subclass of another ListBlock subclass.")

        link = _get_docs_link(reqCls)

        @_validator_rules(
            f"A [simple `ListBlock`](#listblock-and-simple-lists) of [`{reqCls.__name__}` objects.]{link}"
        )
        class SimpleSub(cls):
            _reqCls = reqCls

        name = f"{reqCls.__name__}List"
        qualname = f"{cls.__name__}.Simple.{name}"
        module = reqCls.__module__

        SimpleSub.__name__ = name
        SimpleSub.__qualname__ = qualname
        SimpleSub.__module__ = module

        return SimpleSub


    def __setattr__(self, name, value):
        """
        Only private attributes starting with "_" can be set.
        
        Items in self._objs can be edited/replaced individually by indexing with
        self[i], or self._objs can be replaced with a new list, which is
        re-validated and coerced to the correct `SingleBlock` subclass specified
        by _reqCls

        Args:
            name:
                The name of the attribute to set.
            value:
                The value to set the attribute to.
        Raises:
            AttributeError:
                Only private attributes starting with "_" can be set.
            TypeError:
                self._objs must be a list of objects which can be coerced to the
                correct `SingleBlock` subclass specified by _reqCls
        """
        from .attachments import Attachment
        from ._blockUtils import _unwrap_listblock

        if name == "_objs":


            if hasattr(self, "_reqCls"):
                errors = []
                typ = self._reqCls
                value = _unwrap_listblock(value, typ=typ)
                new_list = []
                for idx, obj in enumerate(value):
                    if isinstance(obj, dict) and obj == {}:
                        continue
                    if not isinstance(obj, typ):
                        try:
                            new_obj = typ.dispatch_subclass(obj)
                        except Exception as e:
                            errors.append(err.ListBlockMismatchError(self, obj, idx, cause=e))
                            continue  
                        if isinstance(obj, Attachment) and hasattr(obj, "_filepath"):
                            new_obj._filepath = obj._filepath
                        obj=new_obj
                    obj._parent_block = self
                    if hasattr(obj, "refresh") and isinstance(obj, Attachment):
                        obj.refresh(new_copy=self._att_new_copy, overwrite=self._att_overwrite)
                    new_list.append(obj)
                if errors:
                    raise err.ListBlockErrorGroup(self, errors)
                return super().__setattr__(name, new_list)

        elif name.startswith("_") or name in self._reserved:
            return super().__setattr__(name,value)
        else:
            raise AttributeError(
                f"{type(self).__name__} does not allow setting attribute '{name}'. "
                f"Only private names starting with '_' can be used. "
                f"Each list item is an item in {type(self).__name__}._objs which can be edited individually, "
                f"Or you can replace {type(self).__name__}._objs with a new list of objects."
            )

    def has_staged(self):
        return len(self._staged_templates) > 0 or any(blk.has_staged() for blk in self)
    
    def stage_template(self, temp_id, template:Block|dict=None):
        from .template import TemplateBlock
        if template is None:
            template = {}

        if "$" in temp_id:
            raise ValueError("ListBlock Template IDs cannot contain '$'. "
                             "The block type must match the required class for the ListBlock.")

        if not isinstance(template, (TemplateBlock, dict)):
            raise ValueError("Template must be a TemplateBlock or dictionary.")
        
        if isinstance(template, dict):
            template = self._reqCls.reflex(serialize=False,**template)
            template.template_name = temp_id
        elif not isinstance(template, self._reqCls):
            raise ValueError("Template must be a TemplateBlock subclass of the same type as this ListBlock.")
        
        if temp_id in self._staged_templates:
            raise ValueError(f"A Template has already been staged for {temp_id}.")
        
        template._staged_parent = self
        self._staged_templates[temp_id] = template

        return temp_id, template
    
    def fill_staged_template(self, temp_id, idx=None, **kwargs):
        template = self._staged_templates.pop(temp_id, None)
        if template is None:
            temp_id, _ = self.stage_template(temp_id)
            return self.fill_staged_template(temp_id, **kwargs)
        
        try:
            filled = template.fill(staged=True,**kwargs)
        except Exception:
            partial = template.fill(staged=True,incomplete=True, **kwargs)
            return self.stage_template(temp_id, partial)
        
        if idx is None:
            self.append(filled)
        else:
            self.insert(idx, filled)
        
        return temp_id, filled

    def block_to_idx(self, blk, idx):
        objs = self._objs.copy()
        current_idx = None
        if blk in objs:
            current_idx = objs.index(blk)
            if idx <= current_idx:
                current_idx += 1
        objs.insert(idx, blk)
        objs.pop(current_idx)
        self._objs = objs

    def order_up(self, blk):
        idx = self.get_idx(blk)
        if idx == 0:
            return
        self.block_to_idx(blk, idx-1)

    def order_down(self, blk):
        idx = self.get_idx(blk)
        if idx == len(self)-1:
            return
        self.block_to_idx(blk, idx+2)

    def get_idx(self, blk):
        try:
            return self._objs.index(blk)
        except ValueError:
            raise err.FoSpyStructureError(f"Block {blk} is not in {self}")

    def append(self, obj:SingleBlock):
        """
        Append a `SingleBlock`-coercable object to this `ListBlock`

        Appends the object to this `ListBlock`'s `_objs` list, and passes the
        entire list back to
        [`__setattr__`][FoSpy.blocks.blocks.ListBlock.__setattr__] for
        validation.

        Args:
            obj:
                The object to append
        """
        objs = self._objs.copy()
        objs.append(obj)
        self._objs = objs
    
    def insert(self, idx, obj:SingleBlock):
        """
        Insert a `SingleBlock`-coercable object into this `ListBlock`.

        Inserts the object into this `ListBlock`'s `_objs` list, and passes the
        entire list back to
        [`__setattr__`][FoSpy.blocks.blocks.ListBlock.__setattr__] for
        validation.

        Args:
            idx:
                The index to insert the object at
            obj:
                The object to insert
        """
        objs = self._objs.copy()
        objs.insert(idx,obj)
        self._objs = objs

    def remove_idx(self, from_idx:int=None, to_idx:int=None):
        """
        Remove a range of items from this `ListBlock`

        Removes a range of items from this `ListBlock`'s `_objs` list, and
        passes the entire list back to
        [`__setattr__`][FoSpy.blocks.blocks.ListBlock.__setattr__] for
        validation.

        `from_idx` is inclusive, and `to_idx` is non-inclusive. i.e., if
        `from_idx` is 0 and `to_idx` is 1, then the first item in the list will
        be removed, but not the second.

        If `from_idx` is None, then all items starting at and including `to_idx`
        will be removed. If `to_idx` is None, then all items up to and **not**
        including `from_idx` will be removed.

        Args:
            from_idx:
                The index of the first item to remove
            to_idx:
                The non-inclusive index to stop removing
        """
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

    def __getitem__(self, idx:int):
        """
        Get an item from this `ListBlock` by index.

        Args:
            idx:
                The index of the item
        """
        return self._objs[idx]
    
    def __setitem__(self, idx, val):
        """
        Set an item to this `ListBlock` by index.

        After setting, all items in this `ListBlock`'s `_objs` list are passed
        back to [`__setattr__`][FoSpy.blocks.blocks.ListBlock.__setattr__] for
        validation.

        Args:
            idx:
                The index of the item
            val:
                The new value for the item
        """
        new_objs = self._objs.copy()
        new_objs[idx] = val
        self._objs = new_objs
    
    def __len__(self):
        """
        Get the number of items in this `ListBlock`
        """
        return len(self._objs)
    
    def __iter__(self):
        """
        Iterate over the items in this `ListBlock`
        """
        return iter(self._objs)
    
    def __eq__(self, other, suppress_routine_paths=False):
        """
        Check equality of two `ListBlock` objects.
        
        Equality is checked by a deep difference of their serialized lists.
        
        Args:
            other:
                The other `ListBlock` object to check equality with
            suppress_routine_paths:
                Optional flag to still return true if the only differences found
                are in [calculation
                routine][FoSpy.blocks.blocks.SingleBlock.add_calc_routine]
                metadata. Calculation routines are for user information only and
                may not be relevant for equality.
        """
        from .._debug import deep_diff
        try:
            return len(deep_diff(self.serialize(), other.serialize(), suppress_routine_paths=suppress_routine_paths))==0
        except Exception:
            return False
        
    def __hash__(self):
        """
        Get the hash of this `ListBlock` object
        """
        return id(self)
    
    def set_list_type(self,typ="explicit"):
        """
        Set FOS list formatting (explicit or looped).

        Sets metadata for all items in this `ListBlock` to the specified type.

        List Types:
            - "explicit": Each object declares its own keys.
            - "looped": 
                Common keys are declared once at the beginning of a list. Each
                object specifies values for those keys in the declared order.
                Anomalous keys are still printed as key:value pairs.

        Args:
            typ:
                The type to set
        """
        if typ not in ("explicit", "looped"):
            raise ValueError("List type must be 'single' or 'looped'.")
        for obj in self:
            obj._meta.list_type = typ
        
    def serialize(self, clean=False, shallow=False, override_list_type:str|bool=None):
        """
        Serialize this `ListBlock` as a list of dictionaries.

        Overriding list type is only skipped when all objects in the list have
        the same list type. To prevent mutation, list type override is performed
        by calling
        [`set_list_type`][FoSpy.blocks.blocks.ListBlock.set_list_type] on a copy
        of this `ListBlock` and returning the serialized copy.

        `ListBlock`s of length one are always overridden to "explicit".

        List Types:
            - "explicit": Each object declares its own keys.
            - "looped": 
                Common keys are declared once at the beginning of a list. Each
                object specifies values for those keys in the declared order.
                Anomalous keys are still printed as key:value pairs.

        Args:
            clean:
                When True, no FOS format read/write metadata is included in the
                serial. Recommended for sending output to other formats like
                JSON.
            shallow:
                When True, no recursive serialization occurs. Recommended when
                serialization is used only to inspect top-level keys for object
                dictionaries.
            override_list_type:
                - When `None` (default): Checks for mixed list types and
                  recurses with override set to "explicit" if found.
                - When `False`: Does not override any list type. This should be
                  avoided for FOS-formatted output unless you know that all
                  objects in the list have the same list type.
                - When `str`: Copies this `ListBlock` and passes override to
                  [`copy.set_list_type`][FoSpy.blocks.blocks.ListBlock.set_list_type]
                  before returning the serialized copy
        """
        if override_list_type is None:
            for obj in self:
                if obj._meta.list_type == "explicit":
                    return self.serialize(clean=clean, shallow=shallow, override_list_type="explicit")
            return self.serialize(clean=clean, shallow=shallow, override_list_type="looped")
        elif not override_list_type:
            keepListType = len(self)>1
            lst = [obj.serialize(clean=clean, shallow=shallow, keepListType=keepListType) for obj in self]
            return lst
        else:
            copy = self.copy()
            copy.set_list_type(override_list_type)
            return copy.serialize(clean=clean, shallow=shallow, override_list_type=False)
    
     
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
        return cls(self.serialize(override_list_type=False))
    
    def remove_block(self, blk):
        if blk in self._objs:
            self._objs.remove(blk)

        if blk in self._staged_templates.values():
            temp_id = next(k for k,v in self._staged_templates.items() if v is blk)
            self._staged_templates.pop(temp_id)
            
    
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
    
    def clear_all_comments(self):
        for obj in self._objs:
            if hasattr(obj, "clear_all_comments"):
                obj.clear_all_comments()

    def default_key_order(self, deep=False):
        for obj in self._objs:
            if hasattr(obj, "default_key_order"):
                obj.default_key_order(deep=deep)

    def refresh_attachments(self, new_copy=None, overwrite=None, **kwargs):
        from .attachments import Attachment

        if new_copy is None:
            new_copy = self._att_new_copy
        if overwrite is None:
            overwrite = self._att_overwrite

        for val in self:
            if hasattr(val, "refresh_attachments"):
                val.refresh_attachments(new_copy=new_copy, overwrite=overwrite, **kwargs)
            if isinstance(val, Attachment) and hasattr(val, "refresh"):
                val.refresh(new_copy=new_copy, overwrite=overwrite, **kwargs)

