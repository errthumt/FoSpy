from ._base import SingleBlockWidget
from .. import editors as ed
from PySide6.QtWidgets import QLabel

class TemplateBlockWidget(SingleBlockWidget):
    def __init__(self, label, blk, window):
        blk.keys_to_front("template_name")
        super().__init__(label, blk, window)
        if blk is not window.root_block:
            disclaimer = QLabel("This block is a <i>staged template</i>. It will be attached to the parent block once all fields are filled in.")
        else:
            disclaimer = QLabel("This file is currently incomplete. It can be saved as a template to be filled in later, or, once all required fields are filled in, it can be saved as a complete file.")
        self.layout().insertWidget(1, disclaimer)

    @staticmethod
    def hard_refresh(func):
        def decorated(self, *args, **kwargs):
            def pending(f=func, a=args, k=kwargs):
                return f(self, *a, **k)
            
            result = self.win.hard_refresh(func=pending, to_blk=False)
            if result is None:
                return
            
            if getattr(self, "filled", None) is not None:
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

        if not hasattr(self.blk, "_staged_parent"):
            root_blk = self.win.root_block
            if self.blk is not root_blk:
                raise NotImplementedError("Features for editing non-staged templates have not been implemented yet.")

            filled = self.blk.fill(**props)
            self.win._flag_edited(filled)
            self.filled = filled
            self.win.root_block = filled
            return filled

        staged_parent = self.blk._staged_parent
        staged_dict = staged_parent._staged_templates
        staged_reversed = {v:k for k,v in staged_dict.items()}

        temp_id = staged_reversed[self.blk]

        temp_id, filled = staged_parent.fill_staged_template(temp_id, **props)
        self.filled = filled

        self.win._flag_edited(filled)

        if isinstance(filled, TemplateBlock) and not (staged_parent is self.win.root_block and temp_id == "metadata"):
            filled.template_name = temp_id

        if not hasattr(filled, "_parent_block") or isinstance(filled, TemplateBlock) or not isinstance(filled._parent_block, TemplateBlock):
            return filled
        
        parent_widget = self.win.find_widget(filled._parent_block)
        return parent_widget.push_filled()
        


        