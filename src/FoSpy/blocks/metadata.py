from . import SingleBlock, ListBlock

class MetaData(SingleBlock):
    def __init__(self, blockDict):
        super().__init__(blockDict)

class Reaction(SingleBlock):
    def __init__(self, blockDict):
        #placeholder assignment
        self.nominal_mass = blockDict["nominal_mass"]
        super().__init__(blockDict)

    def serialize(self):
        mw = self.get_nom_MW()
        self.add_calc_comment("nominal_formula",f"Nominal MW: {mw:.2f} g/mol","Nominal MW")
        return super().serialize()

    def get_nom_MW(self):
        return self.nominal_formula.formula_weight


class Experimenter(SingleBlock):
    def __init__(self, blockDict):
        super().__init__(blockDict)

class ExperimenterList(ListBlock):
    def __init__(self, blockList):
        super().__init__(blockList, Experimenter)