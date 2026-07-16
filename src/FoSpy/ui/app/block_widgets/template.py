from ._base import SingleBlockWidget
from .. import editors as ed

class TemplateBlockWidget(SingleBlockWidget):
    def __init__(self, label, blk, window):
        super().__init__(label, blk, window)

    def _on_primitive_edit(self, prop, line_edit, enabler):
        # TODO: attempt to fill staged template here
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
            line_edit.setText(old_txt)
            error = e

        line_edit.setCursorPosition(0)

        if error is not None:
            raise error

        