from .blocks import SingleBlock, ListBlock
from .. import inherit_class_doc, inherit_docstring

@inherit_class_doc(SingleBlock)
class EmbeddedFile(SingleBlock):
    """
    Represents an non-FOS file embedded as a block in a FOS file.
    """
    def __init__(self, blockDict):
        super().__init__(blockDict)

    @inherit_docstring(SingleBlock)
    def serialize(self):
        """
        Performs the default `SingleBlock` serialization, but restores the
        "embedded" key to the full list of embedded lines instead of a string.
        """
        serial = super().serialize()
        serial[0]["embedded"] = self.embedded.copy()
        return serial


@inherit_class_doc(EmbeddedFile)
class EmbeddedCIF(EmbeddedFile):
    """
    Represents a CIF file embedded as a block in a FOS file.
    """
    def __init__(self, blockDict):
        super().__init__(blockDict)
