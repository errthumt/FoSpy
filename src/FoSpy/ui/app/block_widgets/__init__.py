
from ....blocks import SingleBlock, ListBlock, PathFile

from .. import editors

from ._base import SingleBlockWidget, ListBlockWidget
from . import (
    attachment
)

widget_map = {
    str:(
        editors.text_editor.TextEditorWidget,
        lambda value: "\n" not in value
    ),
    PathFile: attachment.PathFileWidget
}

# assign defaults last
widget_map[SingleBlock] = SingleBlockWidget
widget_map[ListBlock] = ListBlockWidget



