from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QWidget,
    QLabel,
    QScrollArea,
    QLineEdit,
)

from ._base import BaseEditorWidget

class CommentEditorWidget(BaseEditorWidget):
    def __init__(self, block_widget, blk, prop_name, btn):
        super().__init__(block_widget,
            CommentsEditorPanel(blk, prop_name)
        )
        self.btn = btn
        self.editor.btn = btn
        self.on_apply = lambda: None
        self.base_layout.setStretchFactor(self.hintPanel, 0)

    def refresh_editor(self):
        self.editor.refresh_view()

    def apply(self):
        self.editor.send_comments()
        super().apply()

    def is_changed(self):
        blk_comments = self.editor.get_comments()

        editor_comments = list(self.editor.comment_rows.values())

        return blk_comments != editor_comments

class CommentsEditorPanel(QWidget):
    def __init__(self, blk, prop_name):
        super().__init__()

        self.blk = blk
        self.prop_name = prop_name
        self.comment_rows = {}
        self.row_layouts = {}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll.setContentsMargins(0, 0, 0, 0)
        scroll.setSizeAdjustPolicy(QScrollArea.SizeAdjustPolicy.AdjustToContents)

        scroll_content = QWidget()
        self.main_layout = QVBoxLayout(scroll_content)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        scroll_content.setLayout(self.main_layout)

        scroll.setWidget(scroll_content)

        layout.addWidget(scroll, stretch=1)

        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.addStretch()

        add_btn = QPushButton("Add Comment")
        add_btn.clicked.connect(lambda *_: self._add_comment())
        bottom_layout.addWidget(add_btn)

        clear_btn = QPushButton("Clear All")
        clear_btn.clicked.connect(lambda *_: self.clear_comments())
        bottom_layout.addWidget(clear_btn)

        layout.addLayout(bottom_layout)

        self.refresh_view()

    def get_comments(self):
        return self.blk._meta.comments.get(self.prop_name, [])
    
    def send_comments(self):
        self.blk._meta.comments[self.prop_name] = list(self.comment_rows.values())
    
    def delete_comment(self, comment_edit):
        row_layout = self.row_layouts[comment_edit]
        while row_layout.count() > 0:
            w = row_layout.itemAt(0).widget()
            if w:
                row_layout.removeWidget(w)
                w.deleteLater()
        self.main_layout.removeItem(row_layout)
        row_layout.deleteLater()
        self.comment_rows.pop(comment_edit, None)

        if hasattr(self, "btn") and self.comment_rows == {}:
            txt = self.btn.text()
            txt = txt.replace("!", "")
            self.btn.setText(txt)


    def set_comment(self, comment_edit):
        txt = comment_edit.text()
        self.comment_rows[comment_edit] = txt
        

    def _add_comment(self, txt=""):
        row_layout = QHBoxLayout()
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.addWidget(QLabel("//"), stretch=0)

        comment_edit = QLineEdit(txt)
        comment_edit.setContentsMargins(0, 0, 0, 0)
        comment_edit.editingFinished.connect(
            lambda *_, c=comment_edit: self.set_comment(c)
        )
        row_layout.addWidget(comment_edit, stretch=1)
        self.set_comment(comment_edit)

        del_btn = QPushButton("🗑")
        del_btn.clicked.connect(lambda *_, c=comment_edit: self.delete_comment(c))
        row_layout.addWidget(del_btn, stretch=0)

        add_btn = QPushButton("+^")
        add_btn.clicked.connect(
            lambda *_, i=len(self.comment_rows):
            self.insert_comment(idx=i)
        )
        row_layout.addWidget(add_btn, stretch=0)

        self.main_layout.addLayout(row_layout)
        self.row_layouts[comment_edit] = row_layout

        if hasattr(self, "btn"):
            txt = self.btn.text()
            if "!" not in txt:
                txt = "!" + txt
                self.btn.setText(txt)

    def insert_comment(self, txt="", idx=None):
        cut = []
        if idx is not None:
            for comment, text in zip(
                list(self.comment_rows.keys())[idx-1:],
                list(self.comment_rows.values())[idx-1:]):
                self.delete_comment(comment)
                cut.append(text)
        
        self._add_comment(txt)
        for text in cut:
            self._add_comment(text)

    def clear_comments(self):
        for comment in list(self.comment_rows.keys()):
            self.delete_comment(comment)

    def refresh_view(self):
        self.clear_comments()
        
        self.comment_rows = {}

        for txt in self.get_comments():
            self._add_comment(txt)


