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

class TemplateList(ListBlock):
    """
    Represents a list of templates with the same subclass.
    """
    simple_lists = {}

    @staticmethod
    def temp_id_gen():
        i = 0
        while True:
            yield "template_" + str(i)
            i += 1

    def __init__(self, blockList):
        super().__init__([])
        self._temp_id_gen = TemplateList.temp_id_gen()

        if not isinstance(blockList, list):
            blockList = [blockList]

        for block in blockList:
            self.append(block)

    def append(self, block):
        from .. import _errors as err
        from ._blockUtils import _unwrap_block
        try:
            super().append(block)
        except Exception:
            block = _unwrap_block(block)
            try:
                self.stage_template(next(self._temp_id_gen), block)
            except Exception as e:
                raise NotImplementedError("Shouldn't happen") from e


    def serialize(self, *args, override_list_type=None,**kwargs):
        serial = super().serialize(*args, override_list_type=override_list_type, **kwargs).copy()

        if not override_list_type:
            for blk in self._staged_templates.values():
                serial.append(blk.serialize(*args, **kwargs))

        return serial

    @classmethod
    def Simple(cls, reqCls, **kwargs):
        if reqCls in cls.simple_lists:
            return cls.simple_lists[reqCls]
        
        SimpleList = ListBlock.Simple(reqCls)

        link = _get_docs_link(reqCls)

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

        cls.simple_lists[reqCls] = FlexList

        return FlexList

@SingleBlock.setup_dispatch(from_key="_full_class", allow_self=False)
class TemplateBlock(SingleBlock):
    _id_key = "template_name"
    _full_class = None
    _fields = None
    def __init__(self, blockDict, **kwargs):
        self._val_exceptions = {}

        super().__init__(blockDict, **kwargs)

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
        
        if not incomplete and self.has_staged():
            raise ValueError("A template cannot be filled to a full block with staged templates.")
        
        if in_place:
            for kw, arg in kwargs.items():
                setattr(self,kw,arg)
            return self
        
        staged_id = self.find_staged_id()
        if staged_id and not staged:
            return self._staged_parent.fill_staged_template(staged_id, **kwargs)

        serial = self.serialize(keepListType=True)
        serial.pop("template_name",None)
        for kw, arg in kwargs.items():
            serial[kw] = arg

        if incomplete:
            new_template = self._full_class.reflex(serialize=False,**serial)
            new_template.template_name = self.template_name
            for temp_id, template in self._staged_templates.items():
                new_template.stage_template(temp_id, template)
            return new_template

        return self._full_class(serial)
    
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
                    val = serial.pop(key, validator([]).serialize(keepListType=keepListType, shallow=shallow, clean=clean))

            if val is None:
                val = serial.pop(key, TemplateField("").serialize())

            out[key] = val
        
        for key, val in serial.items():
            out[key] = val

        return out
    
    def __setattr__(self, name, value):
        from .. import _errors as err
        from ..parsing.validation import optional_keys

        try:
            super().__setattr__(name, value)
            self._val_exceptions.pop(name, None)
        except err.FailedValidatorError as e:
            from ..parsing.validation import optional_keys
            self._val_exceptions[name] = e

            validators = optional_keys.setdefault(type(self), {})
            cached_val = validators.get(name, None)

            if isinstance(cached_val, type) and issubclass(cached_val, SingleBlock):
                self.stage_template(name, value)

            elif isinstance(cached_val, type) and issubclass(cached_val, ListBlock):
                raise NotImplementedError("A TemplateList failed construction unexpectedly.") from e
            
            else:
                validators[name] = FailedTemplateField
                super().__setattr__(name, value)
                if cached_val is not None:
                    validators[name] = cached_val
                else:
                    validators.pop(name, None)
    
    @classmethod
    def TemplateClass(cls, *args):
        if None in (cls._full_class, cls._fields):
            raise TypeError("A new Template Block must be initialized from an existing class, or a Template of that class.")

        fields = list(cls._fields)

        fields.extend([a for a in args if a not in fields])
        
        return cls._full_class.TemplateClass(*fields)
    
    def __new__(cls, blockDict, *args, **kwargs):
        from .. import _errors as err

        if None in (cls._fields, cls._full_class):
            raise err.BlockDispatchError("A Template Block must be initialized from an existing class, or a Template of that class.")
        
        dispatched = kwargs.pop("_dispatched", False)
        if dispatched:
            return super().__new__(cls, blockDict, *args, _dispatched=True, **kwargs)

        full_class = cls._full_class

        full_dispatch = getattr(full_class, "__dispatch__", {})
        
        next_class = full_dispatch.get("dispatch_from", full_class)

        while next_class is not full_class:
            blockDict = next_class.inject_defaults(blockDict)
            registry = next_class.__dispatch__["registry"]

            try:
                next_class = next(sub for sub in registry.values() if issubclass(full_class, sub))
            except StopIteration:
                err.BlockDispatchError(
                    f"Could not find a valid dispatch chain to get from {next_class.__name__} to "
                    f"{full_class.__name__}.")
                
        template_class = next_class.TemplateClass(*cls._fields)

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

        return {dispatch_key: cls._fields}
    
    def __new__(cls, blockDict, *args, **kwargs):
        if not hasattr(cls, "_fields"):
            raise Exception("FlexTemplate subclasses must be initialized using a SingleBlock's TemplateClass method.")
        
        if cls._fields != ():
            return super().__new__(cls, blockDict, *args, **kwargs)
        
        # flex logic goes here to determine number of fields.
        return super().__new__(cls, blockDict, *args, **kwargs)
    
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
