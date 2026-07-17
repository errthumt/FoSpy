from ._base import SingleBlockWidget
from ..editors.rename import RenameEditorWidget

class RenameWidget(SingleBlockWidget):
    prop_map = {
        "__all__": (
            False,
            lambda value: False
        )
    }

    def __init__(self, label, blk, window):
        super().__init__(label, blk, window)

        self.main_editor = RenameEditorWidget(self)

        self._register_misc_editor(self.main_editor, "Rename Properties", RenameEditorWidget.editor_id)

        self.activate_misc_editor(RenameEditorWidget.editor_id)
        