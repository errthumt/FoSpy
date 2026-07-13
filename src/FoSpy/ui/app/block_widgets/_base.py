from ._utils import _get_editor, _get_widget

from ..window import MainWindow
from ....blocks import Block, SingleBlock, ListBlock, _containers as blk_cont
from .._utils import _get_label
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

    header = QLabel(f"<h3>{preamble}{label}</h3>")
    header_row.addWidget(header)
    base_layout.addLayout(header_row)

    subhead = QLabel(f"<h4>Block Type: <code>{type(blk).__name__}</code></h4>")
    pathtxt = blk.get_prop_path().replace("<","&lt;").replace(">","&gt;")
    pathhead = QLabel(f"<h4>Full Path: <code>{pathtxt}</code></h4>")
    base_layout.addWidget(subhead)
    base_layout.addWidget(pathhead)

    return header_row, base_layout


class SingleBlockWidget(QWidget):
    prop_map = None
    def __init__(self, label:str,blk:SingleBlock, window:MainWindow):
        self.win = window
        self.blk = blk
        parent = window.splitter
        self.editor_map = {"props": {}, "comments": {}}

        super().__init__(parent)

        self.header_row, base_layout = _add_header(self, label, "Properties")

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        base_layout.addLayout(main_layout)

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
        prop_layout = QVBoxLayout(scroll_content)
        prop_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.prop_layout = prop_layout

        scroll.setWidget(scroll_content)
        sidebar.addWidget(scroll)

        self.prop_labels = {}
        self._refresh_properties()

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

    def activate_prop_editor(self, prop_name):
        editor = self.editor_map["props"][prop_name]
        self.activate_editor(editor, label=f"✏️ {prop_name}")

    def activate_comment_editor(self, prop_name):
        editor = self.editor_map["comments"][prop_name]
        self.activate_editor(editor, label=f"🗩 {prop_name}")

    def _refresh_properties(self):
        # TODO: needs to clear self.prop_layout

        prop_dict = self.blk.get_prop_dict()

        for prop, val in prop_dict.items():
            
            if isinstance(val, blk_cont.SimpleWrapper):
                val = val()

            if isinstance(val, Block):
                btn_txt = f"Go to {prop}"
                edit_btn = QPushButton(btn_txt)
                edit_btn.clicked.connect(lambda _, v=val: self.win.go_to_block(v))
                self.prop_layout.addWidget(edit_btn)
                continue

            
            # TODO: add support for non-primitive builtins (list, dict)
            # Non-primitive editing will use a different kind of widget
            # displayed to the right of the sidebar


            row_layout = QHBoxLayout()

            label = QLabel(f"<b>{prop}:</b>")
            label.setMinimumWidth(120)
            row_layout.addWidget(label, stretch=0)
            self.prop_labels[prop] = label

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

            comment_btn = QPushButton("🗩")
            comment_editor = CommentEditorWidget(self, self.blk, prop, comment_btn)
            self.editor_map["comments"][prop] = comment_editor
            comment_editor.refresh_editor()
            comment_btn.clicked.connect(lambda *_, p=prop: self.activate_comment_editor(p))
            row_layout.addWidget(comment_btn, stretch=0)
            
            row_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
            self.prop_layout.addLayout(row_layout)

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
            # TODO: pass exceptions to user
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
            self.blk_widgets[child_blk] = tab_content
            tabs.addTab(tab_content, label)

        tabs.currentChanged.connect(self.on_tab_changed)

        main_layout.addWidget(tabs)

    def on_tab_changed(self, index:int):
        blk = self.blk._objs[index]
        self.win.go_to_block(blk)

    def go_to_tab(self, blk):
        idx = self.blk._objs.index(blk)
        self.tabs.setCurrentIndex(idx)

