from ._base import SingleBlockWidget
from .. import editors as ed
from PySide6.QtWidgets import QLabel

class TemplateBlockWidget(SingleBlockWidget):
    def __init__(self, label, blk, window):
        super().__init__(label, blk, window)

        disclaimer = QLabel("This block is a <i>staged template</i>. It will be attached to the parent block once all fields are filled in.")
        self.header_row.layout().insertWidget(1, disclaimer)

    def _on_primitive_edit(self, prop, line_edit, enabler):
        super()._on_primitive_edit(prop, line_edit, enabler)

        new_text = line_edit.text()

        fill_props = {prop:new_text}

        self.push_filled(**fill_props)

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
        
        self.win.refresh_tree(staged_parent)

        self.win.go_to_block(filled)

        if not hasattr(filled, "_parent_block") or isinstance(filled, TemplateBlock) or not isinstance(filled._parent_block, TemplateBlock):
            return
        
        # TODO: window should have method for finding block widget
        from ..window import WIDGET_DATA_ROLE
        
        parent_blk = filled._parent_block
        win = self.win

        tree_item = win.tree_items[parent_blk]
        blk_widget = tree_item.data(WIDGET_DATA_ROLE)["widget"]

        # If block is in ListBlock, it's widget is stored in ListBlockWidget
        if blk_widget is None:
            parent = parent_blk._parent_block
            listblk_item = win.tree_items[parent]
            listblk_widget = listblk_item.data(WIDGET_DATA_ROLE)["widget"]
            blk_widget = listblk_widget.blk_widgets[parent_blk]
  
        blk_widget.push_filled()

        