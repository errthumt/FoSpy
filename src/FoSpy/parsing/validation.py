from .._debug import Debug
_debug = Debug()

from ..blocks import *
from ..blocks.synthesis import Synthesis
from . import validators

from chemformula import ChemFormula

required_keys = {
    SingleBlock: {
        "ext" : SubContainer
    },

    Synthesis: {
        "metadata" : MetaData,
        "reaction" : Reaction,
        "materials" : MaterialList,
        "treatments" : ListBlock.Simple(Treatment)
    },

    TemplateSet: {
        "metadata" : TemplateMeta
    },

    TemplateMeta: {
        "name" : str,
        "description" : str
    },

    TemplateBlock: {
        "template_name" : str
    },

    MetaData: {
        "name": str,
        "date": str,
        "experimenters": ListBlock.Simple(Experimenter)
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
        "program": ListBlock.Simple(AnnealSection)
    },

    EmbeddedFile: {
        "file_name": str,
        "extension": str,
        "embedded" : list
    }
}

optional_keys = {
    Synthesis: {
        "cif": EmbeddedCIF,
        "cifs": ListBlock.Simple(EmbeddedCIF)
    },

    Experimenter: {
        "orcid" : str
    },

    Material : {
        "purity" : validators.material.purity("Material"),
        "treatments": ListBlock.Simple(Treatment)
    },

    Treatment: {
        "program": ListBlock.Simple(AnnealSection)
    },

    AnnealSection: {
        "temp": str
    },

    TemplateSet: {
        "materials": MatTempList,
        "treatments": ListBlock.Simple(TreatmentTemplate),
        "experimenters": ListBlock.Simple(ExpTemplate)
    }
}