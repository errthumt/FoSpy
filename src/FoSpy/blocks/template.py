from .files import FileBlock

from .blocks import ListBlock, SingleBlock
from ._blockUtils import _get_docs_link
from .._docs.properties import _validator_rules

from ..blocks._containers import SimpleWrapper

from .._debug import Debug
_debug = Debug()

class TemplateField:
    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def serialize(cls,keepListType=None, clean=False):
        from ..parsing.format_fos import format_field
        return format_field("template")
    
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
    
    if name.endswith("ies") and name[:-3] == single[:-1]:
        return True
    
    return False

@FileBlock.register_dispatch("templates")
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
        
        registry = TemplateList.__dispatch__['registry']
        if reqCls not in registry:
            SimpleList = ListBlock.Simple(reqCls)

            link = _get_docs_link(reqCls)
            @SingleBlock.register_dispatch(reqCls, from_parent=TemplateList)
            @_validator_rules(
                f"A [simple `ListBlock`](#listblock-and-simple-lists) of flexible [`{reqCls.__name__}` *templates.*]{link}",
                ["[`FlexTemplate` subclasses](#flextemplate) are defined with a parent "
                "[`SingleBlock` subclass](#singleblock). They automatically detect "
                "which required properties are missing at construction time, and "
                "instantiate a [dynamic `TemplateBlock`](#templateblock) with template "
                "fields in those properties."]
            )
            class FlexList(TemplateList, SimpleList):
                pass

            FlexList.__name__ = f"{reqCls.__name__}FlexList"
            FlexList.__qualname__ = f"{cls.__name__}.{reqCls.__name__}FlexList"
            FlexList.__module__ = cls.__module__

        return {dispatch_key: reqCls}

    def __init__(self, blockList):
        super().__init__(blockList)

    def __iter__(self):
        full_list = self._objs.copy()

        full_list.extend(list(self._staged_templates.values()))

        return iter(full_list)

    def __setattr__(self, name, value):
        if not name == "_objs":
            return super().__setattr__(name, value)

        super().__setattr__(name, [])

        for block in value:
            self.append(block)

    def append(self, block):
        from .. import _errors as err
        from ._blockUtils import _unwrap_block
        try:
            super().append(block)
        except Exception:
            block = _unwrap_block(block)
            try:
                self.stage_template(template=block)
            except Exception as e:
                raise NotImplementedError("Shouldn't happen") from e


    def serialize(self, *args, **kwargs):
        cached_temps = self._staged_templates

        self._staged_templates = {}

        serial = super().serialize(*args, **kwargs).copy()

        for blk_dict, blk in zip(serial, self._objs):
            blk_dict["template_name"] = blk.get_id()

        self._staged_templates = cached_temps

        for blk in self._staged_templates.values():
            serial.append(blk.serialize(*args, **kwargs))

        return serial

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

        super().__init__(blockDict, **kwargs)

    def _override_validators(self, validators):
        from .blocks import Block
        try:
            rename_dict = self.rename_dict()
        except AttributeError:
            rename_dict = {}

        for field in self._fields:
            if field in rename_dict:
                field = rename_dict[field]

            if field not in validators:
                continue

            val = validators[field]
            if not isinstance(val, type) or not issubclass(val, Block):
                new_val = TemplateField

            elif issubclass(val, SingleBlock):
                new_val = val.TemplateClass()

            elif issubclass(val, ListBlock):
                new_val = TemplateList.Simple(val._reqCls)
            
            else:
                raise NotImplementedError("Shouldn't happen")

            validators[field] = new_val

        for field in self._val_exceptions:
            validators[field] = FailedTemplateField

        return validators


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
        if not self._full_class is not None and issubclass(self._full_class, SingleBlock):
            raise TypeError("A Template Block must be initialized from an existing class in order to be filled.")
        
        for prop in self._staged_templates:
            self.fill_staged_template(prop)
        
        staged_id = self.find_staged_id()
        if staged_id and not staged:
            _, filled = self._staged_parent.fill_staged_template(staged_id, **kwargs)
            return filled

        serial = self.serialize(keepListType=True)
        for kw, arg in kwargs.items():
            serial[kw] = arg

        flex_cls = self._full_class.TemplateClass()

        filled = flex_cls(serial)

        return filled
    
    def serialize(self,keepListType=False, shallow=False, clean=False, **kwargs):
        # from ..parsing.validation import required_keys
        # from ..parsing.format_fos import format_field
        required = self.get_req_validators()
        required.pop('ext',None)
        required.pop('template_name',None)
        serial = super().serialize(keepListType=keepListType, shallow=shallow, clean=clean)

        out = {"template_name":serial.pop("template_name","")}

        for key, staged in self._staged_templates.items():
            serial.setdefault(key, staged.serialize(keepListType=keepListType, shallow=shallow, clean=clean))

        for key,validator in required.items():
            val = None
            if isinstance(validator,type):
                if issubclass(validator,SingleBlock):
                    val = serial.pop(key, validator.reflex())
                elif issubclass(validator, ListBlock):
                    val = serial.pop(key, validator([]).serialize())

            if val is None:
                val = serial.pop(key, TemplateField("").serialize())

            out[key] = val
        
        for key, val in serial.items():
            out[key] = val

        return out
    
    def __setattr__(self, name, value):
        from .. import _errors as err
        from .blocks import Block

        try:
            super().__setattr__(name, value)
            self._val_exceptions.pop(name, None)
        except err.FailedValidatorError as e:
            validators = self.get_validators()

            cached_val = validators.get(name, None)

            if not isinstance(cached_val, type) or not issubclass(cached_val, Block):
                self._val_exceptions[name] = e
                # newly mutated _val_exceptions should allow setattr now.
                super().__setattr__(name, value)

            elif issubclass(cached_val, SingleBlock):
                self.stage_template(name, value)

            elif issubclass(cached_val, TemplateList):
                raise NotImplementedError("A TemplateList construction failed unexpectedly.")

            else: # ListBlock Only
                from ._blockUtils import _unwrap_listblock
                from warnings import warn
                setattr(self, name, [])

                value = _unwrap_listblock(value)

                new_listblock = getattr(self, name)

                warnings = []
                for item in value:
                    try:
                        new_listblock.append(item)
                    except err.FailedValidatorError as e:
                        try:
                            new_listblock.stage_template(template=item)
                        except Exception as e:
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
            return super().__new__(cls, blockDict, *args, _dispatched=True, **kwargs)

        full_class = cls._full_class
        blockDict = cls._inject_defaults(full_class, blockDict)
                
        template_class = full_class.TemplateClass(*cls._fields)

        for field in cls._fields:
            if blockDict.get(field, None) is None:
                blockDict[field] = TemplateField()

        blockDict.setdefault("template_name", cls.__name__)

        return template_class(blockDict, *args, _dispatched=True, **kwargs)

    
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
                pass

            suffix = "FlexTemplate" if not fields else "Template"

            TemplateClass.__name__ = f"{cls._full_class.__name__}{suffix}"
            TemplateClass.__qualname__ = f"{cls._full_class.__name__}{suffix}"
            TemplateClass.__module__ = cls.__module__

        return {dispatch_key: cls._fields or fields}
    
    def __new__(cls, blockDict, *args, **kwargs):
        if not hasattr(cls, "_fields"):
            raise Exception("FlexTemplate subclasses must be initialized using a SingleBlock's TemplateClass method.")
        
        if cls._fields != ():
            return super().__new__(cls, blockDict, *args, **kwargs)
        
        from .blocks import Block
        from .metadata import Rename
        from ._blockUtils import _template_found

        full_cls = cls._full_class
        temp_name = blockDict.pop("template_name", cls.__name__)
        try:
            return full_cls(blockDict, *args, **kwargs)
        except Exception:
            blockDict['template_name'] = temp_name

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
        rename_from = {v:k for k, v in rename_dict.items()}
        fields = []
        reqs = full_cls.build_req_validators()
        reqs.pop('ext', None)

        for name, validator in reqs.items():
            if name in rename_from:
                name = rename_from[name]

            if (
                _template_found(blockDict.get(name, None))
            ) or (
                isinstance(validator, type) and
                issubclass(validator, Block) and
                not issubclass(validator, Rename)
            ):
                fields.append(name)

        for prop, val in blockDict.items():
            if prop not in fields and _template_found(val):
                fields.append(prop)

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
