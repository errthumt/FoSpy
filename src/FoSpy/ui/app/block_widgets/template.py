from ._base import SingleBlockWidget
from .. import editors as ed
from PySide6.QtWidgets import (
    QLabel, QDialog, QVBoxLayout, QListWidget, QListWidgetItem,
    QDialogButtonBox, QHBoxLayout, QPushButton
)

from PySide6.QtCore import Qt

class TemplateBlockWidget(SingleBlockWidget):
    def __init__(self, label, blk, window):
        blk.keys_to_front("template_name")
        super().__init__(label, blk, window)
        if blk is not window.root_block:
            disclaimer = QLabel("This block is a <i>staged template</i>. It will be attached to the parent block once all fields are filled in.")
        else:
            disclaimer = QLabel("This file is currently incomplete. It can be saved as a template to be filled in later, or, once all required fields are filled in, it can be saved as a complete file.")
        self.layout().insertWidget(1, disclaimer)

        fields_btn = QPushButton("Template Fields...")
        fields_btn.clicked.connect(self.add_fields_dlg)
        self.custom_btn_layout.insertWidget(2,fields_btn, stretch=0)

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

            new_block = filled
            if not isinstance(filled, TemplateBlock):
                save_as = self.win._custom_popup(
                    "File Complete!",
                    "All template fields in the current file have been filled in. Would you like to convert this file to a complete synthesis file?",
                    ("Convert and save later", False),
                    ("Save as...", True),
                    ("Keep editing as a template", None),
                    cancel=False
                )

                if save_as is None:
                    new_metadata = filled.metadata.add_field("fos_id")
                    new_metadata.fos_id.add_comments("After filling in all required fields, fill in this field to convert as a full synthesis file.")

                    new_block = new_metadata.find_fileblock()
                    new_block.template_name = self.blk.template_name
                    new_block._sourceFile = self.blk._sourceFile


            else:
                save_as = False

            self.win._flag_edited(new_block)
            self.win.root_block = new_block

            if save_as:
                self.win.save_dlg("fosx","fos","json")

            self.filled = self.win.root_block

            return self.win.root_block

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

        self.win.go_to_block(self.win.root_block)
        
        parent_widget = self.win.find_widget(filled._parent_block)
        return parent_widget.push_filled()
        
    def add_fields_dlg(self):
        dlg = TemplateFieldDialog(self, self.blk)
        if not dlg.exec():
            return

        return self._add_fields(dlg)

    @hard_refresh
    def _add_fields(self, dlg):
        from ....blocks.template import TemplateBlock   

        start_fields = dlg.start_fields
        new_fields = dlg.get_results()

        changes = {
            k: v for k, v in new_fields.items() if v != start_fields[k]
        }

        fill_fields = [k for k, v in changes.items() if not v]
        new_fields = [k for k, v in changes.items() if v]

        fill_values = {}

        for prop_name in fill_fields:
            current = getattr(self.blk, prop_name, None)
            if current is None:
                return

            if isinstance(current, TemplateBlock):
                current = current.serialize()

            fill_values[prop_name] = current

        filled = self.blk.fill(**fill_values)

        filled = filled.add_fields(*new_fields)
        self.filled = filled

        return filled


        


        

class TemplateFieldDialog(QDialog):
    def __init__(self, parent, blk):

        super().__init__(parent)
        self.blk = blk
        self.start_fields = self.get_fields(blk)
        self.setWindowTitle("Manage Template Fields")

        layout = QVBoxLayout(self)

        desc = QLabel("""
            <h4>Select which properties you would like to set as template fields.</h4>
                <ul>
                    <li>Simple properties will be cleared and replaced with a template field.</li>
                    <li>Properties containing nested blocks will be converted to a template
                        which allows template fields, but will keep any current values filled in.
                    </li>
                    <li>To add a list of templates under a single property, add a non-template list under that
                        property and add new items to the list instead. As long as one field is left unfilled, 
                        these items are treated as templates.
                    </li>
                </ul>""")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        self.selector = QListWidget(self)
        layout.addWidget(self.selector)

        for prop_name, is_template in self.start_fields.items():
            item = QListWidgetItem(prop_name)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Checked if is_template else Qt.CheckState.Unchecked)
            self.selector.addItem(item)

        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)

    @classmethod
    def get_fields(cls, blk):
        from ....blocks.blocks import ListBlock, SingleBlock
        from ....blocks.template import TemplateField
        validators = blk.get_validators()

        for prop in ('ext', 'rename', 'template_name'):
            validators.pop(prop, None)

        fields = {}

        for prop_name, validator in validators.items():
            if not isinstance(validator, type) or issubclass(validator, ListBlock):
                continue

            if issubclass(validator, SingleBlock):
                is_template = prop_name in blk._staged_templates

            else:
                is_template = issubclass(validator, TemplateField)

            fields[prop_name] = is_template

        return fields

    def get_results(self):
        results = {}
        for i in range(self.selector.count()):
            item = self.selector.item(i)
            results[item.text()] = item.checkState() == Qt.CheckState.Checked
        return results





        