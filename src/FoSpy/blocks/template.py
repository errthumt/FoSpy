from . import FileBlock, ListBlock, SingleBlock, inherit_class_doc, inherit_docstring

from .._debug import Debug
_debug = Debug()

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
        def FromDict(blockDict):
            return ListBlock.Simple(reqCls.Template_from_dict(blockDict[0]))(blockDict)
        return FromDict
      

class TemplateBlock(SingleBlock):
    def __init__(self, blockDict):
        self._full_class = None
        super().__init__(blockDict)
    def fill(self,**kwargs):
        if not self._full_class is not None and issubclass(self._full_class, SingleBlock):
            raise TypeError("A Template Block must be initialized from an existing class in order to be filled.")

        serial = self.serialize()[0]
        serial.pop("template_name",None)
        for kw, arg in kwargs.items():
            serial[kw] = arg

        return self._full_class(serial)
    
    def serialize(self):
        from ..parsing.validation import required_keys
        from ..parsing.format import format_field
        required = required_keys.get(self._full_class, {})

        serial = super().serialize()

        for key in required:
            if key not in serial[0]:
                serial[0][key] = format_field("template")

        return serial
