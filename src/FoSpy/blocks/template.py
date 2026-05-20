from . import FileBlock, ListBlock, SingleBlock, inherit_class_doc, inherit_docstring

from .._debug import Debug
_debug = Debug()

class TemplateField:
    def __init__(self, *args, **kwargs):
        pass
    def serialize(self,keepListType=None):
        from .. import format_field
        return format_field("template")

@inherit_class_doc(FileBlock)
class TemplateSet(FileBlock):
    """
    Represents a set of templates loaded from a FOS file.

    FOS files may contain multiple different types of templates grouped into
    `TemplateList`s. Each of these lists is one attribute of a `TemplateSet`.
    """
    def __init__(self, blockDict, _sourceFile=None):
        super().__init__(blockDict, _sourceFile)


@inherit_class_doc(ListBlock)
class TemplateList(ListBlock):
    """
    Represents a list of templates with the same subclass.
    """
    _reqCls = None
    @classmethod
    def Simple(cls, reqCls):
        def FromList(blockList):
            return ListBlock.Simple(reqCls.Template_from_dict(blockList[0]))(blockList)
        return FromList
      

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
    
    def serialize(self,keepListType=False):
        from ..parsing.validation import required_keys
        from ..parsing.format import format_field
        required = self._full_class.build_req_validators()
        required.pop('ext',None)
        serial = super().serialize(keepListType)

        out = {"template_name":serial.pop("template_name","")}
        for key in required:
            out[key] = serial.pop(key, format_field("template"))
        
        for key in serial:
            out[key] = serial[key]

        return out
