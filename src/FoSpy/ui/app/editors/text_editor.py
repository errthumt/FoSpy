from ._base import BasePropEditor
from PySide6.QtWidgets import QPlainTextEdit

class TextEditorWidget(BasePropEditor):
    def __init__(self, block_widget, line_edit, on_apply):
        super().__init__(block_widget, line_edit, QPlainTextEdit(), on_apply)

    def refresh_editor(self):
        self.editor.setPlainText(self.line_edit.text())
        self.line_edit.setCursorPosition(0)

    def apply(self):
        self.line_edit.setText(self.editor.toPlainText())
        super().apply()