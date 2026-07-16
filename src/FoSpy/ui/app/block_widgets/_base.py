from ._utils import _get_editor, _get_widget

from ..window import MainWindow, Sentinel
from ....blocks import Block, SingleBlock, ListBlock, _containers as blk_cont, Rename
from .._utils import _get_label, _get_template_label
from ..editors.comments import CommentEditorWidget

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QScrollArea,
    QPushButton,
    QTabWidget,
    QStackedWidget
)

SIDEBAR_WIDTH = 400
SIDEBAR_MARGINS = (10,10,10,10)

SCROLL_WIDTH = SIDEBAR_WIDTH - SIDEBAR_MARGINS[0] - SIDEBAR_MARGINS[2]

def _add_header(widget:QWidget,label, view_name=None):
    blk = widget.blk

    base_layout = QVBoxLayout(widget)
    base_layout.setContentsMargins(0, 0, 0, 0)
    widget.setLayout(base_layout)

    header_row = QHBoxLayout()
    header_row.setContentsMargins(0, 0, 0, 0)

    preamble = f"{view_name} | " if view_name else ""
    post = None

    prop = blk.get_parent_prop()
    if prop is not None and "[" not in prop:
        rename_dict = blk._parent_block.rename_dict()
        if prop in rename_dict.values():
            renamed_from = next(k for k,v in rename_dict.items() if v == prop)
            label += " |"
            post = f"<i>(Renamed from {renamed_from})</i>"

    header = QLabel(f"<h3>{preamble}{label}</h3>")
    header_row.addWidget(header)
    if post is not None:
        header_row.addWidget(QLabel(post))

    base_layout.addLayout(header_row)

    subhead = QLabel(f"<h4>Block Type: <code>{type(blk).__name__}</code></h4>")
    pathtxt = blk.get_prop_path().replace("<","&lt;").replace(">","&gt;")
    pathhead = QLabel(f"<h4>Full Path: <code>{pathtxt}</code></h4>")
    base_layout.addWidget(subhead)
    base_layout.addWidget(pathhead)

    return header_row, base_layout

def _unicode_superscript(i:int):
    uni_map = ["⁰","¹","²","³","⁴","⁵","⁶","⁷","⁸","⁹"]

    base = i // 10

    if i >= 10:
        i = i % 10

    txt = uni_map[i]
    if base > 0:
        txt += _unicode_superscript(base)

    return txt

def _footnote_iter():
    i = 1
    while True:
        yield i
        i += 1


class SingleBlockWidget(QWidget):
    prop_map = None
    def __init__(self, label:str,blk:SingleBlock, window:MainWindow):
        self.win = window
        self.blk = blk
        parent = window.splitter
        self.editor_map = {"props": {}, "comments": {}, "misc": {}}
        self.footnote_iter = _footnote_iter()

        super().__init__(parent)


        self.header_row, base_layout = _add_header(self, label, "Properties")
        self.base_layout = base_layout

        if hasattr(blk, "rename"):
            rename_btn = QPushButton("Rename Properties")
            rename_btn.clicked.connect(
                lambda *_, b=blk.rename: self.win.go_to_block(b)
            )
            self.header_row.addWidget(rename_btn)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        base_layout.addLayout(main_layout)

        self.footnotes = QVBoxLayout()
        self.footnotes.setContentsMargins(0, 0, 0, 0)
        base_layout.addLayout(self.footnotes)

        sidebar = QVBoxLayout()
        self.sidebar = sidebar
        sidebar.setContentsMargins(*SIDEBAR_MARGINS)
        main_layout.addLayout(sidebar, stretch=0)

        editor = QStackedWidget()
        self.editor = editor
        main_layout.addWidget(editor, stretch=1)

        self.inactive = QLabel(
            "Select a property or comment editor to inspect it in more detail.\n\n"
            "Greyed-out properties can only be edited in the inspector."
            )
        self.inactive.setWordWrap(True)
        editor.addWidget(self.inactive)
        
        self.active = QTabWidget()
        editor.addWidget(self.active)

        self.deactivate_editor()

        sidebar_w = SIDEBAR_WIDTH

        scroll_w = sidebar_w - SIDEBAR_MARGINS[0] - SIDEBAR_MARGINS[2]

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll.setMinimumWidth(scroll_w)
        scroll.setContentsMargins(0,0,0,0)

        scroll_content = QWidget()
        scroll_content.setMinimumWidth(scroll_w)
        self.scroll_content = scroll_content

        scroll.setWidget(scroll_content)
        sidebar.addWidget(scroll)

        self.prop_labels = {}

        self._refresh_properties()

    @staticmethod
    def hard_refresh(func):
        def decorated(self, *args, **kwargs):
            def pending(f=func, a=args, k=kwargs):
                f(self, *a, **k)

            self.win.hard_refresh(self.blk, func=pending)
        return decorated

    def _add_footnote(self, txt):
        i = next(self.footnote_iter)

        footnote = QLabel(f"<sup>{i}</sup> {txt}")
        self.footnotes.addWidget(footnote)

        return i

    def _get_tabs(self):
        return [
            self.active.widget(i) for
            i in range(self.active.count())
        ]

    def deactivate_editor(self, editor=None):
        tabs = self._get_tabs()

        if editor in tabs:
            self.active.removeTab(self.active.indexOf(editor))

        if self.active.count() == 0 or editor is None:
            self.editor.setCurrentWidget(self.inactive)

        if hasattr(editor, "btn"):
            editor.btn.setText(editor.btn.text().replace("*",""))

    def activate_editor(self, editor, label="MISSING"):
        tabs = [
            self.active.widget(i) for
            i in range(self.active.count())
        ]

        if hasattr(editor, "btn"):
            txt = editor.btn.text()
            if "*" not in txt:
                editor.btn.setText(txt+"*")

        if editor not in tabs:
            self.active.addTab(editor, label)

        self.active.setCurrentIndex(self.active.indexOf(editor))
        self.editor.setCurrentWidget(self.active)

    def _register_misc_editor(self, editor, label="Misc Editor", editor_id:Sentinel=None):
        if editor_id is None:
            # instantiate unique ID object
            from ..window import Sentinel
            editor_id = Sentinel("misc editor id")
        
        self.editor_map["misc"][editor_id] = (editor, label)

        return editor_id

    def activate_misc_editor(self, editor_id:Sentinel):
        editor, label = self.editor_map["misc"][editor_id]
        self.activate_editor(editor, label)

    def activate_prop_editor(self, prop_name):
        editor = self.editor_map["props"][prop_name]
        self.activate_editor(editor, label=f"✏️ {prop_name}")

    def activate_comment_editor(self, prop_name):
        editor = self.editor_map["comments"][prop_name]
        self.activate_editor(editor, label=f"🗩 {prop_name}")

    def _refresh_properties(self, pending:callable=lambda:None):
        if self.active.count() > 0 and not self.win._custom_popup(
            "Refresh Required",
            "This action requires a refresh of the current block. This will close all open editor tabs. Continue?",
            ("Continue", True),
            cancel=True
        ):
            return
        
        pending()

        if hasattr(self, "prop_layout"):
            dummy = QWidget()
            dummy.setLayout(self.prop_layout)
            dummy.deleteLater()

        prop_layout = QVBoxLayout(self.scroll_content)
        prop_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.prop_layout = prop_layout

        prop_dict = self.blk.get_prop_dict()
        prop_dict.pop("rename", None)
        rename_dict = self.blk.rename_dict()
        renamed_from = {v:k for k,v in rename_dict.items()}

        req_props = self.blk.get_req_validators().keys()
        staged_templates = self.blk._staged_templates
        for prop, val in prop_dict.items():
            self._add_prop_row(prop, val, renamed_from, req_props)

        for prop, val in staged_templates.items():
            self._add_prop_row(prop, val, renamed_from, req_props, staged=True)
            # if prop == "rename":
            #     continue

            # prop_txt = prop
            # if prop in renamed_from:
            #     fn_i = self._add_footnote(f"Renamed from {renamed_from[prop]}")
            #     prop_txt += _unicode_superscript(fn_i)
            
            # if isinstance(val, blk_cont.SimpleWrapper):
            #     val = val()

            # row_layout = QHBoxLayout()

            # label = QLabel(f"<b>{prop_txt}:</b>")
            # label.setMinimumWidth(120)
            # row_layout.addWidget(label, stretch=0)
            # self.prop_labels[prop] = label

            # if isinstance(val, Block):
            #     btn_txt = "Go to Block"
            #     edit_btn = QPushButton(btn_txt)
            #     edit_btn.clicked.connect(lambda _, v=val: self.win.go_to_block(v))
            #     row_layout.addWidget(edit_btn, stretch=1)

            # else:
            #     txt = val.serialize() if hasattr(val, "serialize") else str(val)
            #     line_edit = QLineEdit(txt)
            #     line_edit.setCursorPosition(0)

            #     editor, enabler = _get_editor(val, self, prop)
            #     line_edit.setEnabled(enabler(txt))
            #     def on_apply(p=prop, e=line_edit, en=enabler):
            #         self._on_primitive_edit(p, e, en)

            #     def direct_edit(apply=on_apply):
            #         try:
            #             apply()
            #         except Exception:
            #             # TODO: pass to user
            #             pass


            #     line_edit.editingFinished.connect(on_apply)
            #     row_layout.addWidget(line_edit, stretch=1)

            #     if editor:
            #         editor = editor(self, line_edit, on_apply, prop)
            #         self.editor_map["props"][prop] = editor
            #         edit_btn = QPushButton("✏️")
            #         edit_btn.clicked.connect(lambda *_, p=prop: self.activate_prop_editor(p))
            #         row_layout.addWidget(edit_btn, stretch=0)

            # if prop not in req_props:
            #     del_btn = QPushButton("🗑")
            #     del_btn.clicked.connect(lambda *_, p=prop: self.delete_prop(p))
            #     row_layout.addWidget(del_btn, stretch=0)

            # comment_btn = QPushButton("🗩")
            # comment_editor = CommentEditorWidget(self, self.blk, prop, comment_btn)
            # self.editor_map["comments"][prop] = comment_editor
            # comment_editor.refresh_editor()
            # comment_btn.clicked.connect(lambda *_, p=prop: self.activate_comment_editor(p))
            # row_layout.addWidget(comment_btn, stretch=0)
            
            # row_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
            # self.prop_layout.addLayout(row_layout)

    def _add_prop_row(self, prop, val, renamed_from, req_props, staged=False):
        prop_txt = prop
        if prop in renamed_from:
            fn_i = self._add_footnote(f"Renamed from {renamed_from[prop]}")
            prop_txt += _unicode_superscript(fn_i)

        if staged:
            #unicode tag
            prop_txt = "🏷️" + prop_txt
        
        if isinstance(val, blk_cont.SimpleWrapper):
            val = val()

        row_layout = QHBoxLayout()

        label = QLabel(f"<b>{prop_txt}:</b>")
        label.setMinimumWidth(120)
        row_layout.addWidget(label, stretch=0)
        self.prop_labels[prop] = label

        if isinstance(val, Block):
            btn_txt = "Go to Block"
            edit_btn = QPushButton(btn_txt)
            edit_btn.clicked.connect(lambda _, v=val: self.win.go_to_block(v))
            row_layout.addWidget(edit_btn, stretch=1)

        else:
            txt = val.serialize() if hasattr(val, "serialize") else str(val)
            line_edit = QLineEdit(txt)
            line_edit.setCursorPosition(0)

            editor, enabler = _get_editor(val, self, prop)
            line_edit.setEnabled(enabler(txt))
            def on_apply(p=prop, e=line_edit, en=enabler):
                self._on_primitive_edit(p, e, en)

            def direct_edit(apply=on_apply):
                try:
                    apply()
                except Exception:
                    # TODO: pass to user
                    pass


            line_edit.editingFinished.connect(on_apply)
            row_layout.addWidget(line_edit, stretch=1)

            if editor:
                editor = editor(self, line_edit, on_apply, prop)
                self.editor_map["props"][prop] = editor
                edit_btn = QPushButton("✏️")
                edit_btn.clicked.connect(lambda *_, p=prop: self.activate_prop_editor(p))
                row_layout.addWidget(edit_btn, stretch=0)

        if prop not in req_props:
            del_btn = QPushButton("🗑")
            del_btn.clicked.connect(lambda *_, p=prop: self.delete_prop(p))
            row_layout.addWidget(del_btn, stretch=0)

        if not staged:
            comment_btn = QPushButton("🗩")
            comment_editor = CommentEditorWidget(self, self.blk, prop, comment_btn)
            self.editor_map["comments"][prop] = comment_editor
            comment_editor.refresh_editor()
            comment_btn.clicked.connect(lambda *_, p=prop: self.activate_comment_editor(p))
            row_layout.addWidget(comment_btn, stretch=0)
        
        row_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.prop_layout.addLayout(row_layout)

    def delete_prop(self, prop):
        def pending_delete(p=prop):
            delattr(self.blk, p)
            self.win._flag_edited(self.blk)
        self._refresh_properties(pending_delete)

    def _on_primitive_edit(self, prop:str, line_edit:QLineEdit, enabler:callable):
        new_text = line_edit.text()

        old_val = getattr(self.blk, prop)
        old_txt = old_val.serialize() if hasattr(old_val, "serialize") else str(old_val)

        if new_text == old_txt:
            return

        error = None
        try:
            setattr(self.blk, prop, new_text)

            enabled = enabler(new_text)
            line_edit.setEnabled(enabled)

            self.win._flag_edited(self.blk)
            label = self.prop_labels[prop]
            if "*" not in label.text():
                label.setText("*" + label.text())

        except Exception as e:
            line_edit.setText(old_txt)
            error = e

        line_edit.setCursorPosition(0)

        if error is not None:
            raise error

class ListBlockWidget(QWidget):
    def __init__(self, label:str, blk:ListBlock, window:MainWindow):
        self.win = window
        self.blk = blk
        parent = window.splitter
        self.blk_widgets = {}

        super().__init__(parent)

        self.header_row, base_layout = _add_header(self, label, "Tab View")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        base_layout.addLayout(main_layout)

        tabs = QTabWidget(self)
        tabs.setMovable(False)
        self.tabs = tabs

        for i, child_blk in enumerate(self.blk._objs):
            label = _get_label(child_blk, i)
            widget = _get_widget(child_blk)


            tab_content = widget(label, child_blk, window)

            delete_btn = QPushButton("Delete this Block")
            delete_btn.clicked.connect(lambda *_, blk=child_blk: self.remove_block(blk))
            tab_content.header_row.addWidget(delete_btn)
            tab_content.header_row.addStretch()

            self.blk_widgets[child_blk] = tab_content
            tabs.addTab(tab_content, label)

        for temp_id, template in self.blk._staged_templates.items():
            label = _get_template_label(template)
            widget = _get_widget(template)

            tab_content = widget(label, template, window)
            delete_btn = QPushButton("Delete this Template")
            delete_btn.clicked.connect(lambda *_, blk=template: self.remove_block(blk))
            tab_content.header_row.addWidget(delete_btn)
            tab_content.header_row.addStretch()

            self.blk_widgets[template] = tab_content
            tabs.addTab(tab_content, label)

        tabs.currentChanged.connect(self.on_tab_changed)

        main_layout.addWidget(tabs)

    def _find_block(self, idx):
        if idx < len(self.blk._objs):
            return self.blk._objs[idx]
        else:
            return list(self.blk._staged_templates.values())[idx - len(self.blk._objs)]
        
    def _find_idx(self, blk):
        if blk in self.blk._objs:
            return self.blk._objs.index(blk)
        else:
            return len(self.blk._objs) + list(self.blk._staged_templates.values()).index(blk)

    def on_tab_changed(self, index:int):
        blk = self._find_block(index)
        self.win.go_to_block(blk)

    def go_to_tab(self, blk):
        idx = self._find_idx(blk)
        self.tabs.setCurrentIndex(idx)

    def find_widget(self, blk):
        idx = self._find_idx(blk)
        return self.tabs.widget(idx)

    def remove_block(self, blk):
        if not self.win._custom_popup(
            "Delete this block?",
            "Are you sure you want to delete this block? "
            "Deleted blocks cannot be recovered once any changes are saved.",
            ("Delete", True),
            cancel=True
        ):
            return


        self.blk.remove_block(blk)
        self.win._flag_edited(self.blk)
        if hasattr(self.blk, "_parent_block"):
            self.win.go_to_block(self.blk._parent_block)
        self.win.go_to_block(self.blk)

