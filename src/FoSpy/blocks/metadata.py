from . import (
    SingleBlock, ListBlock, 
    TemplateBlock, TemplateList,
    calc_routine)
from .._debug import Debug
_debug = Debug()
_debug.on = True

class MetaData(SingleBlock):
    def __init__(self, blockDict):
        super().__init__(blockDict)

class TemplateMeta(SingleBlock):
    def __init__(self, blockDict):
        super().__init__(blockDict)

class Reaction(SingleBlock):
    def __init__(self, blockDict):
        #placeholder assignment
        self.nominal_mass = blockDict["nominal_mass"]
        super().__init__(blockDict)

    def get_nom_MW(self):
        return self.nominal_formula.formula_weight
    
    @calc_routine
    def add_nom_MW(self):
        mw = self.get_nom_MW()
        _debug.msg(f"Calculated Nominal MW: {mw:.2f} for Reaction block.")
        self.add_calc_comment("nominal_formula",f"Nominal MW: {mw:.2f} g/mol","Nominal MW")


class Experimenter(SingleBlock):
    def __init__(self, blockDict):
        super().__init__(blockDict)

class ExpTemplate(Experimenter, TemplateBlock):
    def __init__(self, blockDict):
        super().__init__(blockDict)

class ExperimenterList(ListBlock):
    def __init__(self, blockList, cls=Experimenter):
        super().__init__(blockList, cls)

class ExpTempList(ExperimenterList, TemplateList):
    def __init__(self, blockList):
        super().__inist__(blockList, ExpTemplate)