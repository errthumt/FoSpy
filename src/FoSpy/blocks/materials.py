from . import (
    SingleBlock, ListBlock, 
    TemplateBlock, TemplateList,
    calc_routine)
from .._debug import Debug
_debug = Debug()
_debug.on = True

class Material(SingleBlock):
    def __init__(self, blockDict):
        super().__init__(blockDict)

    @calc_routine
    def example_calc(self):
        _debug.msg(f"Running example calc routine for material: {self.name}")
        return None

class MaterialTemplate(Material, TemplateBlock):
    def __init__(self, blockDict):
        super().__init__(blockDict)

class MaterialList(ListBlock):
    def __init__(self, blockList, cls=Material):
        super().__init__(blockList, cls)

    def calc_weight_pcts(self, typ=None):
        from decimal import Decimal
        
        weights = {}
        for mat in self._objs:
            if mat.type == typ or typ is None:
                ratio = mat.ratio
                mw = mat.formula.formula_weight
                weights[mat] = ratio * Decimal(mw)

        percents = {}
        total_weight = sum(weights.values())
        for mat, wt in weights.items():
            pct = 100 * wt / total_weight
            percents[mat] = pct
        return percents
    
    @calc_routine
    def add_weight_pcts(self, typ=None):
        for mat, pct in self.calc_weight_pcts(typ).items():
            label = typ.capitalize() if typ else "Total"
            comment = f"{label} weight percent: {pct:.2f}%"
            _debug.msg(f"Calculated {label} weight percent: {pct:.2f}% for {mat.name}")
            mat.add_calc_comment("ratio",comment, f"{label}_pct")

class MatTempList(MaterialList, TemplateList):
    def __init__(self, blockDict):
        super().__init__(blockDict, MaterialTemplate)
