from ._base import BaseEditorWidget
from PySide6.QtWidgets import QPlainTextEdit

class TextEditorWidget(BaseEditorWidget):
    def __init__(self, parent_widget):
        super().__init__(parent_widget, QPlainTextEdit())

    def refresh_editor(self):
        self.editor.setPlainText(self.parent_ref.text())