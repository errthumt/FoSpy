from .blocks import SingleBlock, ListBlock
from ._blockUtils import _calc_routine
from .template import TemplateBlock, TemplateList


from .._debug import Debug
_debug = Debug()

__block_classes__ = [
    "Material",
    "MaterialList"
]


class Material(SingleBlock):
    """
    Represents a material used in a synthesis
    """
    @_calc_routine()
    def add_MW(self):
        """
        Attach a comment to the formula with molecular weight.
        """
        _debug.msg(f"Adding molecular weight to Material: {self.name}")
        mw = self.formula.formula_weight
        self.add_calc_comment("formula",f"Molecular Weight: {mw:.2f} g/mol", "add_MW")

class MaterialList(ListBlock):
    """
    Represents a list of materials used in a synthesis
    """
    _reqCls = Material
    
    def calc_weight_pcts(self, typ=None):
        """
        Calculate weight percent for each material with matching type.

        Args:
            typ:
                Only materials with type attribute matching typ are considered
                in the total weight and given weight percents. This is useful
                if, for instance, you want weight percents of your contributing
                "reagents" without including "flux" or "solvent" materials.

        Returns:
            dict mapping material : weight_pct
        """
        from decimal import Decimal
        
        weights = {}
        for mat in self._objs:
            if mat.type == typ or typ is None:
                amount = mat.amount
                mw = mat.formula.formula_weight
                weights[mat] = amount() * Decimal(mw)

        percents = {}
        total_weight = sum(weights.values())
        for mat, wt in weights.items():
            pct = 100 * wt / total_weight
            percents[mat] = pct
        return percents
    
    
     
    @_calc_routine(attach=False)
    def add_all_MW(self):
        """
        Attach a molecular weight comment to all materials
        """
        for mat in self._objs:
            mat.add_MW()

    @_calc_routine()
    def add_weight_pcts(self, typ=None):
        """
        Calculate weight percents and attach them as comments to each material's amount.

        Args:
            typ:
                Only materials with type attribute matching typ are considered
                in the total weight and given weight percents. This is useful
                if, for instance, you want weight percents of your contributing
                "reagents" without including "flux" or "solvent" materials.
        """
        for mat, pct in self.calc_weight_pcts(typ).items():
            label = typ.capitalize() if typ else "Total"
            comment = f"{label} weight percent: {pct:.2f}%"
            _debug.msg(f"Calculated {label} weight percent: {pct:.2f}% for {mat.name}")
            mat.add_calc_comment("amount",comment, f"{label}_pct")

