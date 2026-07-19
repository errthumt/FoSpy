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
        return serial
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
    @classmethod
    def Simple(cls, reqCls, skip=False):
        class Flex(FlexTemplate, reqCls):
            _baseReq = reqCls
        
        SimpleList = ListBlock.Simple(Flex)

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

        return FlexList
    
    def serialize(self, **kwargs):
        serial = super().serialize(**kwargs)
        if len(serial) == 0:
            serial = [self._reqCls.reflex()]
        return serial
         
class TemplateBlock(SingleBlock):
    _id_key = "template_name"
    def __init__(self, blockDict, _dispatched=False):
        self._full_class = None
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
    
    def serialize(self,keepListType=False, shallow=False, clean=False):
        # from ..parsing.validation import required_keys
        # from ..parsing.format_fos import format_field
        required = self._full_class.build_req_validators()
        required.pop('ext',None)
        serial = super().serialize(keepListType=keepListType, shallow=shallow, clean=clean)

        out = {"template_name":serial.pop("template_name","")}
        for key,validator in required.items():
            if isinstance(validator,type):
                if issubclass(validator,TemplateBlock):
                    val = serial.pop(key, validator.reflex())
                elif issubclass(validator, TemplateList):
                    val = serial.pop(key, validator([]).serialize())
                else:
                    val = serial.pop(key, TemplateField("").serialize())
            else:
                val = serial.pop(key, TemplateField("").serialize())
            out[key] = val
        
        for key in serial:
            out[key] = serial[key]

        return out
    
    def __setattr__(self, name, value):
        from .. import _errors as err

        try:
            super().__setattr__(name, value)
        except err.FailedValidatorError as e:
            from ..parsing.validation import optional_keys
            self._val_exceptions[name] = e

            validators = optional_keys.setdefault(type(self), {})
            validators[name] = FailedTemplateField
            super().__setattr__(name, value)
    
    @classmethod
    def dispatch_subclass(cls, *args, **kwargs):
        try:
            return super().dispatch_subclass(*args, **kwargs)
        except Exception:
            return cls(*args, **kwargs, _dispatched=True)

class FlexTemplate(TemplateBlock):
    _baseReq = None #injected by TemplateList.Simple.Flex
    @classmethod
    def dispatch_subclass(cls, blockDict):
        from ._blockUtils import _unwrap_block, _template_found, _is_full_template
        template_keys = []
        blockDict = _unwrap_block(blockDict)
        temp_dict = blockDict.copy()
        required = cls.build_req_validators()
        all_validators = cls.build_validators()

        for key in required:
            if key != 'ext' and key not in temp_dict:
                template_keys.append(key)
        for key, val in blockDict.items():
            if _template_found(val):
                if _is_full_template(val):
                    if key not in template_keys:
                        template_keys.append(key)
                else:
                    validator = all_validators.get(key, None)
                    catch = ValueError("An incomplete template field was passed for an incompatible key.")
                    if not isinstance(validator, type):
                        raise catch
                    if issubclass(validator, SingleBlock):
                        temp_dict[key] = validator.reflex(**_unwrap_block(val))
                    elif issubclass(validator, ListBlock):
                        temp_dict[key] = TemplateList.Simple(validator._reqCls)(val)
                    else:
                        raise catch
                    
        pass
        return cls._baseReq.TemplateClass(*template_keys).dispatch_subclass(temp_dict)
    
    @classmethod
    def reflex(cls):
        return cls._baseReq.reflex()
