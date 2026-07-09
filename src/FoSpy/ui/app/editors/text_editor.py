from ._base import BaseEditorWidget
from PySide6.QtWidgets import QPlainTextEdit

class TextEditorWidget(BaseEditorWidget):
    def __init__(self, block_widget, line_edit):
        super().__init__(block_widget, line_edit, QPlainTextEdit())

    def refresh_editor(self):
        self.editor.setPlainText(self.line_edit.text())