from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QWidget,
    QLabel,
    QScrollArea,
    QLineEdit,
    QComboBox
)

from ._base import BaseEditorWidget
from ..window import Sentinel
from ....parsing.validators.rename import RESERVED

class RenameEditorWidget(BaseEditorWidget):
    editor_id = Sentinel("rename editor id")
    def __init__(self, block_widget):
        panel = RenameEditorPanel(block_widget.blk)
        super().__init__(block_widget, panel)
        self.okay_btn.setVisible(False)
        self.cancel_btn.setVisible(False)

    def apply(self):
        rename_from = self.editor.selector.currentText()
        rename_to = self.editor.input.text()
        self.editor.parent_blk.rename_block(rename_from, rename_to)
        self.blk_widget.win._flag_edited(self.editor.parent_blk)
        self._hard_refresh()



class RenameEditorPanel(QWidget):
    def __init__(self, blk):
        super().__init__()

        parent_blk = blk._parent_block
        self.blk = blk
        self.parent_blk = parent_blk

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)

        header = QLabel("<h4>Rename Properties</h4>")
        desc = QLabel("Select an existing property and type what you want to rename it to below. Then click 'Apply'.")
        desc.setWordWrap(True)

        blk_props = parent_blk.get_prop_dict()
        for prop in RESERVED:
            blk_props.pop(prop, None)
            
        rename_dict = parent_blk.rename_dict()

        selector_list = []
        for prop in blk_props:
            if prop in rename_dict.values():
                txt = "*"+prop
            else:
                txt = prop
            selector_list.append(txt)

        selector_list.extend(list(rename_dict.keys()))

        self.selector = QComboBox()
        self.selector.addItems(selector_list)
        self.selector.setEditable(False)
        self.selector.currentTextChanged.connect(self.on_change)

        self.input = QLineEdit()

        for w in (header, desc, self.selector, self.input):
            self.main_layout.addWidget(w)

    def on_change(self, text):
        text = text.lstrip("*")
        rename_dict = self.parent_blk.rename_dict()
        rename_from = {v:k for k,v in rename_dict.items()}
        set_to = False
        if text in rename_from:
            set_to = text
            self.selector.setCurrentText(rename_from[text])
        else:
            set_to = rename_dict.get(text, "")
        
        self.input.setText(set_to)

