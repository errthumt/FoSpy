from ._base import SingleBlockWidget
from .. import editors as ed
from PySide6.QtWidgets import QLabel

class TemplateBlockWidget(SingleBlockWidget):
    def __init__(self, label, blk, window):
        super().__init__(label, blk, window)

        disclaimer = QLabel("This block is a <i>staged template</i>. It will be attached to the parent block once all fields are filled in.")
        self.layout().insertWidget(1, disclaimer)

    @staticmethod
    def hard_refresh(func):
        def decorated(self, *args, **kwargs):
            def pending(f=func, a=args, k=kwargs):
                return f(self, *a, **k)
            
            result = self.win.hard_refresh(func=pending, to_blk=False)
            if result is None:
                return
            
            if hasattr(self, "filled") and self.filled is not None:
                self.win.go_to_block(self.filled)

            return result
        return decorated

    def _on_primitive_edit(self, prop, line_edit, enabler):
        super()._on_primitive_edit(prop, line_edit, enabler)

        new_text = line_edit.text()

        fill_props = {prop:new_text}

        new_blk = self.push_filled(**fill_props)
        new_widget = self.win.find_widget(blk=new_blk,go_to=True)
        new_widget.next_line(prop)

    @hard_refresh
    def push_filled(self, **props):
        from ....blocks import TemplateBlock

        staged_parent = self.blk._staged_parent
        staged_dict = staged_parent._staged_templates
        staged_reversed = {v:k for k,v in staged_dict.items()}

        temp_id = staged_reversed[self.blk]

        temp_id, filled = staged_parent.fill_staged_template(temp_id, **props)

        self.win._flag_edited(filled)

        if isinstance(filled, TemplateBlock):
            filled.template_name = temp_id

        if not hasattr(filled, "_parent_block") or isinstance(filled, TemplateBlock) or not isinstance(filled._parent_block, TemplateBlock):
            self.filled = filled
            return filled
        
        parent_widget = self.win.find_widget(filled._parent_block)
        return parent_widget.push_filled()
        


        