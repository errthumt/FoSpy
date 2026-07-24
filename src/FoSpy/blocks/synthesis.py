
from .files import FileBlock

from .._debug import Debug
_debug = Debug()

@FileBlock.register_dispatch("synthesis", defaults={"metadata":{"fos_type":"synthesis"}})
@FileBlock.register_dispatch(None)
class Synthesis(FileBlock):
    """
    Represents a Synthesis loaded from a FOS file.
    """
    dispatch_from = FileBlock

    def insert_material(self, mat, idx=-1):
        # placeholder. modify for insertion at idx
        self.materials.append(mat)

    def insert_treatment(self, treat, idx=-1):
        # placeholder. modify for insertion at idx
        self.treatments.append(treat)

    