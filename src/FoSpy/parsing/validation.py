from .._debug import Debug
_debug = Debug()

from ..blocks.blocks import (
    ListBlock,
    SingleBlock,
    SubContainer,
)

from ..blocks.embedded import (
    EmbeddedCIF,
    EmbeddedFile,
)

from ..blocks.materials import (
    Material,
    MaterialList,
    TemplateBlock,
    TemplateList,
)

from ..blocks.metadata import (
    Experimenter,
    MetaData,
    Product,
    Reaction,
    TemplateMeta,
)

from ..blocks.synthesis import (
    Synthesis,
)

from ..blocks.template import (
    TemplateSet,
)

from ..blocks.treatments import (
    AnnealProgram,
    AnnealSection,
    Annealing,
    Dwell,
    Quench,
    Ramp,
    Treatment,
)

from . import validators
import chemformula


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

class TestBlock(SingleBlock):
    pass

EquipmentList = ListBlock.Simple(Equipment)
FlowList = ListBlock.Simple(GasFlow)

def default_TemplateLists():
    """
    Default dictionary for
    [`TemplateList`s][FoSpy.parsing.validation.TemplateLists]. Maps alias names
    to TemplateList classes for use in
    [`TemplateSet`][FoSpy.parsing.validation.TemplateSet] blocks.
    """
    return {
        "experimenters": TemplateList.Simple(Experimenter),
        "materials": TemplateList.Simple(Material),
        "treatments": TemplateList.Simple(Treatment),
        "annealings": TemplateList.Simple(Annealing),
        "anneal_sections": TemplateList.Simple(AnnealSection),
        "cifs": CifList
    }
TemplateLists = default_TemplateLists()
"""Maps alias names to [`TemplateList`][FoSpy.parsing.validation.TemplateLists] classes for use in
[`TemplateSet`][FoSpy.parsing.validation.TemplateSet] blocks."""


def default_aliases():
    return {
        "material": Material,
        "materials": MaterialList,
        "treatment": Treatment,
        "treatments": TreatmentList,
        "experimenter": Experimenter,
        "experimenters": ExperimenterList,
        "embed": EmbeddedFile
    }
aliases = default_aliases()
"""Maps alias names to block classes for use in non-template
[`SingleBlock`][FoSpy.parsing.validation.SingleBlock] blocks."""

def default_required():
    """
    Default dictionary for
    [`required_keys`][FoSpy.parsing.validation.required_keys]. Maps block
    classes to dictionaries of required keys and their validators. Validators
    can be types (e.g. `str`, `int`), [`Block`][FoSpy.blocks.blocks.Block]
    constructors, or custom validator functions.
    """
    return {
        TestBlock: {
            "test_key": str
        },
        SingleBlock: {
                "ext" : SubContainer
        },

        Synthesis: {
            "metadata" : MetaData,
            "experimenters": ExperimenterList,
            "reaction" : Reaction,
            "products": ProductList,
            "materials" : MaterialList,
            "treatments" : TreatmentList,
            "test": TestBlock
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
            "nominal_formula": chemformula.ChemFormula,
            "nominal_amount" : validators.numbers.positive_decimal("Reaction/nominal_amount", "nominal_amount"),
            "nominal_amount_unit": validators.units.FOSUnit.enforce_dims(["[mass]",{"[length]":3}])
        },

        Product: {
            "name": str,
            "expected" : bool,
            "obtained" : bool,
            "formula": chemformula.ChemFormula,
            "observations": str
        },

        Material: {
            "name": str,
            "type": str,
            "formula": chemformula.ChemFormula,
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

required_keys = default_required()
"""Maps block classes to dictionaries of required keys and their validators.
Validators can be types (e.g. `str`, `int`),
[`Block`][FoSpy.blocks.blocks.Block] constructors, or custom validator
functions."""

def default_optional():
    """
    Default dictionary for
    [`optional_keys`][FoSpy.parsing.validation.optional_keys]. Maps block
    classes to dictionaries of optional keys and their validators. Validators
    can be types (e.g. `str`, `int`), [`Block`][FoSpy.blocks.blocks.Block]
    constructors, or custom validator functions.

    Optional key mapping is only necessary if the expected value should be
    passed to a validator. Simple unexpected values can be assigned directly to
    [`SingleBlock`][FoSpy.parsing.validation.SingleBlock] instance attributes
    without validation.
    """
    return {
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
            "treatments": ListBlock.Simple(Treatment),
            "test": TestBlock
        },

        Treatment: {
            "recovered_amount": validators.numbers.positive_decimal("Treatment/recovered_amount", "recovered_amount", True),
            "recovered_amount_unit": validators.units.FOSUnit.enforce_dims(["[mass]",{"[length]":3}]), 
            "start_time": str,
            "end_time": str
        },

        Annealing: {
            "gas_flow": FlowList
        },

        Ramp: {
            "temp": validators.numbers.positive_decimal("RampNoRate/temp", "temp", True) ,
            "time": validators.numbers.positive_decimal("RampNoRate/time", "time", True),
            "rate": validators.numbers.any_decimal("RampNoTemp/rate", "rate", True),
            "temp_unit": validators.units.FOSTempUnit,
            "time_unit": validators.units.FOSUnit.enforce_dims("[time]"),
            "rate_unit": validators.units.temp_rate_unit
        },

        TemplateSet: TemplateLists
    }

optional_keys = default_optional()
"""
Maps block classes to dictionaries of optional keys and their validators.
Validators can be types (e.g. `str`, `int`),
[`Block`][FoSpy.blocks.blocks.Block] constructors, or custom validator
functions.

Optional key mapping is only necessary if the expected value should be passed to
a validator. Simple unexpected values can be assigned directly to
[`SingleBlock`][FoSpy.parsing.validation.SingleBlock] instance attributes
without validation.
"""