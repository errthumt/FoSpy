
from ....blocks import SingleBlock, ListBlock

from .. import editors

from ._base import SingleBlockWidget, ListBlockWidget

widget_map = {
    str:(
        editors.text_editor.TextEditorWidget,
        lambda value: "\n" not in value
    )
}

# assign defaults last
widget_map[SingleBlock] = SingleBlockWidget
widget_map[ListBlock] = ListBlockWidget



