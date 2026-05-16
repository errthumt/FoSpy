from . import SingleBlock, ListBlock

class Material(SingleBlock):
    def __init__(self, blockDict):
        super().__init__(blockDict)

class MaterialList(ListBlock):
    def __init__(self, blockList):
        super().__init__(blockList, Material)

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
    
    def add_weight_pcts(self, typ=None):
        for mat, pct in self.calc_weight_pcts("reagent").items():
            comment = f"Reagent weight percent: {pct:.2f}%"
            mat.add_calc_comment("ratio",comment, "reagent_pct")