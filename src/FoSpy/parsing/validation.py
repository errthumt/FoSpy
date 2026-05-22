from .._debug import Debug
_debug = Debug()

from ..blocks.blocks import *
from ..blocks.embedded import *
from ..blocks.materials import *
from ..blocks.metadata import *
from ..blocks.synthesis import *
from ..blocks.template import *
from ..blocks.treatments import *

from ..blocks.synthesis import Synthesis
from . import validators

from chemformula import ChemFormula

TreatmentList = ListBlock.Simple(Treatment)
ExperimenterList = ListBlock.Simple(Experimenter)
CifList = ListBlock.Simple(EmbeddedCIF)

TemplateLists = {
    "experimenters": TemplateList.Simple(Experimenter),
    "materials": TemplateList.Simple(Material),
    "treatments": TemplateList.Simple(Treatment),
    "annealings": TemplateList.Simple(Annealing),
    "anneal_sections": TemplateList.Simple(AnnealSection),
    "cifs": CifList
}

aliases = {
    "material": Material,
    "materials": MaterialList,
    "treatment": Treatment,
    "treatments": TreatmentList,
    "experimenter": Experimenter,
    "experimenters": ExperimenterList,
}

required_keys = {
    SingleBlock: {
        "ext" : SubContainer
    },

    Synthesis: {
        "metadata" : MetaData,
        "experimenters": ExperimenterList,
        "reaction" : Reaction,
        "materials" : MaterialList,
        "treatments" : TreatmentList
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
        "date": str
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
        "time": str
    },

    Ramp: {
        "temp": str
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

    TemplateSet: TemplateLists
}