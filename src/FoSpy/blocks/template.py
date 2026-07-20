from .files import FileBlock

from .blocks import ListBlock, SingleBlock, Block
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

@FileBlock.set_dispatch("templates")
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
         
class TemplateBlock(SingleBlock):
    _id_key = "template_name"
    def __init__(self, blockDict, _dispatched=False, **kwargs):
        self._val_exceptions = {}

        super().__init__(blockDict, _dispatched=_dispatched)

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

        return self._full_class.dispatch_subclass(serial)
    
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
    def find_dispatch_values(cls):
        out = {}

        mro = cls.__mro__
        for parent_cls in reversed(mro):
            dispatch_key = getattr(parent_cls, "dispatch_key", None)
            if dispatch_key is None:
                continue
            if dispatch_key.startswith("_"):
                # If dispatch key is private, it is determined dynamically during dispatch.
                # dispatch methods using private keys should bind defaults to the dispatch method.
                dispatch_vals = parent_cls.dispatch_subclass({}, _get_defaults=True)
                out.update(dispatch_vals)
            else:
                try:
                    dispatch_val = next(
                        k for k, v in parent_cls.dispatch.items()
                        if v is not None
                        and issubclass(cls, v)
                    )
                    out[dispatch_key] = dispatch_val
                except StopIteration:
                    pass


        out = {k:v for k,v in out.items() if v is not None}

        return out
    
    @classmethod
    def TemplateClass(cls, *args):
        if None in (cls._full_class, cls._fields):
            raise TypeError("A new Template Block must be initialized from an existing class, or a Template of that class.")

        fields = list(cls._fields)

        fields.extend([a for a in args if a not in fields])
        
        return cls._full_class.TemplateClass(*fields)
    
    @classmethod
    def next_dispatch(cls):
        # skip abstract classes
        try:
            mro = cls.__mro__
            next_blk_cls = next(c for c in mro[1:] if issubclass(c, SingleBlock)
                                and getattr(c, "dispatch_key", None) is not None)
        except StopIteration:
            return None, None
        
        next_key = next_blk_cls.dispatch_key
        next_val = getattr(cls, next_key, None)

        return next_key, next_val
    
    @staticmethod
    def make_dispatch(*args, **kwargs):
        func = SingleBlock.make_dispatch(*args, **kwargs).__func__
        @classmethod
        def wrapper(cls,blockDict, _f=func, **kw):
            from ._blockUtils import _unwrap_block

            if not isinstance(blockDict, dict):
                blockDict = _unwrap_block(blockDict)
                
            next_key, next_val = cls.next_dispatch()
            if next_key is not None:
                set_val = blockDict.setdefault(next_key, next_val)
                if set_val is None:
                    raise TypeError("A new Template Block must be initialized from an existing class, or a Template of that class.")
                # if set_val is () but next_val is truthy, FlexTemplate is dispatching
                elif next_val and not set_val:
                    blockDict[next_key] = next_val
            
            # skip None and () values
            if not kw.get("_template_fields", None):
                kw["_template_fields"] = getattr(cls, "_fields", blockDict.get("_fields", None))

            return _f(cls, blockDict, **kw)
        return wrapper
    
    @make_dispatch
    def dispatch_subclass(cls, blockDict, **kwargs):
        return super(TemplateBlock, cls)

    
class AbstractTemplateLocator:
    @TemplateBlock.make_dispatch
    def dispatch_subclass(cls, blockDict, **kwargs):
        return super(AbstractTemplateLocator, cls)
    
class AbstractTemplate:
    @TemplateBlock.make_dispatch
    def dispatch_subclass(cls, blockDict, **kwargs):
        from ..parsing.validation import optional_keys, required_keys
        
        # populate validators only once for each constructed template class
        if cls not in optional_keys:
            validators = cls.build_validators()

            req_validators = required_keys.setdefault(cls, {})
            template_validators = optional_keys.setdefault(cls, {})
            for field in cls._fields:
                validator = validators.get(field, None)
                req_validators[field] = False
                if isinstance(validator, type) and issubclass(validator, SingleBlock):
                    template_validators[field] = FlexTemplate.reflexor(validator)
                elif isinstance(validator, type) and issubclass(validator, ListBlock):
                    template_validators[field] = TemplateList.Simple(validator._reqCls)
                else:
                    template_validators[field] = TemplateField



        return super(AbstractTemplate, cls)


class FlexTemplate(SingleBlock):
    _baseReq = None
    @classmethod
    def reflexor(cls, subcls):
        if getattr(subcls, "_full_class", None) is not None:
            subcls = subcls._full_class

        # First recursion:
        #   - calls TemplateClass(*()) to initialize locator and base
        #   - after initializing locator and base,
        #       TemplateClass calls reflexor to promote base to reflexor
        # Second recursion (called by TemplateClass(*())):
        #    calls TemplateClass again, which now returns the cached base
        BaseTemplateClass = subcls.TemplateClass()

        # First Recursion:
        #    Reflexor was already cached by second recursion, return it
        if issubclass(BaseTemplateClass, FlexTemplate):
            return BaseTemplateClass
        
        # Second Recursion:
        #    Replace cached base with new reflexor subclass

        TemplateLocator = TemplateBlock.dispatch[subcls]
        
        @TemplateLocator.set_dispatch(())
        class Reflexor(FlexTemplate, BaseTemplateClass):
            _baseReq = subcls

        mro = Reflexor.__mro__


        Reflexor.__name__ = f"Flex{subcls.__name__}"
        Reflexor.__qualname__ = f"{cls.__name__}.reflexor.Flex{subcls.__name__}"
        Reflexor.__module__ = cls.__module__

        from ..parsing.validation import optional_keys, required_keys

        old_reqs = Reflexor.build_req_validators()
        req_vals = {k:False for k in old_reqs}
        req_vals.pop('ext', None)

        required_keys[Reflexor] = req_vals
        Reflexor.req_overrides = req_vals
        optional_keys.setdefault(Reflexor, {}).update(old_reqs)

        return Reflexor

    @TemplateBlock.make_dispatch
    def dispatch_subclass(cls, blockDict, **kwargs):
        if cls._baseReq is None:
            raise TypeError("To dispatch a FlexTemplate, it must be initialized from an existing class using FlexTemplate.reflexor().")
        
        from ._blockUtils import  _template_found


        req_overrides = cls.req_overrides.copy()
        validators = cls.build_validators()

        rename_dict = blockDict.get("rename", {})
        rename_from = {v:k for k,v in rename_dict.items()}

        template_fields = []

        dispatch_values = cls.find_dispatch_values()

        for key, val in dispatch_values.items():
            blockDict.setdefault(key, val)

        for orig_key, val in blockDict.items():
            req_overrides.pop(orig_key, None)
            if orig_key in rename_from:
                key = rename_from[key]
            else:
                key = orig_key

            if _template_found(val):
                template_fields.append(key)
            else:
                validator = validators.get(key, lambda x: x)
                try:
                    if isinstance(validator, type) and issubclass(validator, SingleBlock):
                        new_val = validator.dispatch_subclass(val)
                    else:
                        new_val = validator(val)
                    blockDict[orig_key] = new_val
                except Exception:
                    template_fields.append(key)


        for key in req_overrides:
            template_fields.append(key)
            blockDict[key] = TemplateField

        if not template_fields:
            return cls._baseReq
        
        TemplateClass = cls._baseReq.TemplateClass(*template_fields)

        return TemplateClass
    
    @classmethod
    def reflex(cls):
        return cls._baseReq.reflex()
