
from .files import FileBlock

from .._debug import Debug
_debug = Debug()

class Synthesis(FileBlock):
    """
    Represents a Synthesis loaded from a FOS file.
    """

    def insert_material(self, mat, idx=-1):
        # placeholder. modify for insertion at idx
        self.materials.append(mat)

    def insert_treatment(self, treat, idx=-1):
        # placeholder. modify for insertion at idx
        self.treatments.append(treat)

from ._blockUtils import _get_block_classes
import sys
__block_classes__ = _get_block_classes(sys.modules[__name__])
"""List of all [`Block`][FoSpy.blocks.blocks.Block] classes defined in this module.
Used for generating documentation site."""
    