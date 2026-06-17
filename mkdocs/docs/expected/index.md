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

`TemplateList` is a unique subclass of `ListBlock` used for storing [`TemplateBlock` subclass objects](#templateblock). `TemplateList` has a class method `Simple()` similar to `ListBlock`'s method, but instead of full objects (e.g. `Material`), it generates hybridized templates with fields for any field-marked or missing properties. Some syntax for `TemplateList` entries can be found in the [code example walkthrough](../examples/templates/index.md).

## Modifying Property Validation at Runtime

The intent of the FOS is to be as flexible as possible while still enforcing standards for fully capturing a synthetic method. However, it may be necessary for private or niche applications to modify standards to match your own synthesis. This can be done by mutating the dictionaries in `FoSpy.parsing.validation` at the start of your script. The example below creates a new block type with its own expected properties, and then adds it as an optional top-level block for a synthesis file.

These modifications should be reserved for very unique and isolated cases. If you are modifying standards in a significant way, or such that may be applicable for other researchers, consider reaching out to `FoSpy` developers or creating a fork of the [GitHub](https://github.com/errthumt/FoSpy).

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

## Expected Property Tables

### `AnnealSection`

[Class Documentation][blockdocs-AnnealSection]

**[Subclass of `SingleBlock`](#singleblock)**

#### Required properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| type | `str` (dispatched) | Examples: `"dwell", "ramp", "quench"` |

---

### `Annealing`

[Class Documentation][blockdocs-Annealing]

**[Subclass of `Treatment`](#treatment)**

#### Required properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| program | [Block: `AnnealProgram`][blockdocs-AnnealProgram] | A [specialized `ListBlock`](#listblock-and-simple-lists) of [`AnnealSection` objects](#annealsection) |
| start_temp | [Numbers validator: `positive_decimal`][FoSpy.parsing.validators.numbers.positive_decimal] | The initial temperature of the annealing profile.<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). |
| start_temp_unit | [Units validator: `FOSTempUnit`][FoSpy.parsing.validators.units.FOSTempUnit] | `FOSTempUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) which allows a little more coersion of temperature units. (Like recognizing `"C"` as degrees celsius as opposed to coulombs)|

#### Optional properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| gas_flow | [Block: `FlowList`][blockdocs-FlowList] | A [simple list](#listblock-and-simple-lists) of [`GasFlow` objects](#singleblock-method-subclasses) |

---

### `Attachment`

[Class Documentation][blockdocs-Attachment]

**[Subclass of `SingleBlock`](#singleblock)**

#### Required properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| file_name | [Filenames validator: `file_name`][FoSpy.parsing.validators.filenames.file_name] (dispatched) | A name for the file that does not contain any incompatible characters ( `\ / : * ? " < > \|`). Must include a valid extension. Some subclasses (like `CIFFile`) are dispatched based on detected file extension. |

##### Additional Requirements

In addition to the required properties above, all `Attachment` objects must be constructed with one of the following optional properties:

- `embedded`
- `path`

The first matching property found will be used and the remainder will be discarded. The presence of one of these properties is used to identify what form of file attachment it is. Refer to the [attachments guide](../guides/attachments.md) for more information

#### Optional properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| embedded | `list` | A list of raw utf-8 line strings copied from the embedded file. See [attachments guide](../guides/attachments.md) for syntax. |
| path | [Filenames validator: `PathPosix`][FoSpy.parsing.validators.filenames.PathPosix] | Instead of directly embedding contents, refers to a relative path from the folder containing the parent `FileBlock`. Can use relative characters like "`.`" and "`..`". See [attachments guide](../guides/attachments.md) for more information.<br> `PathPosix` validator is a subclass of `pathlib.Path` which always uses back slashes (`/`) instead of forward slashes (`\`) when serialized, regardless of OS |

#### Attachment Method Subclasses

Attachment Subclasses are hybridized between an **attachment type** and a **file type**. Attachment types share most method names to be called by *file type* methods, but method source code differs on the basis of how the file was attached. For example, `_get_filepath()` for [`PathFile`](../blocks/attachments.md#FoSpy.blocks.attachments.PathFile._get_filepath) simply returns an absolute filepath resolved from the value in its `path` attribute, whereas [`EmbeddedFile`](../blocks/attachments.md#FoSpy.blocks.attachments.EmbeddedFile._get_filepath) objects create a temporary file to print their embedded lines to before returning its filepath.

Attachment types are dispatched based on which optional properties they have. File types are dispatched based on extension. Unrecognized extensions simply don't add any special file type methods.

##### Attachment Types

- `EmbeddedFile`
- `PathFile`

##### File Types

- `CIFFile`

### `Dwell`

[Class Documentation][blockdocs-Dwell]

**[Subclass of `AnnealSection`](#annealsection)**

#### Required properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| time | [Numbers validator: `positive_decimal`][FoSpy.parsing.validators.numbers.positive_decimal] | How long the temperature was kept constant in this section.<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). |
| time_unit | [Units validator: `FOSUnit.enforce_dims('[time]')`][FoSpy.parsing.validators.units.FOSUnit.enforce_dims] | `FOSUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) with a class method for enforcing the correct dimensionality of the unit. |

---

### `Experimenter`

[Class Documentation][blockdocs-Experimenter]

**[Subclass of `SingleBlock`](#singleblock)**

#### Required properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| name | `str` | Name of the experimenter |
| affiliation | `str` | Lab/University/Research Group/etc. |

#### Optional properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| orcid | `str` | The experimenter's [ORCID](https://orcid.org/)|

---

### `FileBlock`

[Class Documentation][blockdocs-FileBlock]

**[Subclass of `SingleBlock`](#singleblock)**

#### Required properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| metadata | [Block: `MetaData`](#metadata) | General information about the file. Lines at the beginning of a FOS-formatted file without a header will automatically be interpreted as a `MetaData` dictionary |

---

### `Material`

[Class Documentation][blockdocs-Material]

**[Subclass of `SingleBlock`](#singleblock)**

#### Required properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| name | `str` | Identifiable name for the material |
| type | `str` | How it was used in the synthesis (e.g., reagent, flux, solvent) |
| formula | `ChemFormula` | Chemical composition written in a [ChemFormula](https://pypi.org/project/chemformula/) compatible format |
| supplier | `str` | Source of purchase/synthesis (may be internal) |
| cas | `str` | CAS ID. May be "unknown"| 
| form | `str` | Physical shape or state of the material **at time of acquisition** (e.g., powder, shot, wire, lump). If the material was modified after aquiring but before use in the synthesis (like grinding into powder, drying, etc.), these actions should be specified in the *material's* treatments property (not the synthesis treatments).|
| env | `str` | What environment the material is stored in. (e.g., ambient, Ar(g))|
| amount | [Numbers validator: `positive_decimal`][FoSpy.parsing.validators.numbers.positive_decimal] | Amount that was used.<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). |
| amount_unit | `str` | Descriptive unit for amount. Dimensionality may be enforced in the future once more input is gained from experimenters.|

#### Optional properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| purity | [Numbers validator: `decimal_range`][FoSpy.parsing.validators.numbers.decimal_range] | 0 < purity ≤ 1 |
| treatments | [Block: `TreatmentList`][blockdocs-TreatmentList] | A [simple list](#listblock-and-simple-lists) of [`Treatment` objects](#treatment)<br>Any modifications to the material between acquisition and use in the synthesis. |

---

### `MetaData`

[Class Documentation][blockdocs-MetaData]

**[Subclass of `SingleBlock`](#singleblock)**

#### Required properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| fos_id | `str` | Identifiable ID for the synthesis or sample.<br><br>**For [`Synthesis`](#synthesismeta) files:** this should be kept informative and unique within the scope of the project_id, as it may be used as identification for future database storage.<br>**For [`TemplateSet`](#templateset) files:** it is for convenience. |
| fos_type | `str` | What type of `FileBlock` subclass the file should be interpreted as. Expected values are:<br>`synthesis`<br>`templates` |
| description | `str` | A brief description of the intent for the file (characteristic methods, target products, template category, etc.). |

---

### `Product`

[Class Documentation][blockdocs-Product]

**[Subclass of `SingleBlock`](#singleblock)**

#### Required properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| name | `str` | Identifiable name for the product. |
| expected | `bool` | Whether or not it was expected from the synthesis. |
| obtained | `bool` | Whether or not it was obtained from the synthesis. |
| formula | `ChemFormula` | Chemical composition written in a [ChemFormula](https://pypi.org/project/chemformula/) compatible format. |
| observations | `str` | General observations about the product. |

#### Optional properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| expected_amount | [Numbers validator: `positive_decimal`][FoSpy.parsing.validators.numbers.positive_decimal] | How much of the product was nominally expected to be obtained from the synthesis.<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). |
| expected_amount_unit | [Units validator: `FOSUnit.enforce_dims(["[mass]",{"[length]":3}])`][FoSpy.parsing.validators.units.FOSUnit.enforce_dims] | `FOSUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) with a class method for enforcing the correct dimensionality of the unit. (In this case mass or volume) |
| obtained_amount | [Numbers validator: `positive_decimal`][FoSpy.parsing.validators.numbers.positive_decimal] | How much of the product was actually obtained from the synthesis.<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). |
| obtained_amount_unit | [Units validator: `FOSUnit.enforce_dims(["[mass]",{"[length]":3}])`][FoSpy.parsing.validators.units.FOSUnit.enforce_dims] | `FOSUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) with a class method for enforcing the correct dimensionality of the unit. (In this case mass or volume) |
| characterizations | `str` | Description of characterization methods used to determine/quantitate the product. |
| structure_comments | `str` | General description on the structure of the product. |

---

### `Quench`

[Class Documentation][blockdocs-Quench]

**[Subclass of `AnnealSection`](#annealsection)**

#### Required properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| medium | `str` | What medium the reaction vessel was quenched in (e.g., water, air). |

---

### `Ramp`

[Class Documentation][blockdocs-Ramp]

**[Subclass of `AnnealSection`](#annealsection)**

#### Required properties

During construction of a `Ramp` object, it is required to have at least 2 of the following optional properties, with their respective units:

- `temp`
- `time`
- `rate`

If all three are provided, the last one found during reading will be discarded as redundant data, and the object is [dipatched](#dispatching-subclasses) to a `Ramp` subclass with a "retrieval" method for calculating the missing property (e.g., `get_temp()`, `get_time()`, or `get_rate()`) When working with `Ramp` objects in the FoSpy framework, it is best practice to always use the "retrieval" methods. For subclasses that *do* have the desired property, retrieval methods default to returning it directly.

#### Optional properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| temp | [Numbers validator: `positive_decimal`][FoSpy.parsing.validators.numbers.positive_decimal] | The next temperature in the program.<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). |
| time | [Numbers validator: `positive_decimal`][FoSpy.parsing.validators.numbers.positive_decimal] | How long it took to get from the last temperature to the new temperature.<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). |
| rate | [Numbers validator: `any_decimal`][FoSpy.parsing.validators.numbers.any_decimal] | The sign-sensitive rate at which temperature was changed to get to the new temperature. (Increase -> positive, Decrease -> negative).<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). |
| temp_unit | [Units validator: `FOSTempUnit`][FoSpy.parsing.validators.units.FOSTempUnit] | `FOSTempUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) which allows a little more coersion of temperature units. (Like recognizing `"C"` as degrees celsius as opposed to coulombs) |
| time_unit | [Units validator: `FOSUnit.enforce_dims("[time]")`][FoSpy.parsing.validators.units.FOSUnit.enforce_dims] | `FOSUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) with a class method for enforcing the correct dimensionality of the unit. |
| rate_unit | [Units validator: `temp_rate_unit`][FoSpy.parsing.validators.units.temp_rate_unit] | Makes use of [`pint`'s dimensionality properties](https://pint.readthedocs.io/en/stable/) to verify that the value is a unit of temperature over time.|

#### Ramp Method Subclasses

The following subclasses are dispatched based on the redundant parameter (see [Required Properties](#ramp) above) and override the retrieval method to calculate the missing parameter instead of getting it from attributes:

- `RampNoRate`: overrides [`get_rate()`](../blocks/treatments.md#FoSpy.blocks.treatments.RampNoRate.get_rate)
- `RampNoTemp`: overrides [`get_temp()`](../blocks/treatments.md#FoSpy.blocks.treatments.RampNoRate.get_temp)
- `RampNoTime`: overrides [`get_time()`](../blocks/treatments.md#FoSpy.blocks.treatments.RampNoRate.get_time)

______________________________________________________________________

### `Reaction`

[Class Documentation][blockdocs-Reaction]

**[Subclass of `SingleBlock`](#singleblock)**

#### Required properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| nominal_formula | `ChemFormula` | Chemical composition written in a [ChemFormula](https://pypi.org/project/chemformula/) compatible format |
| nominal_amount | [Numbers validator: `positive_decimal`][FoSpy.parsing.validators.numbers.positive_decimal] | Total amount expected to be recovered from all participating reactants.<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). |
| nominal_amount_unit | [Units validator: `FOSUnit.enforce_dims(["[mass]",{"[length]":3}])`][FoSpy.parsing.validators.units.FOSUnit.enforce_dims] | `FOSUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) with a class method for enforcing the correct dimensionality of the unit. |

---

### `SingleBlock`

[Class Documentation][blockdocs-SingleBlock]

**Parent Block Class**

#### Required properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| ext | [Special: `SubContainer`][FoSpy.blocks._containers.SubContainer] | **Do not include in FOS files. This property is automatically created**. This attribute is used to store unexpected properties so that they don't inadvertently overwrite existing methods or attributes. |

#### Optional properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| rename | [Rename validator: `rename_dict`][FoSpy.parsing.validators.rename.rename_dict] | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage.|

#### SingleBlock Method Subclasses

These subclasses don't currently have any additional required properties but will either be expanded in the future or have specialized methods.

- `GasFlow`: For specifying gas flow rates during an annealing treatment (to be expanded).
- `LabConditions`: For specifying laboratory conditions during the synthesis (to be expanded).
- `Equipment`: For specifying specialized laboratory equipment used in the synthesis (to be expanded).
- `CSVdata`: Placeholder for planned features with CSV data inserted as dataframes
- `TraceData`: Placeholder for planned features with plottable 2D dataframes

______________________________________________________________________

### `Synthesis`

[Class Documentation][blockdocs-Synthesis]

**[Subclass of `FileBlock`](#fileblock)**

#### Required properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| metadata | [Block: `SynthesisMeta`](#synthesismeta) | General information about the file. Additional requirements from basic [file metadata](#metadata). Lines at the beginning of a FOS-formatted file without a header will automatically be interpreted as a `MetaData` dictionary |
| experimenters | [Block: `ExperimenterList`][blockdocs-ExperimenterList] | A [simple list](#listblock-and-simple-lists) of [`Experimenter` objects](#experimenter) |
| reaction | [Block: `Reaction`](#reaction) | [General reaction information](#reaction) |
| products | [Block: `ProductList`][blockdocs-ProductList] | A [simple list](#listblock-and-simple-lists) of [`Product` objects](#product) |
| materials | [Block: `MaterialList`][blockdocs-MaterialList] | A [specialized `ListBlock`](#listblock-and-simple-lists) of [`Material` objects](#material) |
| treatments | [Block: `TreatmentList`][blockdocs-TreatmentList] | A [simple list](#listblock-and-simple-lists) of [`Treatment` objects](#treatment) |

#### Optional properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| cif | `Attachment.enforce_subtype(CIFFile)` ([see class method](../blocks/attachments.md#FoSpy.blocks.attachments.Attachment.enforce_subtype)) | [A single attached CIF file](#attachment) |
| cifs | [Block: `CifList`][blockdocs-CifList] | A [simple list](#listblock-and-simple-lists) of [attached CIF files](#attachment) |
| laboratory_conditions | [Block: `LabConditions`](#singleblock-method-subclasses) | [General Laboratory Conditions](#singleblock-method-subclasses) |
| equipment | [Block: `EquipmentList`][blockdocs-EquipmentList] | A [simple list](#listblock-and-simple-lists) of [`Equipment` objects](#singleblock-method-subclasses) |

---

### `SynthesisMeta`

[Class Documentation][blockdocs-SynthesisMeta]

**[Subclass of `MetaData`](#metadata)**

#### Required properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| group_id | `str` | A unique identifier for the research group or organization.<br><br>**In the future:** unique group_id values should be standardized and/or issued by a central party to ensure that all future database uploads have a unique index location.<br>**For now:** group_id values can be verified unique by ending with the primary investigator's ORCID (example: kovnir-0000-0003-1152-1912). After standardization, tools will be developed to convert group_id values for entire group repositories. |
| project_id| `str` | An identifier that only needs to be unique within the scope of the group_id. This can be more flexible to the needs of the group, but good practice is to keep synthesis files in a folder structure that matches project_id values. A large experimental group, for example, might categorize syntheses by experimenter then project, or vice versa for intra-collaboration. To avoid future conflicts, name-based categories should be given unique suffixes, like university ID/username or the last 4 digits of the ORCID. Some examples:<br> `travis5672/clathrates`, `travis(errthumt)/pnictides`, `thermoelectrics/travis5672/Ba2-TM5-Pn6`<br><br>***Future Tools** will expect project_ids to reflect folder structure using "`/`" or "`\`" delimiters.* |

### `TemplateBlock`

[Class Documentation][blockdocs-TemplateBlock]

**[Subclass of `SingleBlock`](#singleblock)**

`TemplateBlock` is used to make hybridized subclasses of other `SingleBlock` subclasses. Template subclasses override required properties of the original class with template fields that can be later filled in and passed to their validators with the `fill()` method. Refer to the [code example walkthrough](../examples/code_example/index.md) for some uses of templates.

#### Required properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| template_name | `str` | An identifiable name for the template. |

#### TemplateBlock Method Subclasses

These subclasses don't currently have any additional required properties but will either be expanded in the future or have specialized methods.

- `FlexTemplate`: Same functionality as `TemplateBlock`, but automatically interprets missing input as template fields rather than having preset expectations for which fields are unfilled. Used for [`reflex()`](../blocks/blocks.md#FoSpy.blocks.blocks.SingleBlock.reflex) method and [`TemplateList`](../blocks/template.md#FoSpy.blocks.template.TemplateList) construction.

______________________________________________________________________

### `TemplateSet`

[Class Documentation][blockdocs-TemplateSet]

**[Subclass of `FileBlock`](#fileblock)**

#### Optional properties

In contrast with a `Synthesis` file, most top-level properties for a `TemplateSet` are expected to contain [lists of templates](#templatelists) of a given type. `TemplateList.Simple()` allows entries to be incomplete and generates hybridized `TemplateBlock` subclasses for them.

Developers are currently working on ways to flexibly allow any template list in a `TemplateSet`. For now, refer to [modifying validation at runtime](#modifying-property-validation-at-runtime) or reach out to developers if current standards are limiting how you want to use templates.

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| experimenters | `TemplateList.Simple(Experimenter)` | A list of incomplete [`Experimenter` objects](#experimenter) |
| materials | `TemplateList.Simple(Material)` | A list of incomplete [`Material` objects](#material) |
| treatments | `TemplateList.Simple(Treatment)` | A list of incomplete [`Treatment` objects](#treatment) |
| annealings | `TemplateList.Simple(Annealing)` | A list of incomplete [`Annealing` objects](#annealing) |
| anneal_sections | `TemplateList.Simple(AnnealSection)` | A list of incomplete [`AnnealSection` objects](#annealsection) |
| cifs | [Block: `CifList`][blockdocs-CifList] | A [simple list](#listblock-and-simple-lists) of [attached CIF files](#attachment) |

______________________________________________________________________

### `Treatment`

[Class Documentation][blockdocs-Treatment]

**[Subclass of `SingleBlock`](#singleblock)**

When applicable, treatments are dispatched to subclasses based on the type value. Specialized subclasses for treatments are added by developers on an as-needed basis for specialized methods, or requiring additional properties for some types. Unrecognized types are still allowed but aren't given any additional properties or methods. The current dispatch list is below:

| type | Subclass |
| --- | --- |
| anneal | [Block: `Annealing`](#annealing) |

#### Required properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| type | `str` (dispatched) | What type of treatment was performed |
| repeats | `int` | How many times it was performed in succession (if interrupted by other treatments, add a different treatment block after the interrupting treatments) |
| observations | `str` | General observations |

#### Optional properties

| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| recovered_amount | `validators.numbers.positive_decimal` | How much material was recovered after treatment. <br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). |
| recovered_amount_unit | `validators.units.FOSUnit.enforce_dims(["[mass]",{"[length]":3}])` | `FOSUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) with a class method for enforcing the correct dimensionality of the unit. |
| start_time | `str` | What time the treatment was started |
| end_time | `str` | What time the treatment was finished |
