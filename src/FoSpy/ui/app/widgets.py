from .window import MainWindow
from ...blocks import Block, SingleBlock, ListBlock, _containers as blk_cont
from ._utils import _get_label

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QScrollArea,
    QPushButton,
    QTabWidget
)

widget_map = {ListBlock: lambda label, blk, window: QLabel("ListBlock Placeholder")}

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
        sidebar.setContentsMargins(10, 10, 10, 10)
        main_layout.addLayout(sidebar)

        header = QLabel(f"<h3>Properties | {label}</h3>")
        subhead = QLabel(f"<h4>({type(blk).__name__})</h4>")

        sidebar.addWidget(header)
        sidebar.addWidget(subhead)

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)

        scroll_content = QWidget()
        prop_layout = QVBoxLayout(scroll_content)
        prop_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.prop_layout = prop_layout

        scroll.setWidget(scroll_content)
        sidebar.addWidget(scroll)

        self.prop_labels = {}
        self._refresh_properties()

    def _refresh_properties(self):
        # TODO: needs to clear self.prop_layout

        prop_dict = self.blk.get_prop_dict()

        for prop, val in prop_dict.items():
            
            if isinstance(val, blk_cont.SimpleWrapper):
                val = val()

            if isinstance(val, Block):
                btn_txt = f"Go to {prop}"
                btn = QPushButton(btn_txt)
                btn.clicked.connect(lambda _, v=val: self.win.go_to_block(v))
                self.prop_layout.addWidget(btn)
            
            # TODO: add support for non-primitive builtins (list, dict)
            # Non-primitive editing will use a different kind of widget
            # displayed to the right of the sidebar

            elif type(val) in widget_map:
                pass

            else:
                row_layout = QHBoxLayout()

                label = QLabel(f"<b>{prop}:</b>")
                label.setMinimumWidth(120)
                row_layout.addWidget(label)
                self.prop_labels[prop] = label

                txt = val.serialize() if hasattr(val, "serialize") else str(val)
                line_edit = QLineEdit(txt)
                line_edit.editingFinished.connect(
                    lambda p=prop, e=line_edit: self._on_primitive_edit(p,e)
                )
                row_layout.addWidget(line_edit)
                self.prop_layout.addLayout(row_layout)

    def _on_primitive_edit(self, prop:str, line_edit:QLineEdit):
        new_text = line_edit.text()

        old_val = getattr(self.blk, prop)
        old_txt = old_val.serialize() if hasattr(old_val, "serialize") else str(old_val)

        if new_text == old_txt:
            return

        try:
            setattr(self.blk, prop, new_text)

            self.win._flag_edited(self.blk)
            label = self.prop_labels[prop]
            if "*" not in label.text():
                label.setText("*" + label.text())

        except Exception:
            # TODO: pass exceptions to user
            line_edit.setText(str(getattr(self.blk, prop)))

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

        for i, child_blk in enumerate(self.blk._objs):
            label = _get_label(child_blk, i)

            tab_content = SingleBlockWidget(label, child_blk, window)
            tabs.addTab(tab_content, label)

        main_layout.addWidget(tabs)

widget_map[ListBlock] = ListBlockWidget

