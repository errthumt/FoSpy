from ._blockUtils import _calc_routine
from .blocks import SingleBlock

from .._debug import Debug
_debug = Debug()

class Chemical(SingleBlock):
    """
    An abbreviated reference to a material, product, or chemical composition.

    This class is the bare minimum for identifying a chemical composition.
    Additional requirements are enforced for various subclasses, including
    `Material` and `Product`.
    """
    @_calc_routine
    def add_MW(self):
        """
        Attach a comment to the formula with molecular weight.
        """
        _debug.msg(f"Adding molecular weight to chemical: {self.formula}")
        mw = self.formula.formula_weight
        self.add_calc_comment("formula",f"Molecular Weight: {mw:.2f} g/mol", "add_MW")