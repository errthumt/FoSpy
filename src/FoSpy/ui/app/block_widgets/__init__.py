
from .... import blocks as b

from .. import editors

from ._base import SingleBlockWidget, ListBlockWidget
from . import (
    attachment,
    rename,
    template
)

__all__ = [
    "attachment",
    "rename",
    "template"
]

widget_map = {
    str:(
        editors.text_editor.TextEditorWidget,
        lambda value: "\n" not in value
    ),
    b.TemplateBlock: template.TemplateBlockWidget,
    b.PathFile: attachment.PathFileWidget,
    b.Rename: rename.RenameWidget
}

# assign defaults last
widget_map[b.SingleBlock] = SingleBlockWidget
widget_map[b.ListBlock] = ListBlockWidget



