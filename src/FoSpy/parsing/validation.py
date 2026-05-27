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

# Placeholder classes
class LabConditions(SingleBlock):
    pass

class Equipment(SingleBlock):
    pass

EquipmentList = ListBlock.Simple(Equipment)



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
    "embed": EmbeddedFile
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
        "nominal_mass" : validators.numbers.positive_decimal("Reaction/nominal_mass"),
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
        "type": str
    },

    RampNoRate: {
        "temp": validators.numbers.positive_decimal("RampNoRate/temp") ,
        "time": validators.numbers.positive_decimal("RampNoRate/time"),
        "temp_units": validators.units.temp_units,
        "time_units": validators.units.time_units
    },

    RampNoTime: {
        "temp": validators.numbers.positive_decimal("RampNoTime/temp"),
        "rate": validators.numbers.positive_decimal("RampNoTime/rate"),
        "temp_units": validators.units.temp_units,
        "rate_units": validators.units.rate_units
    },

    RampNoTemp: {
        "time": validators.numbers.positive_decimal("RampNoTemp/time"),
        "rate": validators.numbers.positive_decimal("RampNoTemp/rate"),
        "time_units": validators.units.time_units,
        "rate_units": validators.units.rate_units   
    },

    Dwell: {
        "time": validators.numbers.positive_decimal("Dwell/time"),
        "time_units": validators.units.time_units
    },

    Quench: {
        "medium": str
    },

    Annealing: {
        "program": AnnealProgram
    },

    EmbeddedFile: {
        "file_name": validators.filenames.file_name,
        "extension": validators.filenames.file_extension,
        "embedded" : list
    }
}

optional_keys = {
    SingleBlock: {
        "rename": validators.rename.rename_dict
    },
    Synthesis: {
        "cif": EmbeddedCIF,
        "cifs": ListBlock.Simple(EmbeddedCIF),
        "laboratory_conditions": LabConditions,
        "equipment": EquipmentList
    },

    Experimenter: {
        "orcid" : str
    },

    Material : {
        "purity" : validators.material.purity("Material"),
        "treatments": ListBlock.Simple(Treatment)
    },

    Treatment: {
        "program": ListBlock.Simple(AnnealSection),
        "recovered_mass": validators.numbers.positive_decimal("Treatment/recovered_mass"),
        "start_time": str,
        "end_time": str
    },

    TemplateSet: TemplateLists
}