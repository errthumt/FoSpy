from PySide6.QtWidgets import (
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QWidget,
    QLabel
)



class BasePropEditor(QWidget):
    def __init__(self, block_widget, line_edit, editor_widget, on_apply):
        super().__init__()

        self.on_apply = on_apply
        self.blk_widget = block_widget
        self.line_edit = line_edit

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(10)

        self.editor = editor_widget
        self.refresh_editor()

        self.layout.addWidget(self.editor, stretch=0)

        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.apply_btn = QPushButton("Apply")
        self.apply_btn.clicked.connect(self.apply)
        button_layout.addWidget(self.apply_btn)

        self.okay_btn = QPushButton("OK")
        self.okay_btn.clicked.connect(self.ok)
        button_layout.addWidget(self.okay_btn)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.cancel)
        button_layout.addWidget(self.cancel_btn)

        self.layout.addLayout(button_layout, stretch=0)

        self.hintPanel = QLabel()
        self.layout.addWidget(self.hintPanel, stretch=1)

        self.setLayout(self.layout)

    def ok(self):
        self.apply()
        self.cancel()

    def cancel(self):
        self.refresh_editor()
        if hasattr(self, "blk_widget"):
            self.blk_widget.deactivate_editor(self)

    def apply(self):
        # subclass pushes content to line_edit, then calls super().apply()
        try:
            self.on_apply()
            self.hint()
        except Exception as e:
            self.hint(str(e), "Failed to apply changes:")
        self.refresh_editor()

    def hint(self, text="", header=None):

        txt = f"<h4>{header}</h4>\n" if header else ""

        txt += text

        self.hintPanel.setText(txt)

    def refresh_editor(self):
        pass
