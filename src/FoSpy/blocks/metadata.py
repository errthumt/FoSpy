from .blocks import SingleBlock
from ._blockUtils import _calc_routine
from .template import TemplateBlock

from .._debug import Debug
_debug = Debug()

class MetaData(SingleBlock):
    """
    Represents metadata for a synthesis.

    Any key:value pairs at the top of a FOS file will automatically be assigned
    to metadata
    """
    pass

class TemplateMeta(SingleBlock):
    """
    Represents metadata for a set of templates loaded from a FOS file.

    Required metadata for a template file may be different than required
    metadata for a synthesis file.

    Any key:value pairs at the top of a FOS file will automatically be assigned
    to metadata
    """
    pass

class Reaction(SingleBlock):
    """
    Represents information pertaining to the entire synthesis but not pertaining
    to FOS file metadata, such as nominal_mass or target_composition.
    """

    def get_nom_MW(self):
        """Returns the molecular weight of nominal_formula"""
        return self.nominal_formula.formula_weight
    
    @_calc_routine()
    def add_nom_MW(self):
        """
        Attaches a comment to the nominal_formula with the molecular weight.
        """
        mw = self.get_nom_MW()
        _debug.msg(f"Calculated Nominal MW: {mw:.2f} for Reaction block.")
        self.add_calc_comment("nominal_formula",f"Nominal MW: {mw:.2f} g/mol","Nominal MW")

class Experimenter(SingleBlock):
    """
    Represents an an experimenter who worked on a synthesis.
    """
    pass

class ExpTemplate(Experimenter, TemplateBlock):
    """
    Represents an experimenter who frequently performs syntheses and is
    attached to multiple FOS files.
    """
    pass
