from .blocks import (
    SingleBlock, ListBlock
)

from ._blockUtils import _calc_routine

from .._debug import Debug
_debug = Debug()

@SingleBlock.setup_dispatch(
    from_key="fos_type",
    allow_self=True
)
class MetaData(SingleBlock):
    """
    Represents metadata for a FOS-formatted file.

    Any key:value pairs at the top of a FOS file will automatically be assigned
    to metadata
    """
    allow_rename = False

@MetaData.register_dispatch("synthesis",
    defaults = {
        "metadata": {
            "fos_type": "synthesis"
        }
    })
class SynthesisMeta(MetaData):
    pass

class Reaction(SingleBlock):
    """
    Represents information pertaining to the entire synthesis but not pertaining
    to FOS file metadata, such as nominal_mass or target_composition.
    """

    def get_nom_MW(self):
        """Returns the molecular weight of nominal_formula"""
        return self.nominal_formula.formula_weight
    
    @_calc_routine
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
    _id_key = "name"
    pass


ExperimenterList = ListBlock.Simple(Experimenter)
"""
A [simple list][FoSpy.blocks.blocks.ListBlock.Simple] of
[`Experimenter` objects][FoSpy.blocks.metadata.Experimenter].
"""

class LabConditions(SingleBlock):
    pass

class Equipment(SingleBlock):
    pass

EquipmentList = ListBlock.Simple(Equipment)


class Rename(SingleBlock):
    allow_rename = False
