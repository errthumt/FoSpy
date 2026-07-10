from .window import MainWindow
from ...blocks import Block, SingleBlock, ListBlock, _containers as blk_cont
from ._utils import _get_label
from . import editors
from .editors.comments import CommentEditorWidget

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

widget_map = {
    str:(
        editors.text_editor.TextEditorWidget,
        lambda value: "\n" not in value
    )
}

def _get_editor(value):
    if type(value) in widget_map:
        editor, enabler = widget_map[type(value)]

        if not callable(enabler):
             def static_enabler(val, e=enabler):
                 return e
             enabler = static_enabler
        
        return editor, enabler

    if hasattr(value, "serialize") and callable(value.serialize):
        return _get_editor(value.serialize())
    
    return _get_editor(str(value))

class SingleBlockWidget(QWidget):
    def __init__(self, label:str,blk:SingleBlock, window:MainWindow):
        self.win = window
        self.blk = blk
        parent = window.splitter

        super().__init__(parent)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

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

        header = QLabel(f"<h3>Properties | {label}</h3>")
        subhead = QLabel(f"<h4>({type(blk).__name__})</h4>")

        sidebar.addWidget(header)
        sidebar.addWidget(subhead)

        sidebar_w = max(
            SIDEBAR_WIDTH,
            header.sizeHint().width(),
            subhead.sizeHint().width()
        )

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

            editor, enabler = _get_editor(val)
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

            editor = editor(self, line_edit, on_apply)
            edit_btn = QPushButton("✏️")
            edit_btn.clicked.connect(lambda *_, e=editor, p=prop: self.activate_editor(e, label=f"✏️ {p}"))

            comment_btn = QPushButton("🗩")
            comment_editor = CommentEditorWidget(self, self.blk, prop, comment_btn)
            comment_editor.refresh_editor()
            comment_btn.clicked.connect(lambda *_, e=comment_editor, p=prop: self.activate_editor(e, label=f"🗩 {p}"))

            row_layout.addWidget(line_edit, stretch=1)
            row_layout.addWidget(edit_btn, stretch=0)
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

widget_map[SingleBlock] = SingleBlockWidget

class ListBlockWidget(QWidget):
    def __init__(self, label:str, blk:ListBlock, window:MainWindow):
        self.win = window
        self.blk = blk
        parent = window.splitter

        super().__init__(parent)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(main_layout)

        header = QLabel(f"<h3>Tab View | {label}</h3>")
        subhead = QLabel(f"<h4>({type(blk).__name__})</h4>")

        main_layout.addWidget(header)
        main_layout.addWidget(subhead)

        tabs = QTabWidget(self)
        tabs.setMovable(False)
        self.tabs = tabs

        for i, child_blk in enumerate(self.blk._objs):
            label = _get_label(child_blk, i)

            tab_content = SingleBlockWidget(label, child_blk, window)
            tabs.addTab(tab_content, label)

        tabs.currentChanged.connect(self.on_tab_changed)

        main_layout.addWidget(tabs)

    def on_tab_changed(self, index:int):
        blk = self.blk._objs[index]
        self.win.go_to_block(blk)

    def go_to_tab(self, blk):
        idx = self.blk._objs.index(blk)
        self.tabs.setCurrentIndex(idx)

widget_map[ListBlock] = ListBlockWidget

