from .blocks import FileBlock, ListBlock, SingleBlock, inherit_class_doc, inherit_docstring

from .._debug import Debug
_debug = Debug()

class TemplateField:
    def __init__(self, *args, **kwargs):
        pass
    def serialize(self,keepListType=None):
        from ..parsing.format import format_field
        return format_field("template")

@inherit_class_doc(FileBlock)
class TemplateSet(FileBlock):
    """
    Represents a set of templates loaded from a FOS file.

    FOS files may contain multiple different types of templates grouped into
    `TemplateList`s. Each of these lists is one attribute of a `TemplateSet`.
    """
    def __init__(self, blockDict, _sourceFile=None):
        from ..parsing.validation import TemplateLists
        self._aliases = TemplateLists
        super().__init__(blockDict, _sourceFile)


@inherit_class_doc(ListBlock)
class TemplateList(ListBlock):
    """
    Represents a list of templates with the same subclass.
    """
    @classmethod
    def Simple(cls, reqCls, skip=False):
        class Flex(FlexTemplate, reqCls):
            _baseReq = reqCls
        
        SimpleList = ListBlock.Simple(Flex)
        class FlexList(TemplateList, SimpleList):
            pass

        FlexList.__name__ = f"{reqCls.__name__}FlexList"
        FlexList.__qualname__ = f"{cls.__name__}.{reqCls.__name__}FlexList"
        FlexList.__module__ = cls.__module__

        return FlexList
    
    def serialize(self):
        serial = super().serialize()
        if len(serial) == 0:
            serial = [self._reqCls.reflex()]
        return serial
    
      

class TemplateBlock(SingleBlock):
    def __init__(self, blockDict):
        self._full_class = None
        super().__init__(blockDict)

    def fill(self,**kwargs):
        if not self._full_class is not None and issubclass(self._full_class, SingleBlock):
            raise TypeError("A Template Block must be initialized from an existing class in order to be filled.")


        serial = self.serialize(keepListType=True)
        serial.pop("template_name",None)
        for kw, arg in kwargs.items():
            serial[kw] = arg

        return self._full_class(serial)
    
    def serialize(self,keepListType=False, shallow=False):
        from ..parsing.validation import required_keys
        from ..parsing.format import format_field
        required = self._full_class.build_req_validators()
        required.pop('ext',None)
        serial = super().serialize(keepListType=keepListType, shallow=shallow)

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

def _template_found(val):
    if val == TemplateField().serialize():
        return True
    
    if isinstance(val, list):
        for d in val:
            if _template_found(d):
                return True
        return False
    
    if isinstance(val, dict):
        for key, v in val.items():
            if key != "template_name" and _template_found(v):
                return True
        return False
    
    return False

def _is_full_template(val):
    if val == TemplateField().serialize():
        return True
    
    if isinstance(val, list):
        if len(val) != 1:
            return False
        if type(val[0]) is not dict:
            return False
        return _is_full_template(val[0])
    
    if isinstance(val, dict):
        for key, v in val.items():
            if key != "template_name" and not (key.startswith("_") or _is_full_template(v)):
                return False
        return True

            

class FlexTemplate(TemplateBlock):
    _baseReq = None #injected by TemplateList.Simple.Flex
    @classmethod
    def subclass(cls, blockDict):
        from ..parsing.format import format_field
        from .blocks import unwrap_block
        template_keys = []
        blockDict = unwrap_block(blockDict)
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
                        temp_dict[key] = validator.reflex(**unwrap_block(val))
                    elif issubclass(validator, ListBlock):
                        temp_dict[key] = TemplateList.Simple(validator._reqCls)(val)
                    else:
                        raise catch
                    
        pass
        return cls._baseReq.TemplateClass(*template_keys).subclass(temp_dict)
    
    @classmethod
    def reflex(cls):
        return cls._baseReq.reflex()