from .._debug import Debug
_debug = Debug()

from ..blocks import *
from ..blocks.synthesis import Synthesis
from . import validators

from chemformula import ChemFormula

required_keys = {
    Synthesis: {
        "metadata" : MetaData,
        "reaction" : Reaction,
        "materials" : MaterialList,
        "treatments" : TreatmentList
    },

    MetaData: {
        "name": str,
        "date": str,
        "experimenters": ExperimenterList
    },

    Experimenter: {
        "name" : str,
        "affiliation": str
    },

    Reaction: {
        "nominal_formula": ChemFormula,
        "nominal_mass" : validators.reaction.nominal_mass,
        "nominal_mass_units": validators.units.mass_unit("Reaction/nominal_mass_units")
    },

    Material: {
        "name": str,
        "type": str,
        "formula": ChemFormula,
        "supplier": str,
        "cas": str,
        "form": str,
        "env": str,
        "ratio": validators.material.ratio
    },

    Treatment: {
        "type": str,
        "repeats": int,
        "observations": str
    },

    AnnealSection: {
        "type": str,
        "time": str,
    },

    Annealing: {
        "program": AnnealProgram
    }
}

optional_keys = {
    Experimenter: {
        "orcid" : str
    },

    Material : {
        "purity" : validators.material.purity("Material"),
        "treatments": TreatmentList
    },

    Treatment: {
        "program": AnnealProgram
    },

    AnnealSection: {
        "temp": str
    }
}