from PySide6.QtWidgets import (
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QWidget,
    QLabel
)

class BaseEditorWidget(QWidget):
    def __init__(self, block_widget, editor_widget):
        super().__init__()

        self.blk_widget = block_widget

        self.base_layout = QVBoxLayout(self)
        self.base_layout.setContentsMargins(0, 0, 0, 0)
        self.base_layout.setSpacing(10)

        self.editor = editor_widget
        self.refresh_editor()
        self.base_layout.addWidget(self.editor, stretch=0)

        self.setLayout(self.base_layout)

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

        self.base_layout.addLayout(button_layout, stretch=0)

        self.hintPanel = QVBoxLayout()
        self.hintLabel = QLabel()
        self.hintButton = QPushButton("More...")

        self.hintPanel.addWidget(self.hintLabel)
        self.hintPanel.addWidget(self.hintButton)
        self.hintButton.hide()
        self.hintPanel.addStretch()

        self.base_layout.addLayout(self.hintPanel, stretch=1)

        self.setLayout(self.base_layout)

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
            self.hint(str(e), "Failed to apply changes:", exc=e)
        self.refresh_editor()

    def refresh_editor(self):
        pass

    def hint(self, text="", header=None, exc=None):

        txt = f"<h4>{header}</h4>\n" if header else ""

        txt += text

        self.hintLabel.setText(txt)

        if exc is not None:
            self.hintButton.show()

            def raise_exc(*_, e=exc):
                raise e

            self.hintButton.clicked.connect(raise_exc)
        else:
            self.hintButton.hide()

    def _hard_refresh(self, func:callable=lambda:None):
        from ..window import WIDGET_DATA_ROLE
        from .comments import CommentEditorWidget

        blk = self.blk_widget.blk
        parent = blk._parent_block if hasattr(blk, "_parent_block") else None
        win = self.blk_widget.win

        if (self.blk_widget.active.count() > 1 and
            not win._custom_popup(
                "Warning!",
                "This change requires a refresh of the entire window for this block. "
                "You will lose changes made in other editor tabs.\n\n"
                "Continue?",
                ("Apply Changes and Refresh", True),
                cancel=True
        )):
            return

        func()

        # Refresh tree
        win.refresh_tree(blk._parent_block if hasattr(blk, "_parent_block") else None)
        win.go_to_block(parent)
        win.go_to_block(blk)

        # This editor is desynced. Find new editor
        tree_item = win.tree_items[blk]
        blk_widget = tree_item.data(WIDGET_DATA_ROLE)["widget"]

        # If block is in ListBlock, it's widget is stored in ListBlockWidget
        if blk_widget is None:
            listblk_item = win.tree_items[parent]
            listblk_widget = listblk_item.data(WIDGET_DATA_ROLE)["widget"]
            blk_widget = listblk_widget.blk_widgets[blk]
            
        if isinstance(self, BasePropEditor):
            blk_widget.activate_prop_editor(self.prop_name)
        elif isinstance(self, CommentEditorWidget):
            blk_widget.activate_comment_editor(self.editor.prop_name)
        else:
            blk_widget.activate_misc_editor(self.editor_id)

        return blk_widget


class BasePropEditor(BaseEditorWidget):
    def __init__(self, block_widget, line_edit, editor_widget, on_apply, prop_name):
        self.on_apply = on_apply
        self.line_edit = line_edit
        self.prop_name = prop_name

        super().__init__(block_widget, editor_widget)


