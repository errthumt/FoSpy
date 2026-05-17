from . import FileBlock, ListBlock, SingleBlock, inherit_class_doc, inherit_docstring

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
    def _build_index(self):
        self._index = {}
        for obj in self._objs:
            self._index[obj.template_name] = obj
    def get_obj(self, template_name):
        self._build_index()

        temp_obj = self._index.get(template_name)
        if not temp_obj:
            raise KeyError(f"No template found with name '{template_name}'")
        
        parent_cls = next(
            base for base in type(temp_obj).__bases__
            if issubclass(base, SingleBlock)
            and base not in (TemplateBlock, SingleBlock, ListBlock)
        )

        serial = temp_obj.serialize()[0]
        serial.pop("template_name",None)
        return parent_cls.subclass(serial)
    
    def append(self, obj:SingleBlock, template_name=""):
        serial = obj.serialize()[0]
        if template_name:
            serial["template_name"] = template_name
        elif not serial.get("template_name"):
            raise ValueError("Cannot append object to a template list without an existing "
                             "template_name or a new template_name passed as an argument.")
        return super().append(self._reqCls.subclass(serial))

class TemplateBlock(SingleBlock):
    def __init__(self, template_name, blockDict):
        self._full_class = None
        blockDict["template_name"] = template_name
        super().__init__(blockDict)
    def fill(self,**kwargs):
        if not self._full_class is not None and issubclass(self._full_class, SingleBlock):
            raise TypeError("A Template Block must be initialized from an existing class in order to be filled.")

        serial = self.serialize()[0]
        serial.pop("template_name",None)
        for kw, arg in kwargs.items():
            serial[kw] = arg

        return self._full_class(serial)
