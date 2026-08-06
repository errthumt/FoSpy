from .._debug import Debug
from .._docs.properties import _validator_rules
from ..blocks._containers import SimpleWrapper
from ._blockUtils import _get_docs_link
from .blocks import ListBlock, SingleBlock
from .files import FileBlock

_debug = Debug()

class TemplateField:
    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def serialize(cls,**kwargs):
        from ..parsing.format_fos import format_field
        return format_field("template")

    def __str__(self):
        return self.serialize()
    
class FailedTemplateField(SimpleWrapper,TemplateField):
    def serialize(self, *args, **kwargs):
        return self._value

def _get_template_aliases():
    from .. import blocks as b
    template_aliases = {}
    for blk_name in b.__all__:

        blk = getattr(b, blk_name)

        blk_name = blk_name.lower()

        if "template" in blk_name or "meta" in blk_name or blk_name in (
            "rename"
        ):
            continue

        target = None
        if issubclass(blk, SingleBlock):
            if issubclass(blk, b.Attachment):
                target = ListBlock.Simple(blk)
            else:
                target = TemplateList.Simple(blk)
        elif issubclass(blk, ListBlock) and blk._reqCls is not None:
            if issubclass(blk._reqCls, b.Attachment):
                target = blk
            else:
                target = TemplateList.Simple(blk._reqCls)

        if target is not None:
            template_aliases[blk_name] = target
    return template_aliases

def _is_plural(name, single):
    """Not exhaustive, but good enough for now"""
    if not name.endswith("s"):
        return False

    if name[:-1] == single:
        return True
    
    if name.endswith("es") and name[:-2] == single:
        return True
    
    return bool(name.endswith("ies") and name[:-3] == single[:-1])

@FileBlock.register_dispatch("templates",defaults={"metadata":{"fos_type":"templates"}})
class TemplateSet(FileBlock):
    """
    Represents a set of templates loaded from a FOS file.

    FOS files may contain multiple different types of templates grouped into
    `TemplateList`s. Each of these lists is one attribute of a `TemplateSet`.
    """
    def __init__(self, blockDict, **kwargs):
        self._aliases = _get_template_aliases()
        super().__init__(blockDict, **kwargs)
    
    def __setattr__(self, name, value):
        if "$" in name:
            new_name, alias = name.split("$")
            if alias in self._aliases:
                return super().__setattr__(name, value)
            
            try:
                alias = next(a for a in self._aliases if _is_plural(alias, a))
                name = new_name + "$" + alias
            except StopIteration:
                pass
            return super().__setattr__(name, value)

        if name.startswith("_") or name in (
            "metadata",
            "ext",
            "rename"
        ):
            return super().__setattr__(name, value)

        if name in self._aliases:
            name = name + "s" + name
        else:
            try:
                alias = next(a for a in self._aliases if _is_plural(name, a))
                name = name + "$" + alias
            except StopIteration:
                pass

        return super().__setattr__(name, value)
    
    def serialize(self, *args, **kwargs):
        serial = super().serialize(*args, **kwargs)

        out = {}

        for name, value in serial.items():
            if "$" in name:
                new_name, alias = name.split("$")
                if _is_plural(new_name, alias):
                    name = new_name

            out[name] = value

        return out

@SingleBlock.setup_dispatch(from_key="_reqCls",allow_self=False)
class TemplateList(ListBlock):
    """
    Represents a list of templates with the same subclass.
    """

    @classmethod
    def add_dispatch(cls, blockDict, dispatch_key, **kwargs):
        _ = SingleBlock.add_dispatch(blockDict, dispatch_key, **kwargs)

        block_dispatch = blockDict.setdefault("__dispatch__", {})
        reqCls = block_dispatch.setdefault("_reqCls", cls._reqCls)

        if reqCls is None:
            return {}
        
        if getattr(reqCls, "_full_class", None) is not None:
            reqCls = reqCls._full_class
        
        registry = TemplateList.__dispatch__['registry']
        if reqCls not in registry:

            link = _get_docs_link(reqCls)
            @SingleBlock.register_dispatch(reqCls, from_parent=TemplateList)
            @_validator_rules(
                f"A [simple `ListBlock`](#listblock-and-simple-lists) of flexible [`{reqCls.__name__}` *templates.*]{link}",
                [("[`FlexTemplate` subclasses](#flextemplate) are defined with a parent "
                "[`SingleBlock` subclass](#singleblock). They automatically detect "
                "which required properties are missing at construction time, and "
                "instantiate a [dynamic `TemplateBlock`](#templateblock) with template "
                "fields in those properties.")]
            )
            class FlexList(TemplateList):
                _reqCls = reqCls.TemplateClass()

            FlexList.__name__ = f"{reqCls.__name__}FlexList"
            FlexList.__qualname__ = f"{cls.__name__}.{reqCls.__name__}FlexList"
            FlexList.__module__ = cls.__module__

        return {dispatch_key: reqCls}

    @classmethod
    def Simple(cls, reqCls, **kwargs):
        proxy_dict = {
            "__dispatch__": {
                "_reqCls": reqCls,
            }
        }

        return TemplateList.dispatch_subclass(proxy_dict)

@SingleBlock.setup_dispatch(from_key="_full_class", allow_self=False)
class TemplateBlock(SingleBlock):
    _id_key = "template_name"
    _full_class = None
    _fields = None
    def __init__(self, blockDict, **kwargs):
        self._val_exceptions = {}
        from ._blockUtils import _unwrap_block

        blockDict = _unwrap_block(blockDict)

        if isinstance(self, FileBlock):
            if "metadata" not in self._fields:
                new_fields = list(self._fields)
                new_fields.append("metadata")
                self._fields = tuple(new_fields)

            current_temp = blockDict.pop("template_name", None)
            metadata = blockDict.setdefault("metadata", {})
            temp_name = metadata.setdefault("template_name", current_temp or self.__class__.__name__)
            blockDict["template_name"] = temp_name
        
        super().__init__(blockDict, **kwargs)

    def _override_validators(self, validators):
        from .blocks import Block
        try:
            rename_dict = self.rename_dict()
        except AttributeError:
            rename_dict = {}

        for field in self._fields:
            field = rename_dict.get(field, field)

            if field not in validators:
                continue

            val = validators[field]
            if not (isinstance(val, type) and issubclass(val, Block)):
                new_val = TemplateField


                validators[field] = new_val

        for field in self._val_exceptions:
            validators[field] = FailedTemplateField

        return validators

    def try_singleblock(self, blk_cls, field_name, candidate):
        if isinstance(candidate, blk_cls) and not isinstance(candidate, TemplateBlock):
            return candidate
        if not isinstance(candidate, blk_cls):
            try:
                return blk_cls(candidate)
            except Exception:
                pass

        _, template = self.stage_template(field_name, candidate)

        return template

    def try_listblock(self, blk_cls, candidate):
        from ._blockUtils import _unwrap_listblock
        if isinstance(candidate, blk_cls) and not isinstance(candidate, TemplateList):
            return candidate
        if not isinstance(candidate, blk_cls):
            try:
                return blk_cls(candidate)
            except Exception:
                pass

        listblock = blk_cls([])
        candidate = _unwrap_listblock(candidate, blk_cls._reqCls)
        for item in candidate:
            try:
                listblock.append(item)
            except Exception:
                listblock.stage_template(template=item)

        return listblock

    def get_req_validators(self):
        validators = super().get_req_validators()

        return self._override_validators(validators)
    
    def get_validators(self):
        validators = super().get_validators()

        return self._override_validators(validators)

    def find_staged_id(self):
        if not (hasattr(self, "_staged_parent")
                and self._staged_parent.has_staged()):
            return False
        
        staged_dict = self._staged_parent._staged_templates
        staged_reversed = {v:k for k,v in staged_dict.items()}

        return staged_reversed.get(self, False)

    def fill(self,incomplete=False,staged=False,in_place=False,**kwargs):
        from .. import _errors as err

        if not self._full_class is not None and issubclass(self._full_class, SingleBlock):
            raise TypeError("A Template Block must be initialized from an existing class in order to be filled.")

        current_templates = list(self._staged_templates.keys())
        
        for prop in current_templates:
            self.fill_staged_template(prop)
        
        staged_id = self.find_staged_id()
        if staged_id and not staged:
            _, filled = self._staged_parent.fill_staged_template(staged_id, **kwargs)
            return filled

        serial = self.serialize(keepListType=True)
        for kw, arg in kwargs.items():
            serial[kw] = arg

        flex_cls = self._full_class.TemplateClass()
        temp_name = None
        try:
            if staged_id == "metadata" and isinstance(self._staged_parent, FileBlock) and self._staged_parent.has_staged():
                raise err.PropertyErrorGroup(self, serial, [
                    ValueError("A FileBlock's metadata template cannot be finalized until all other staged templates are filled.")
                ])

            temp_name = serial.pop("template_name", None)
            filled = self._full_class(serial)
        except err.MultiplePropertyErrors:

            if temp_name is not None:
                serial["template_name"] = temp_name
            filled = flex_cls(serial)

        filled.keys_to_front(*self._key_order)

        return filled
    
    def serialize(self,keepListType=False, shallow=False, clean=False, **kwargs):
        # from ..parsing.validation import required_keys
        # from ..parsing.format_fos import format_field
        required = self.get_req_validators()
        required.pop('ext',None)
        required.pop('template_name',None)
        serial = super().serialize(keepListType=keepListType, shallow=shallow, clean=clean, as_template=True)

        if shallow:
            return serial

        rename_dict = self.rename_dict()

        out = {"template_name":serial.pop("template_name","")}

        for key,validator in required.items():
            val = None
            key = rename_dict.get(key, key)
            if isinstance(validator,type):
                if issubclass(validator,SingleBlock):
                    val = serial.pop(key, validator.reflex())
                elif issubclass(validator, ListBlock):
                    val = serial.pop(key, validator([]).serialize())

            if val is None:
                val = serial.pop(key, TemplateField.serialize())

            out[key] = val
        
        for key, val in serial.items():
            out[key] = val

        if isinstance(self, FileBlock):
            metadata = getattr(self, "metadata", None)
            if metadata is None or isinstance(metadata, TemplateBlock):
                temp_name = out.pop("template_name", self.__class__.__name__)
                out["metadata"]["template_name"] = temp_name

        return out

    def __getattr__(self, name):
        if name in self._staged_templates:
            return self._staged_templates[name]
        return super().__getattr__(name)
    
    def __setattr__(self, name, value):
        from .. import _errors as err
        from .blocks import Block

        try:
            super().__setattr__(name, value)
            self._val_exceptions.pop(name, None)
        except err.FailedValidatorError as e:
            validators = self.get_validators()

            if "$" in name:
                prop_name = name.split("$")[0]
            else:
                prop_name = name

            cached_val = validators.get(prop_name, None)

            if not isinstance(cached_val, type) or not issubclass(cached_val, Block):
                self._val_exceptions[name] = e
                # newly mutated _val_exceptions should allow setattr now.
                super().__setattr__(name, value)

            elif issubclass(cached_val, SingleBlock):
                if isinstance(value, TemplateField) or value == TemplateField.serialize():
                    value = {}
                self.stage_template(name, value)

            elif issubclass(cached_val, TemplateList):
                raise NotImplementedError("A TemplateList construction failed unexpectedly.")

            else: # ListBlock Only
                from warnings import warn

                from ._blockUtils import _unwrap_listblock
                setattr(self, name, [])

                value = _unwrap_listblock(value)

                new_listblock = getattr(self, name)

                warnings = []
                for item in value:
                    try:
                        new_listblock.append(item)
                    except err.MultipleListBlockErrors as e:
                        try:
                            new_listblock.stage_template(template=item)
                        except Exception as e:  # noqa: BLE001
                            warnings.append("The following item could not be set to a ListBlock or staged as a template:"
                                            f"\n\nCANDIDATE:\n{item}"
                                            f"\n\nERROR:\n{e}")
                if warnings:
                    for w in warnings:
                        warn(w, UserWarning)
    
    @classmethod
    def TemplateClass(cls, *args):
        if None in (cls._full_class, cls._fields):
            raise TypeError("A new Template Block must be initialized from an existing class, or a Template of that class.")

        fields = list(cls._fields)

        fields.extend([a for a in args if a not in fields])
        
        return cls._full_class.TemplateClass(*fields)
    
    @classmethod
    def _inject_defaults(cls, full_class, blockDict):
        from .. import _errors as err

        full_dispatch = getattr(full_class, "__dispatch__", {})
        
        next_class = None
        while next_class is not full_class:
            if next_class is None:
                next_class = full_dispatch.get("dispatch_from", full_class)
            else:
                registry = next_class.__dispatch__["registry"]
                try:
                    next_class = next(sub for sub in registry.values() if issubclass(full_class, sub))
                except StopIteration:
                    err.BlockDispatchError(
                        f"Could not find a valid dispatch chain to get from {next_class.__name__} to "
                        f"{full_class.__name__}.")
                    
            blockDict = next_class.inject_defaults(blockDict)


        return blockDict
    
    def __new__(cls, blockDict, *args, **kwargs):
        from .. import _errors as err

        if None in (cls._fields, cls._full_class):
            raise err.BlockDispatchError("A Template Block must be initialized from an existing class, or a Template of that class.")
        
        dispatched = kwargs.pop("_dispatched", False)
        if dispatched:
            blockDict.setdefault("template_name", cls.__name__)
            return super().__new__(cls, blockDict, *args, _dispatched=True, **kwargs)

        full_class = cls._full_class
        blockDict = cls._inject_defaults(full_class, blockDict)
                
        template_class = full_class.TemplateClass(*cls._fields)

        rename_dict = blockDict.get("rename", {})
        if isinstance(rename_dict, list):
            rename_dict = rename_dict[0]

        for field in cls._fields:
            field = rename_dict.get(field, field)
            if blockDict.get(field, None) is None:
                blockDict[field] = TemplateField()


        return template_class(blockDict, *args, _dispatched=True, **kwargs)

    def add_field(self, prop_name, value=None):
        from .blocks import Block, SingleBlock, ListBlock

        validators = self.get_validators()
        cached_val = validators.get(prop_name, None)

        value = value or getattr(self, prop_name, None)
        if value is None:
            if not isinstance(cached_val, type) or not issubclass(cached_val, Block):
                value = TemplateField.serialize()
            elif issubclass(cached_val, SingleBlock):
                value = {}
            else:
                # elif issubclass(cached_val, ListBlock):
                value = []

        elif prop_name not in validators:
            setattr(self, prop_name, value)
            return self

        elif isinstance(value, Block):
            value = value.serialize()

        if isinstance(value, dict):
            value.setdefault("template_name", prop_name)

        if prop_name in self._fields or prop_name not in validators:
            setattr(self, prop_name, value)
            return self

        serial = self.serialize()
        serial[prop_name] = value

        new_template = self.TemplateClass(prop_name)(serial)

        if getattr(self, "_parent_block", getattr(self, "_staged_parent", None)) is None:
            return new_template

        if getattr(self, "_staged_parent", None) is not None:
            prop_name = next(k for k, v in self._staged_parent._staged_templates.items() if v is self)
            _, new_template = self._staged_parent.stage_template(prop_name, template=new_template, replace=True)
            return new_template

        parent_blk = self._parent_block

        if isinstance(parent_blk, ListBlock):
            _, new_template = parent_blk.stage_template(template=new_template)
            return new_template
        
        parent_prop = self.get_parent_prop()

        new_parent = parent_blk.add_field(parent_prop, value=new_template)
        return getattr(new_parent, parent_prop)

    def add_fields(self, *empty_fields, **set_fields):
        if any(field in set_fields for field in empty_fields):
            raise ValueError("A new field cannot be both empty and set in the same call.")

        all_fields = {field: None for field in empty_fields}
        all_fields.update(set_fields)

        current_template = self

        for field, value in all_fields.items():
            current_template = current_template.add_field(field, value=value)

        return current_template

    def stage_template(self, prop_name, template=None):
        cached_value = getattr(self, prop_name, None)
        if cached_value is not None:
            try:
                super(SingleBlock, self).__delattr__(prop_name)
            except AttributeError:
                self._staged_templates.pop(prop_name)

        try:
            return super().stage_template(prop_name, template=template)
        except Exception:
            setattr(self, prop_name, cached_value)
            raise

    def is_staged(self):
        if getattr(self, "_staged_parent", None) is None:
            return False

        try:
            return any(v is self for k, v in self._staged_parent._staged_templates.items())
        except StopIteration:
            return False

    def get_staged_id(self):
        if not self.is_staged():
            return None

        return next(k for k, v in self._staged_parent._staged_templates.items() if v is self)

    def find_fileblock(self):
        from .. import _errors as err

        try:
            return super().find_fileblock()
        except err.FileBlockNotFoundError:
            if not self.is_staged():
                raise

        try:
            return self._staged_parent.find_fileblock()
        except err.FileBlockNotFoundError as e:
            raise err.FileBlockNotFoundError("Could not find FileBlock containing this object's staged parent.") from e

    
class FlexTemplate:
    @classmethod
    def add_dispatch(cls, blockDict, dispatch_key, **kwargs):
        _ = SingleBlock.add_dispatch(blockDict, dispatch_key, **kwargs)

        registry = cls.__dispatch__["registry"]

        block_dispatch = blockDict.setdefault("__dispatch__", {})
        fields = block_dispatch.setdefault("_fields", ())

        if fields not in registry:

            @cls.register_dispatch(fields)
            class TemplateClass(TemplateFieldCounter,cls):
                _fields = fields

            suffix = "FlexTemplate" if not fields else "Template"

            TemplateClass.__name__ = f"{cls._full_class.__name__}{suffix}"
            TemplateClass.__qualname__ = f"{cls._full_class.__name__}{suffix}"
            TemplateClass.__module__ = cls.__module__

        return {dispatch_key: cls._fields or fields}
    
    def __new__(cls, blockDict, *args, **kwargs):
        if not hasattr(cls, "_fields"):
            raise Exception("FlexTemplate subclasses must be initialized using a SingleBlock's TemplateClass method.")  # noqa: TRY002
        
        if cls._fields != ():
            return super().__new__(cls, blockDict, *args, **kwargs)
        
        from ._blockUtils import _template_found
        from .blocks import Block
        from .metadata import Rename

        full_cls = cls._full_class

        # jump back to start of dispatch chain.
        dispatch = getattr(full_cls, "__dispatch__", None) or {}

        dispatch_start = dispatch.get("dispatch_from", full_cls)

        # continuously inject until chain tops out.
        next_cls = None
        while next_cls is not full_cls:
            next_cls = next_cls or dispatch_start
            blockDict = cls._inject_defaults(next_cls, blockDict)

            full_cls, next_cls = next_cls, full_cls.dispatch_subclass(blockDict, for_template=True)
            blockDict.pop("__dispatch__", None)

        rename_dict = blockDict.get("rename", {})
        if isinstance(rename_dict, list):
            rename_dict = rename_dict[0]

        rename_from = {v:k for k, v in rename_dict.items() if not k.startswith("_")}
        fields = []
        reqs = full_cls.build_req_validators()
        reqs.pop('ext', None)

        for name, validator in reqs.items():
            block_name = rename_dict.get(name, name)

            if (
                _template_found(blockDict.get(block_name, None))
            ) or (
                isinstance(validator, type) and
                issubclass(validator, Block) and
                not issubclass(validator, Rename)
            ):
                fields.append(name)

        for prop, val in blockDict.items():
            alias = False
            if "$" in prop:
                alias = True
                prop = prop.split("$")[0]

            if prop not in fields and (alias or _template_found(val)):
                fields.append(prop)

        try:
            idx = fields.index("template_name")
            fields.pop(idx)
        except ValueError:
            pass

        if not fields:
            return super().__new__(cls, blockDict, *args, _dispatched=True, **kwargs)

        return full_cls.TemplateClass(*fields)(blockDict, *args, **kwargs)
    
class TemplateFieldCounter:
    _fields = ()
    @classmethod
    def add_dispatch(cls, blockDict, dispatch_key, **kwargs):
        _ = SingleBlock.add_dispatch(blockDict, dispatch_key, **kwargs)

        return {dispatch_key: cls._fields}







# class FlexTemplate(SingleBlock):
#     _baseReq = None
#     @classmethod
#     def reflexor(cls, subcls):
#         if getattr(subcls, "_full_class", None) is not None:
#             subcls = subcls._full_class

#         # First recursion:
#         #   - calls TemplateClass(*()) to initialize locator and base
#         #   - after initializing locator and base,
#         #       TemplateClass calls reflexor to promote base to reflexor
#         # Second recursion (called by TemplateClass(*())):
#         #    calls TemplateClass again, which now returns the cached base
#         BaseTemplateClass = subcls.TemplateClass()

#         # First Recursion:
#         #    Reflexor was already cached by second recursion, return it
#         if issubclass(BaseTemplateClass, FlexTemplate):
#             return BaseTemplateClass
        
#         # Second Recursion:
#         #    Replace cached base with new reflexor subclass

#         TemplateLocator = TemplateBlock.dispatch[subcls]
        
#         @TemplateLocator.set_dispatch(())
#         class Reflexor(FlexTemplate, BaseTemplateClass):
#             _baseReq = subcls

#         mro = Reflexor.__mro__


#         Reflexor.__name__ = f"Flex{subcls.__name__}"
#         Reflexor.__qualname__ = f"{cls.__name__}.reflexor.Flex{subcls.__name__}"
#         Reflexor.__module__ = cls.__module__

#         from ..parsing.validation import optional_keys, required_keys

#         old_reqs = Reflexor.build_req_validators()
#         req_vals = {k:False for k in old_reqs}
#         req_vals.pop('ext', None)

#         required_keys[Reflexor] = req_vals
#         Reflexor.req_overrides = req_vals
#         optional_keys.setdefault(Reflexor, {}).update(old_reqs)

#         return Reflexor
    
#     @classmethod
#     def reflex(cls):
#         return cls._baseReq.reflex()
