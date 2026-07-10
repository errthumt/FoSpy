
from ..blocks._containers import SubContainer
from .. import blocks as b


from . import validators
import chemformula

from .._debug import Debug
_debug = Debug()



TemplateLists = {
    "experimenters": b.TemplateList.Simple(b.Experimenter),
    "materials": b.TemplateList.Simple(b.Material),
    "treatments": b.TemplateList.Simple(b.Treatment),
    "annealings": b.TemplateList.Simple(b.Annealing),
    "anneal_sections": b.TemplateList.Simple(b.AnnealSection),
    "cifs": b.CifList
}
"""Maps alias names to [`TemplateList`][FoSpy.blocks.template.TemplateList] classes for use in
[`TemplateSet`][FoSpy.blocks.template.TemplateSet] blocks."""


aliases = {
    "material": b.Material,
    "materials": b.MaterialList,
    "treatment": b.Treatment,
    "treatments": b.TreatmentList,
    "experimenter": b.Experimenter,
    "experimenters": b.ExperimenterList,
    "embed": b.EmbeddedFile
}
"""Maps alias names to block classes for use in non-template
[`SingleBlock`][FoSpy.blocks.blocks.SingleBlock] blocks."""

required_keys = {
    b.SingleBlock: {
            "ext" : SubContainer
    },

    b.FileBlock: {
        "metadata" : b.MetaData
    },

    b.Synthesis: {
        "metadata" : b.SynthesisMeta,
        "experimenters": b.ExperimenterList,
        "reaction" : b.Reaction,
        "products": b.ProductList,
        "materials" : b.MaterialList,
        "treatments" : b.TreatmentList
    },

    b.TemplateBlock: {
        "template_name" : str
    },

    b.MetaData: {
        "fos_id": str,
        "fos_type": str,
        "description": str
    },

    b.SynthesisMeta: {
        "group_id": str,
        "project_id": str
    },

    b.Experimenter: {
        "name" : str,
        "affiliation": str
    },

    b.Reaction: {
        "nominal_formula": chemformula.ChemFormula,
        "nominal_amount" : validators.numbers.positive_decimal("Reaction/nominal_amount", "nominal_amount"),
        "nominal_amount_unit": validators.units.FOSUnit.enforce_dims(["[mass]",{"[length]":3}]) # TODO: single validator instance for enforcing amount units.
    },

    b.Chemical: {
        "formula": chemformula.ChemFormula
    },

    b.ChemChange: {
        "amount": validators.numbers.positive_decimal("b.Chemical/amount", "amount"),
        "amount_unit": str # TODO: enforce units after formalization of moles and molar ratios.
    },

    b.Product: {
        "name": str,
        "expected" : bool,
        "obtained" : bool,
        "observations": str,
    },

    b.Material: {
        "name": str,
        "type": str,
        "formula": True,
        "supplier": str,
        "cas": str,
        "form": str,
        "env": str,
        "amount": validators.numbers.positive_decimal("b.Chemical/amount", "amount"),
        "amount_unit": str # TODO: enforce units after formalization of moles and molar ratios.
    },

    b.Treatment: {
        "type": str,
        "repeats": int,
    },

    b.CompChange: {
        "repeats": False,
        "changes": b.ChemChangeList
    },

    b.AnnealSection: {
        "type": str
    },

    b.Dwell: {
        "time": validators.numbers.positive_decimal("Dwell/time", "time", True),
        "time_unit": validators.units.FOSUnit.enforce_dims("[time]")
    },

    b.Quench: {
        "medium": str
    },

    b.Annealing: {
        "program": b.AnnealProgram,
        "start_temp": validators.numbers.positive_decimal("b.Annealing/start_temp", "start_temp", True),
        "start_temp_unit": validators.units.FOSTempUnit
    },

    b.Attachment: {
        "file_name": validators.filenames.file_name
    }
}
"""Maps block classes to dictionaries of required keys and their validators.
Validators can be types (e.g. `str`, `int`),
[`Block`][FoSpy.blocks.blocks.Block] constructors, or custom validator
functions."""


optional_keys = {
    b.Attachment: {
        "embedded": validators.filenames.embedded,
        "path": validators.filenames.PathPosix
    }, 
    b.SingleBlock: {
        "rename": validators.rename.rename_dict
    },
    b.Synthesis: {
        "cif": b.Attachment.enforce_subtype(b.CIFFile),
        "cifs": b.CifList,
        "laboratory_conditions": b.LabConditions,
        "equipment": b.EquipmentList
    },

    b.Experimenter: {
        "orcid" : str
    },

    b.Product: {
        "expected_amount": validators.numbers.positive_decimal("Product/expected_amount", "expected_amount", require_unit=True),
        "expected_amount_unit": validators.units.FOSUnit.enforce_dims(["[mass]",{"[length]":3}]),
        "obtained_amount": validators.numbers.positive_decimal("Product/obtained_amount", "obtained_amount", require_unit=True),
        "obtained_amount_unit": validators.units.FOSUnit.enforce_dims(["[mass]",{"[length]":3}]),
        "characterizations": str,
        "structure_comments": str
    },

    b.Material : {
        "purity" : validators.numbers.decimal_range("b.Material/purity","purity", 0, 1),
        "treatments": b.TreatmentList
    },

    b.Treatment: {
        "observations": str,
        "recovered_amount": validators.numbers.positive_decimal("b.Treatment/recovered_amount", "recovered_amount", True),
        "recovered_amount_unit": validators.units.FOSUnit.enforce_dims(["[mass]",{"[length]":3}]), 
        "start_time": str,
        "end_time": str
    },

    b.Annealing: {
        "gas_flow": b.FlowList
    },

    b.Ramp: {
        "temp": validators.numbers.positive_decimal("RampNoRate/temp", "temp", True) ,
        "time": validators.numbers.positive_decimal("RampNoRate/time", "time", True),
        "rate": validators.numbers.any_decimal("RampNoTemp/rate", "rate", True),
        "temp_unit": validators.units.FOSTempUnit,
        "time_unit": validators.units.FOSUnit.enforce_dims("[time]"),
        "rate_unit": validators.units.temp_rate_unit
    },

    b.TemplateSet: TemplateLists
}
"""
Maps block classes to dictionaries of optional keys and their validators.
Validators can be types (e.g. `str`, `int`),
[`Block`][FoSpy.blocks.blocks.Block] constructors, or custom validator
functions.

Optional key mapping is only necessary if the expected value should be passed to
a validator. Simple unexpected values can be assigned directly to
[`SingleBlock`][FoSpy.blocks.blocks.SingleBlock] instance attributes
without validation.
"""