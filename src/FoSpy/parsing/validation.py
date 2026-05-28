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
ProductList = ListBlock.Simple(Product)
CifList = ListBlock.Simple(EmbeddedCIF)

# Placeholder classes
class LabConditions(SingleBlock):
    pass

class Equipment(SingleBlock):
    pass

class GasFlow(SingleBlock):
    pass

EquipmentList = ListBlock.Simple(Equipment)
FlowList = ListBlock.Simple(GasFlow)


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
        "products": ProductList,
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
        "nominal_mass" : validators.numbers.positive_decimal("Reaction/nominal_mass", "nominal_mass"),
        "nominal_mass_unit": validators.units.mass_unit("Reaction/nominal_mass_units")
    },

    Product: {
        "name": str,
        "expected" : bool,
        "obtained" : bool,
        "formula": ChemFormula,
        "observations": str
    },

    Material: {
        "name": str,
        "type": str,
        "formula": ChemFormula,
        "supplier": str,
        "cas": str,
        "form": str,
        "env": str,
        "amount": validators.numbers.positive_decimal("Material/amount", "amount"),
        "amount_unit": str
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
        "temp": validators.numbers.positive_decimal("RampNoRate/temp", "temp", True) ,
        "time": validators.numbers.positive_decimal("RampNoRate/time", "time", True),
        "temp_unit": validators.units.FOSTempUnit,
        "time_unit": validators.units.FOSUnit.enforce_dims("[time]")
    },

    RampNoTime: {
        "temp": validators.numbers.positive_decimal("RampNoTime/temp", "temp", True),
        "rate": validators.numbers.positive_decimal("RampNoTime/rate", "rate", True),
        "temp_unit": validators.units.FOSTempUnit,
        "rate_unit": validators.units.temp_rate_unit 
    },

    RampNoTemp: {
        "time": validators.numbers.positive_decimal("RampNoTemp/time", "time", True),
        "rate": validators.numbers.positive_decimal("RampNoTemp/rate", "rate", True),
        "time_unit": validators.units.FOSUnit.enforce_dims("[time]"),
        "rate_unit": validators.units.temp_rate_unit  
    },

    Dwell: {
        "time": validators.numbers.positive_decimal("Dwell/time", "time", True),
        "time_unit": validators.units.FOSUnit.enforce_dims("[time]")
    },

    Quench: {
        "medium": str
    },

    Annealing: {
        "program": AnnealProgram,
        "start_temp": validators.numbers.positive_decimal("Annealing/start_temp", "start_temp", True),
        "start_temp_unit": validators.units.FOSTempUnit
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

    Product: {
        "expected_amount": validators.numbers.positive_decimal("Product/expected_amount", "expected_amount", require_unit=True),
        "expected_amount_unit": validators.units.FOSUnit.enforce_dims(["[mass]",{"[length]":3}]),
        "obtained_amount": validators.numbers.positive_decimal("Product/obtained_amount", "obtained_amount", require_unit=True),
        "obtained_amount_unit": validators.units.FOSUnit.enforce_dims(["[mass]",{"[length]":3}]),
        "characterizations": str,
        "structure_comments": str
    },

    Material : {
        "purity" : validators.numbers.decimal_range("Material/purity","purity", 0, 1),
        "treatments": ListBlock.Simple(Treatment)
    },

    Treatment: {
        "program": ListBlock.Simple(AnnealSection),
        "recovered_mass": validators.numbers.positive_decimal("Treatment/recovered_mass", "recovered_mass"),
        "start_time": str,
        "end_time": str
    },

    Annealing: {
        "gas_flow": FlowList
    },

    TemplateSet: TemplateLists
}