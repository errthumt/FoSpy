# Object Construction and Property Validation for Files of Synthesis (FOS)

## Introduction

During construction of a parsed FOS into a Synthesis object, or when reassigning a property of an exising object, most classes have properties that should be expected in a certain format, or might contain nested objects with their own properties. The parsed properties are passed as either strings or (in the case of nested objects) a `list` or `dict` structure to the validation routine mapped to them in `FoSpy.parsing.validation.py`. In the case of nested objects, the validation routine is usually the constructor of the required object.

Classes can have required properties, which must be present at read time, or optional properties, which have validation routines but might not be expected for all syntheses.

During attribute assignment, expected properties are built up in order of parent classes. Any subclass inherits all the expected properties of its parent classes, but they may be overwritten to other validators.

## Dispatching Subclasses

Properties marked with (dispatched) are used to identify and delegate construction to the respective subclass. A class with a dispatch key is rarely constructed as itself, but may be used to inherit methods or required/optional properties.

## `ListBlock` and Simple Lists

`ListBlock` subclasses do not have required properties. Instead, they are a rich list of objects with a certain required `SingleBlock` subclass. Some `ListBlock` subclasses have their own methods and unique attributes. If a `ListBlock` is required for a given `SingleBlock` subclass but it doesn't need any method or attribute overrides, it can be instantiated with the class method `ListBlock.Simple(SingleBlockSubclass)` (referred to below as a "simple list").

### `TemplateList`s

`TemplateList` is a unique subclass of `ListBlock` used for storing [`TemplateBlock` subclass objects](#templateblock). `TemplateList` has a class method `Simple()` similar to `ListBlock`'s method, but instead of full objects (e.g. `Material`), it generates hybridized templates with fields for any field-marked or missing properties. Some syntax for `TemplateList` entries can be found in the [API script example](../examples/templates/index.md).

## Modifying Property Validation at Runtime

The intent of the FOS is to be as flexible as possible while still enforcing standards for fully capturing a synthetic method. However, it may be necessary for private or niche applications to modify standards to match your own synthesis. This can be done by mutating the dictionaries in `FoSpy.parsing.validation` at the start of your script. The example below creates a new block type with its own expected properties, and then adds it as an optional top-level block for a synthesis file.

These modifications should be reserved for very unique and isolated cases. If you are modifying standards in a significant way, or such that may be applicable for other researchers, consider reaching out to `FoSpy` developers or creating a fork of the API.

### Python

```python
import FoSpy.parsing.validation as vd
from FoSpy.blocks import (
    blocks.SingleBlock as SingleBlock
    synthesis.Synthesis as Synthesis
)


class MySpecialBlock(SingleBlock):
    pass

vd.required_keys[MySpecialBlock] = {
    "special_prop1": str
    "special_prop2": float
}

vd.optional_keys[Synthesis]["special"] = MySpecialBlock
```

### New FOS Block

```fos
[Special]
special_prop1: foobar
special_prop2: 6.022
```

______________________________________________________________________

# Expected Property Tables

## `AnnealSection`

[Class Documentation][FoSpy.blocks.treatments.AnnealSection]

**[Subclass of `SingleBlock`](#singleblock)**

### Required properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| type | `str` (dispatched) | Examples: `"dwell", "ramp", "quench"` |

______________________________________________________________________

## `Annealing`

**[Subclass of `Treatment`](#treatment)**

### Required properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| program | `AnnealProgram` | A [specialized `ListBlock`](#listblock-and-simple-lists) of [`AnnealSection` objects](#annealsection) |
| start_temp | `validators.numbers.positive_decimal` | The initial temperature of the annealing profile |
| start_temp_unit | `validators.units.FOSTempUnit` | `FOSTempUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) which allows a little more coersion of temperature units. (Like recognizing `"C"` as degrees celsius as opposed to coulombs)|

### Optional properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| gas_flow | `FlowList` | A [simple list](#listblock-and-simple-lists) of [`GasFlow` objects](#singleblock-method-subclasses) |

______________________________________________________________________

## `Dwell`

**[Subclass of `AnnealSection`](#annealsection)**

### Required properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| time | `validators.numbers.positive_decimal` | How long the temperature was kept constant in this section. |
| time_unit | `validators.units.FOSUnit.enforce_dims('[time]')` | `FOSUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) with a class method for enforcing the correct dimensionality of the unit. |

______________________________________________________________________

## `EmbeddedFile`

**[Subclass of `SingleBlock`](#singleblock)**

### Required properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| file_name | `validators.filenames.file_name` | Name of the embedded file |
| extension | `validators.filenames.file_extension` | File extension |
| embedded | `list` | A list of raw lines read directly from the FOS file which can be unpacked to a temporary file during runtime for reading as the original filetype. |

### `EmbeddedFile` Method Subclasses

These subclasses don't have any additional required properties but will either be given additional requirements in the future or have specialized methods.

- `EmbeddedCIF`

______________________________________________________________________

## `Experimenter`

**[Subclass of `SingleBlock`](#singleblock)**

### Required properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| name | `str` | Name of the experimenter |
| affiliation | `str` | Lab/University/Research Group/etc. |

### Optional properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| orcid | `str` | The experimenter's [ORCID](https://orcid.org/)|

______________________________________________________________________

## `Material`

**[Subclass of `SingleBlock`](#singleblock)**

### Required properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| name | `str` | Identifiable name for the material |
| type | `str` | How it was used in the synthesis (e.g., reagent, flux, solvent) |
| formula | `ChemFormula` | Chemical composition written in a [ChemFormula](https://pypi.org/project/chemformula/) compatible format |
| supplier | `str` | Source of purchase/synthesis (may be internal) |
| cas | `str` | CAS ID. May be "unknown"|
| form | `str` | Physical shape or state of the material **at time of acquisition** (e.g., powder, shot, wire, lump). If the material was modified after aquiring but before use in the synthesis (like grinding into powder, drying, etc.), these actions should be specified in the *material's* treatments property (not the synthesis treatments).|
| env | `str` | What environment the material is stored in. (e.g., ambient, Ar(g))|
| amount | `validators.numbers.positive_decimal` | Amount that was used. |
| amount_unit | `str` | Descriptive unit for amount. Dimensionality may be enforced in the future once more input is gained from experimenters.|

### Optional properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| purity | `validators.numbers.decimal_range` | 0 < purity \<= 1|
| treatments | `ListBlock.Simple(Treatment)` | A [simple list](#listblock-and-simple-lists) of [`Treatment` objects](#treatment)<br>Any modifications to the material between acquisition and use in the synthesis.|

______________________________________________________________________

## `MetaData`

**[Subclass of `SingleBlock`](#singleblock)**

### Required properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| name | `str` | Identifiable name for the synthesis or sample|
| date | `str` | What date the synthesis was started|

______________________________________________________________________

## `Product`

**[Subclass of `SingleBlock`](#singleblock)**

### Required properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| name | `str` | Identifiable name for the product. |
| expected | `bool` | Whether or not it was expected from the synthesis. |
| obtained | `bool` | Whether or not it was obtained from the synthesis. |
| formula | `ChemFormula` | Chemical composition written in a [ChemFormula](https://pypi.org/project/chemformula/) compatible format. |
| observations | `str` | General observations about the product. |

### Optional properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| expected_amount | `validators.numbers.positive_decimal` | How much of the product was nominally expected to be obtained from the synthesis. |
| expected_amount_unit | `validators.units.FOSUnit.enforce_dims(["[mass]",{"[length]":3}])` | `FOSUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) with a class method for enforcing the correct dimensionality of the unit. (In this case mass or volume) |
| obtained_amount | `validators.numbers.positive_decimal` | How much of the product was actually obtained from the synthesis. |
| obtained_amount_unit | `validators.units.FOSUnit.enforce_dims(["[mass]",{"[length]":3}])` | `FOSUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) with a class method for enforcing the correct dimensionality of the unit. (In this case mass or volume) |
| characterizations | `str` | Description of characterization methods used to determine/quantitate the product. |
| structure_comments | `str` | General description on the structure of the product. |

______________________________________________________________________

## `Quench`

**[Subclass of `AnnealSection`](#annealsection)**

### Required properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| medium | `str` | What medium the reaction vessel was quenched in (e.g., water, air). |

______________________________________________________________________

## `Ramp`

**[Subclass of `AnnealSection`](#annealsection)**

### Required properties

During construction of a `Ramp` object, it is required to have at least 2 of the following optional properties, with their respective units:

- `temp`
- `time`
- `rate`

If all three are provided, the last one found during reading will be discarded as redundant data, and the object is [dipatched](#dispatching-subclasses) to a `Ramp` subclass with a "retrieval" method for calculating the missing property (e.g., `get_temp()`, `get_time()`, or `get_rate()`) When working with `Ramp` objects in the API, it is best practice to always use the "retrieval" methods. For subclasses that *do* have the desired property, retrieval methods default to returning it directly.

### Optional properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| temp | `validators.numbers.positive_decimal` | The next temperature in the program |
| time | `validators.numbers.positive_decimal` | How long it took to get from the last temperature to the new temperature. |
| rate | `validators.numbers.any_decimal` | The sign-sensitive rate at which temperature was changed to get to the new temperature. (Increase -> positive, Decrease -> negative)|
| temp_unit | `validators.units.FOSTempUnit` | `FOSTempUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) which allows a little more coersion of temperature units. (Like recognizing `"C"` as degrees celsius as opposed to coulombs) |
| time_unit | `validators.units.FOSUnit.enforce_dims("[time]")` | `FOSUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) with a class method for enforcing the correct dimensionality of the unit. |
| rate_unit | `validators.units.temp_rate_unit` | Makes use of [`pint`'s dimensionality properties](https://pint.readthedocs.io/en/stable/) to verify that the value is a unit of temperature over time.|

______________________________________________________________________

## `Reaction`

**[Subclass of `SingleBlock`](#singleblock)**

### Required properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| nominal_formula | `ChemFormula` | Chemical composition written in a [ChemFormula](https://pypi.org/project/chemformula/) compatible format |
| nominal_amount | `validators.numbers.positive_decimal` | Total amount expected to be recovered from all participating reactants. |
| nominal_amount_unit | `validators.units.FOSUnit.enforce_dims(["[mass]",{"[length]":3}])` | `FOSUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) with a class method for enforcing the correct dimensionality of the unit. |

______________________________________________________________________

## `SingleBlock`

**Parent Block Class**

### Required properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| ext | `SubContainer` | **Not to be passed to constructor. This property is automatically created**. This attribute is used to store unexpected properties so that they don't inadvertently overwrite existing methods or attributes. |

### Optional properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| rename | `validators.rename.rename_dict` | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [API script example](../examples/API_example/index.md) for usage.|

### SingleBlock Method Subclasses

These subclasses don't currently have any additional required properties but will either be expanded in the future or have specialized methods.

- `GasFlow`: For specifying gas flow rates during an annealing treatment (to be expanded).
- `LabConditions`: For specifying laboratory conditions during the synthesis (to be expanded).
- `Equipment`: For specifying specialized laboratory equipment used in the synthesis (to be expanded).
- `FileBlock`: Subclasses of `FileBlock` are intended to be the main/top-level block of a FOS file (e.g., `Synthesis`, `TemplateSet`).

______________________________________________________________________

## `Synthesis`

**[Subclass of `FileBlock`](#singleblock)**

### Required properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| metadata | `MetaData` | [Metadata for the synthesis file](#metadata) |
| experimenters | `ExperimenterList` | A [simple list](#listblock-and-simple-lists) of [`Experimenter` objects](#experimenter) |
| reaction | `Reaction` | [General reaction information](#reaction) |
| products | `ProductList` | A [simple list](#listblock-and-simple-lists) of [`Product` objects](#product) |
| materials | `MaterialList` | A [specialized `ListBlock`](#listblock-and-simple-lists) of [`Material` objects](#material) |
| treatments | `TreatmentList` | A [simple list](#listblock-and-simple-lists) of [`Treatment` objects](#treatment) |

### Optional properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| cif | `EmbeddedCIF` | [A single embedded CIF file](#embeddedfile-method-subclasses) |
| cifs | `ListBlock.Simple(EmbeddedCIF)` | A [simple list](#listblock-and-simple-lists) of [`EmbeddedCIF` objects](#embeddedfile-method-subclasses) |
| laboratory_conditions | `LabConditions` | [General Laboratory Conditions](#singleblock-method-subclasses) |
| equipment | `EquipmentList` | A [simple list](#listblock-and-simple-lists) of [`Equipment` objects](#singleblock-method-subclasses) |

______________________________________________________________________

## `TemplateBlock`

**[Subclass of `SingleBlock`](#singleblock)**

`TemplateBlock` is used to make hybridized subclasses of other `SingleBlock` subclasses. Template subclasses override required properties of the original class with template fields that can be later filled in and passed to their validators with the `fill()` method. Refer to the [API script example](../examples/API_example/index.md) for some uses of templates.

### Required properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| template_name | `str` | An identifiable name for the template. |

______________________________________________________________________

## `TemplateMeta`

**[Subclass of `SingleBlock`](#)**

### Required properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| name | `str` | Identifiable name for the set of templates stored in a Template FOS file.|
| description | `str` | Additional information about the set of templates.|

______________________________________________________________________

## `TemplateSet`

**[Subclass of `FileBlock`](#)**

### Required properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| metadata | `TemplateMeta` | Meta information for the set of templates stored in a Template FOS file. |

### Optional properties

In contrast with a `Synthesis` file, most top-level properties for a `TemplateSet` are expected to contain [lists of templates](#templatelists) of a given type. `TemplateList.Simple()` allows entries to be incomplete and generates hybridized `TemplateBlock` subclasses for them.

Developers are currently working on ways to flexibly allow any template list in a `TemplateSet`. For now, refer to [modifying validation at runtime](#modifying-property-validation-at-runtime) or reach out to developers if current standards are limiting how you want to use templates.

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| experimenters | `TemplateList.Simple(Experimenter)` | A list of incomplete [`Experimenter` objects](#experimenter) |
| materials | `TemplateList.Simple(Material)` | A list of incomplete [`Material` objects](#material) |
| treatments | `TemplateList.Simple(Treatment)` | A list of incomplete [`Treatment` objects](#treatment) |
| annealings | `TemplateList.Simple(Annealing)` | A list of incomplete [`Annealing` objects](#annealing) |
| anneal_sections | `TemplateList.Simple(AnnealSection)` | A list of incomplete [`AnnealSection` objects](#annealsection) |
| cifs | `CifList` | A [simple list](#listblock-and-simple-lists) of [`EmbeddedCIF` objects](#embeddedfile) |

______________________________________________________________________

## `Treatment`

**[Subclass of `SingleBlock`](#singleblock)**

When applicable, treatments are dispatched to subclasses based on the type value. Specialized subclasses for treatments are added by developers on an as-needed basis for specialized methods, or requiring additional properties for some types. Unrecognized types are still allowed but aren't given any additional properties or methods. The current dispatch list is below:

| type | Subclass |
| --- | --- |
| anneal | `Annealing` [(link)](#annealing) |

### Required properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| type | `str` (dispatched) | What type of treatment was performed |
| repeats | `int` | How many times it was performed in succession (if interrupted by other treatments, add a different treatment block after the interrupting treatments) |
| observations | `str` | General observations |

### Optional properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| recovered_amount | `validators.numbers.positive_decimal` | How much material was recovered after treatment |
| recovered_amount_unit | `validators.units.FOSUnit.enforce_dims(["[mass]",{"[length]":3}])` | `FOSUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) with a class method for enforcing the correct dimensionality of the unit. |
| start_time | `str` | What time the treatment was started |
| end_time | `str` | What time the treatment was finished |
