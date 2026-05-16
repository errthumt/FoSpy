from . import FileBlock, ListBlock, SingleBlock

class TemplateSet(FileBlock):
    def __init__(self, blockDict, _sourceFile=None):
        super().__init__(blockDict, _sourceFile)

class TemplateList(ListBlock):
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
        return super().append(self._reqCls.from_blockList(serial))


class TemplateBlock(SingleBlock):
    pass
