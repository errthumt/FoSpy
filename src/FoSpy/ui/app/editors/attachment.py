from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog
)
from PySide6.QtCore import Qt

from ._base import BasePropEditor


class FilePathPanel(QWidget):
    def __init__(self, block_widget):
        super().__init__()

        self.blk_widget = block_widget
        self.selected_path = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # --- Row: label + non-editable path display + choose button ---
        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)

        row.addWidget(QLabel("File Path:"), stretch=0)

        self.path_display = QLineEdit()
        self.path_display.setReadOnly(True)
        self.path_display.setFocusPolicy(Qt.NoFocus)
        row.addWidget(self.path_display, stretch=1)

        self.choose_btn = QPushButton("Choose…")
        self.choose_btn.clicked.connect(self.choose_file)
        row.addWidget(self.choose_btn, stretch=0)

        layout.addLayout(row)

        self.refresh()

    # ------------------------------------------------------------
    # Public API for the editor
    # ------------------------------------------------------------

    def refresh(self):
        """Refresh display from the block."""
        if self.blk_widget.blk.find_fileblock()._sourceFile is not None:
            current = self.blk_widget.blk._get_filepath()
            self.selected_path = current
            self.choose_btn.setEnabled(True)
            self.path_display.setEnabled(True)
        else:
            current = "<Path cannot be set until the parent FoS file is saved>"
            self.choose_btn.setEnabled(False)
            self.path_display.setEnabled(False)
        self.path_display.setText(str(current))

    def get_selected_path(self) -> Path:
        """Return the selected path as a Path object."""
        return Path(self.selected_path) if self.selected_path else None

    # ------------------------------------------------------------
    # Internal behavior
    # ------------------------------------------------------------

    def choose_file(self):
        """Open a file dialog and update the display."""
        path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if path:
            self.selected_path = path
            self.path_display.setText(path)


class FilePathEditor(BasePropEditor):
    def __init__(self, block_widget, line_edit, on_apply=None):
        panel = FilePathPanel(block_widget)

        # BasePropEditor signature:
        # BasePropEditor(block_widget, line_edit, editor_widget, on_apply)
        super().__init__(block_widget, line_edit, panel, on_apply)

    # ------------------------------------------------------------
    # Stub apply method — you fill in the real logic later
    # ------------------------------------------------------------

    def apply(self):
        """
        Pull the selected path from the panel, convert to Path,
        process it, then eventually set attributes on self.blk_widget.blk.
        """
        path_obj = self.editor.get_selected_path()

        # Example processing stub:
        # (You replace this with your real logic)
        if path_obj is not None:
            print("Selected path:", path_obj)
            # e.g. self.blk_widget.blk.filepath = path_obj

        # Call BaseEditorWidget.apply() to run on_apply + hint + refresh
        super().apply()

    def is_changed(self):
        return self.editor.get_selected_path() != self.line_edit.text()
