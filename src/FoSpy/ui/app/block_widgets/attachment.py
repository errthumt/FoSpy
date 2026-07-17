from ._base import SingleBlockWidget
from .. import editors as ed

class PathFileWidget(SingleBlockWidget):
    prop_map = {
        "file_name": (
            ed.attachment.FilePathEditor,
            lambda value: False
        ),
        "path": (
            False,
            lambda value: False
        )
    }