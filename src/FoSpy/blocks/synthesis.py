
from .blocks import FileBlock

from .._debug import Debug
_debug = Debug()

class Synthesis(FileBlock):
    """
    Represents a Synthesis loaded from a FOS file.
    """
    def __init__(self, blockDict, _sourceFile=None):
        super().__init__(blockDict, _sourceFile)

    def insert_material(self, mat, idx=-1):
        # placeholder. modify for insertion at idx
        self.materials.append(mat)

    def insert_treatment(self, treat, idx=-1):
        # placeholder. modify for insertion at idx
        self.treatments.append(treat)
    