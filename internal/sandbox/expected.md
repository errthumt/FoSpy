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

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| type | Examples: `"dwell", "ramp", "quench"` | No Rules Found |

#### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | No Rules Found |

---

### `Annealing`

[Class Documentation][blockdocs-Annealing]

**[Subclass of `Treatment`](#treatment)**

#### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| type | What type of treatment was performed | No Rules Found |
| repeats | How many times it was performed in succession (if interrupted by other treatments, add a different treatment block after the interrupting treatments) | No Rules Found |
| observations | General observations | No Rules Found |
| program | A [specialized `ListBlock`](#listblock-and-simple-lists) of [`AnnealSection` objects](#annealsection) | No Rules Found |
| start_temp | The initial temperature of the annealing profile.<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). | No Rules Found |
| start_temp_unit | `FOSTempUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) which allows a little more coersion of temperature units. (Like recognizing `"C"` as degrees celsius as opposed to coulombs) | No Rules Found |

#### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | No Rules Found |
| recovered_amount | How much material was recovered after treatment. <br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). | No Rules Found |
| recovered_amount_unit | `FOSUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) with a class method for enforcing the correct dimensionality of the unit. | No Rules Found |
| start_time | What time the treatment was started | No Rules Found |
| end_time | What time the treatment was finished | No Rules Found |
| gas_flow | A [simple list](#listblock-and-simple-lists) of [`GasFlow` objects](#singleblock-method-subclasses) | No Rules Found |

---

### `Attachment`

[Class Documentation][blockdocs-Attachment]

**[Subclass of `SingleBlock`](#singleblock)**

#### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| file_name | A name for the file that does not contain any incompatible characters ( `\ / : * ? " < > \|`). Must include a valid extension. Some subclasses (like `CIFFile`) are dispatched based on detected file extension. | No Rules Found |

#### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | No Rules Found |
| embedded | A list of raw utf-8 line strings copied from the embedded file. See [attachments guide](../guides/attachments.md) for syntax. | No Rules Found |
| path | Instead of directly embedding contents, refers to a relative path from the folder containing the parent `FileBlock`. Can use relative characters like "." and "..". See [attachments guide](../guides/attachments.md) for more information.<br> `PathPosix` validator is a subclass of `pathlib.Path` which always uses back slashes (`/`) instead of forward slashes (`\`) when serialized, regardless of OS | <ul><li>A valid relative filepath.</li><li>Paths to nonexistent files will be validated, but may raise errors when the parent `FileBlock` attempts to track the file.</li></ul> |

#### Additional Requirements

In addition to the required properties above, all `Attachment` objects must be constructed with one of the following optional properties:

- `embedded`
- `path`

The first matching property found will be used and the remainder will be discarded. The presence of one of these properties is used to identify what form of file attachment it is. Refer to the [attachments guide](../guides/attachments.md) for more information

#### Attachment Method Subclasses

Attachment Subclasses are hybridized between an **attachment type** and a **file type**. Attachment types share most method names to be called by *file type* methods, but method source code differs on the basis of how the file was attached. For example, `_get_filepath()` for [`PathFile`](../blocks/attachments.md#FoSpy.blocks.attachments.PathFile._get_filepath) simply returns an absolute filepath resolved from the value in its `path` attribute, whereas [`EmbeddedFile`](../blocks/attachments.md#FoSpy.blocks.attachments.EmbeddedFile._get_filepath) objects create a temporary file to print their embedded lines to before returning its filepath.

Attachment types are dispatched based on which optional properties they have. File types are dispatched based on extension. Unrecognized extensions simply don't add any special file type methods.

##### Attachment Types

- `EmbeddedFile`
- `PathFile`

##### File Types

- `CIFFile`---

### `CIFFile`

[Class Documentation][blockdocs-CIFFile]

**[Subclass of `Attachment`](#attachment)**

#### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| file_name | A name for the file that does not contain any incompatible characters ( `\ / : * ? " < > \|`). Must include a valid extension. Some subclasses (like `CIFFile`) are dispatched based on detected file extension. | No Rules Found |

#### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | No Rules Found |
| embedded | A list of raw utf-8 line strings copied from the embedded file. See [attachments guide](../guides/attachments.md) for syntax. | No Rules Found |
| path | Instead of directly embedding contents, refers to a relative path from the folder containing the parent `FileBlock`. Can use relative characters like "." and "..". See [attachments guide](../guides/attachments.md) for more information.<br> `PathPosix` validator is a subclass of `pathlib.Path` which always uses back slashes (`/`) instead of forward slashes (`\`) when serialized, regardless of OS | <ul><li>A valid relative filepath.</li><li>Paths to nonexistent files will be validated, but may raise errors when the parent `FileBlock` attempts to track the file.</li></ul> |

---

### `CSVdata`

[Class Documentation][blockdocs-CSVdata]

**[Subclass of `SingleBlock`](#singleblock)**

#### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |

#### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | No Rules Found |

---

### `Dwell`

[Class Documentation][blockdocs-Dwell]

**[Subclass of `AnnealSection`](#annealsection)**

#### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| type | Examples: `"dwell", "ramp", "quench"` | No Rules Found |
| time | How long the temperature was kept constant in this section.<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). | No Rules Found |
| time_unit | `FOSUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) with a class method for enforcing the correct dimensionality of the unit. | No Rules Found |

#### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | No Rules Found |

---

### `EmbeddedFile`

[Class Documentation][blockdocs-EmbeddedFile]

**[Subclass of `Attachment`](#attachment)**

#### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| file_name | A name for the file that does not contain any incompatible characters ( `\ / : * ? " < > \|`). Must include a valid extension. Some subclasses (like `CIFFile`) are dispatched based on detected file extension. | No Rules Found |

#### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | No Rules Found |
| embedded | A list of raw utf-8 line strings copied from the embedded file. See [attachments guide](../guides/attachments.md) for syntax. | No Rules Found |
| path | Instead of directly embedding contents, refers to a relative path from the folder containing the parent `FileBlock`. Can use relative characters like "." and "..". See [attachments guide](../guides/attachments.md) for more information.<br> `PathPosix` validator is a subclass of `pathlib.Path` which always uses back slashes (`/`) instead of forward slashes (`\`) when serialized, regardless of OS | <ul><li>A valid relative filepath.</li><li>Paths to nonexistent files will be validated, but may raise errors when the parent `FileBlock` attempts to track the file.</li></ul> |

---

### `Equipment`

[Class Documentation][blockdocs-Equipment]

**[Subclass of `SingleBlock`](#singleblock)**

#### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |

#### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | No Rules Found |

---

### `Experimenter`

[Class Documentation][blockdocs-Experimenter]

**[Subclass of `SingleBlock`](#singleblock)**

#### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| name | Name of the experimenter | No Rules Found |
| affiliation | Lab/University/Research Group/etc. | No Rules Found |

#### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | No Rules Found |
| orcid | The experimenter's [ORCID](https://orcid.org/) | No Rules Found |

---

### `FileBlock`

[Class Documentation][blockdocs-FileBlock]

**[Subclass of `SingleBlock`](#singleblock)**

#### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| metadata | General information about the file. Lines at the beginning of a FOS-formatted file without a header will automatically be interpreted as a `MetaData` dictionary | No Rules Found |

#### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | No Rules Found |

---

### `FlexTemplate`

[Class Documentation][blockdocs-FlexTemplate]

**[Subclass of `TemplateBlock`](#templateblock)**

#### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| template_name | An identifiable name for the template. | No Rules Found |

#### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | No Rules Found |

---

### `GasFlow`

[Class Documentation][blockdocs-GasFlow]

**[Subclass of `SingleBlock`](#singleblock)**

#### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |

#### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | No Rules Found |

---

### `LabConditions`

[Class Documentation][blockdocs-LabConditions]

**[Subclass of `SingleBlock`](#singleblock)**

#### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |

#### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | No Rules Found |

---

### `Material`

[Class Documentation][blockdocs-Material]

**[Subclass of `SingleBlock`](#singleblock)**

#### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| name | Identifiable name for the material | No Rules Found |
| type | How it was used in the synthesis (e.g., reagent, flux, solvent) | No Rules Found |
| formula | Chemical composition written in a [ChemFormula](https://pypi.org/project/chemformula/) compatible format | No Rules Found |
| supplier | Source of purchase/synthesis (may be internal) | No Rules Found |
| cas | CAS ID. May be "unknown" | No Rules Found |
| form | Physical shape or state of the material **at time of acquisition** (e.g., powder, shot, wire, lump). If the material was modified after aquiring but before use in the synthesis (like grinding into powder, drying, etc.), these actions should be specified in the *material's* treatments property (not the synthesis treatments). | No Rules Found |
| env | What environment the material is stored in. (e.g., ambient, Ar(g)) | No Rules Found |
| amount | Amount that was used.<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). | No Rules Found |
| amount_unit | Descriptive unit for amount. Dimensionality may be enforced in the future once more input is gained from experimenters. | No Rules Found |

#### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | No Rules Found |
| purity | 0 < purity ≤ 1 | No Rules Found |
| treatments | A [simple list](#listblock-and-simple-lists) of [`Treatment` objects](#treatment)<br>Any modifications to the material between acquisition and use in the synthesis. | No Rules Found |

---

### `MetaData`

[Class Documentation][blockdocs-MetaData]

**[Subclass of `SingleBlock`](#singleblock)**

#### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| fos_id | Identifiable ID for the synthesis or sample.<br><br>**For [`Synthesis`](#synthesismeta) files:** this should be kept informative and unique within the scope of the project_id, as it may be used as identification for future database storage.<br>**For [`TemplateSet`](#templateset) files:** it is for convenience. | No Rules Found |
| fos_type | What type of `FileBlock` subclass the file should be interpreted as. Expected values are:<br>`synthesis`<br>`templates` | No Rules Found |
| description | A brief description of the intent for the file (characteristic methods, target products, template category, etc.). | No Rules Found |

#### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | No Rules Found |

---

### `PathFile`

[Class Documentation][blockdocs-PathFile]

**[Subclass of `Attachment`](#attachment)**

#### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| file_name | A name for the file that does not contain any incompatible characters ( `\ / : * ? " < > \|`). Must include a valid extension. Some subclasses (like `CIFFile`) are dispatched based on detected file extension. | No Rules Found |

#### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | No Rules Found |
| embedded | A list of raw utf-8 line strings copied from the embedded file. See [attachments guide](../guides/attachments.md) for syntax. | No Rules Found |
| path | Instead of directly embedding contents, refers to a relative path from the folder containing the parent `FileBlock`. Can use relative characters like "." and "..". See [attachments guide](../guides/attachments.md) for more information.<br> `PathPosix` validator is a subclass of `pathlib.Path` which always uses back slashes (`/`) instead of forward slashes (`\`) when serialized, regardless of OS | <ul><li>A valid relative filepath.</li><li>Paths to nonexistent files will be validated, but may raise errors when the parent `FileBlock` attempts to track the file.</li></ul> |

---

### `Product`

[Class Documentation][blockdocs-Product]

**[Subclass of `SingleBlock`](#singleblock)**

#### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| name | Identifiable name for the product. | No Rules Found |
| expected | Whether or not it was expected from the synthesis. | No Rules Found |
| obtained | Whether or not it was obtained from the synthesis. | No Rules Found |
| formula | Chemical composition written in a [ChemFormula](https://pypi.org/project/chemformula/) compatible format. | No Rules Found |
| observations | General observations about the product. | No Rules Found |

#### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | No Rules Found |
| expected_amount | How much of the product was nominally expected to be obtained from the synthesis.<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). | No Rules Found |
| expected_amount_unit | `FOSUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) with a class method for enforcing the correct dimensionality of the unit. (In this case mass or volume) | No Rules Found |
| obtained_amount | How much of the product was actually obtained from the synthesis.<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). | No Rules Found |
| obtained_amount_unit | `FOSUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) with a class method for enforcing the correct dimensionality of the unit. (In this case mass or volume) | No Rules Found |
| characterizations | Description of characterization methods used to determine/quantitate the product. | No Rules Found |
| structure_comments | General description on the structure of the product. | No Rules Found |

---

### `Quench`

[Class Documentation][blockdocs-Quench]

**[Subclass of `AnnealSection`](#annealsection)**

#### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| type | Examples: `"dwell", "ramp", "quench"` | No Rules Found |
| medium | What medium the reaction vessel was quenched in (e.g., water, air). | No Rules Found |

#### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | No Rules Found |

---

### `Ramp`

[Class Documentation][blockdocs-Ramp]

**[Subclass of `AnnealSection`](#annealsection)**

#### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| type | Examples: `"dwell", "ramp", "quench"` | No Rules Found |

#### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | No Rules Found |
| temp | The next temperature in the program.<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). | No Rules Found |
| time | How long it took to get from the last temperature to the new temperature.<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). | No Rules Found |
| rate | The sign-sensitive rate at which temperature was changed to get to the new temperature. (Increase -> positive, Decrease -> negative).<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). | No Rules Found |
| temp_unit | `FOSTempUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) which allows a little more coersion of temperature units. (Like recognizing `"C"` as degrees celsius as opposed to coulombs) | No Rules Found |
| time_unit | `FOSUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) with a class method for enforcing the correct dimensionality of the unit. | No Rules Found |
| rate_unit | Makes use of [`pint`'s dimensionality properties](https://pint.readthedocs.io/en/stable/) to verify that the value is a unit of temperature over time. | No Rules Found |

#### Required properties

During construction of a `Ramp` object, it is required to have at least 2 of the following optional properties, with their respective units:

- `temp`
- `time`
- `rate`

If all three are provided, the last one found during reading will be discarded as redundant data, and the object is [dispatched](#dispatching-subclasses) to a `Ramp` subclass with a "retrieval" method for calculating the missing property (e.g., `get_temp()`, `get_time()`, or `get_rate()`) When working with `Ramp` objects in the FoSpy framework, it is best practice to always use the "retrieval" methods. For subclasses that *do* have the desired property, retrieval methods default to returning it directly.


| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | No Rules Found |
| temp | The next temperature in the program.<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). | No Rules Found |
| time | How long it took to get from the last temperature to the new temperature.<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). | No Rules Found |
| rate | The sign-sensitive rate at which temperature was changed to get to the new temperature. (Increase -> positive, Decrease -> negative).<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). | No Rules Found |
| temp_unit | `FOSTempUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) which allows a little more coersion of temperature units. (Like recognizing `"C"` as degrees celsius as opposed to coulombs) | No Rules Found |
| time_unit | `FOSUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) with a class method for enforcing the correct dimensionality of the unit. | No Rules Found |
| rate_unit | Makes use of [`pint`'s dimensionality properties](https://pint.readthedocs.io/en/stable/) to verify that the value is a unit of temperature over time. | No Rules Found |


#### Ramp Method Subclasses

The following subclasses are dispatched based on the redundant parameter (see [Required Properties](#ramp) above) and override the retrieval method to calculate the missing parameter instead of getting it from attributes:

- `RampNoRate`: overrides [`get_rate()`](../blocks/treatments.md#FoSpy.blocks.treatments.RampNoRate.get_rate)
- `RampNoTemp`: overrides [`get_temp()`](../blocks/treatments.md#FoSpy.blocks.treatments.RampNoRate.get_temp)
- `RampNoTime`: overrides [`get_time()`](../blocks/treatments.md#FoSpy.blocks.treatments.RampNoRate.get_time)
---

### `RampNoRate`

[Class Documentation][blockdocs-RampNoRate]

**[Subclass of `Ramp`](#ramp)**

#### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| type | Examples: `"dwell", "ramp", "quench"` | No Rules Found |

#### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | No Rules Found |
| temp | The next temperature in the program.<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). | No Rules Found |
| time | How long it took to get from the last temperature to the new temperature.<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). | No Rules Found |
| rate | The sign-sensitive rate at which temperature was changed to get to the new temperature. (Increase -> positive, Decrease -> negative).<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). | No Rules Found |
| temp_unit | `FOSTempUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) which allows a little more coersion of temperature units. (Like recognizing `"C"` as degrees celsius as opposed to coulombs) | No Rules Found |
| time_unit | `FOSUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) with a class method for enforcing the correct dimensionality of the unit. | No Rules Found |
| rate_unit | Makes use of [`pint`'s dimensionality properties](https://pint.readthedocs.io/en/stable/) to verify that the value is a unit of temperature over time. | No Rules Found |

---

### `RampNoTemp`

[Class Documentation][blockdocs-RampNoTemp]

**[Subclass of `Ramp`](#ramp)**

#### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| type | Examples: `"dwell", "ramp", "quench"` | No Rules Found |

#### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | No Rules Found |
| temp | The next temperature in the program.<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). | No Rules Found |
| time | How long it took to get from the last temperature to the new temperature.<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). | No Rules Found |
| rate | The sign-sensitive rate at which temperature was changed to get to the new temperature. (Increase -> positive, Decrease -> negative).<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). | No Rules Found |
| temp_unit | `FOSTempUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) which allows a little more coersion of temperature units. (Like recognizing `"C"` as degrees celsius as opposed to coulombs) | No Rules Found |
| time_unit | `FOSUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) with a class method for enforcing the correct dimensionality of the unit. | No Rules Found |
| rate_unit | Makes use of [`pint`'s dimensionality properties](https://pint.readthedocs.io/en/stable/) to verify that the value is a unit of temperature over time. | No Rules Found |

---

### `RampNoTime`

[Class Documentation][blockdocs-RampNoTime]

**[Subclass of `Ramp`](#ramp)**

#### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| type | Examples: `"dwell", "ramp", "quench"` | No Rules Found |

#### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | No Rules Found |
| temp | The next temperature in the program.<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). | No Rules Found |
| time | How long it took to get from the last temperature to the new temperature.<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). | No Rules Found |
| rate | The sign-sensitive rate at which temperature was changed to get to the new temperature. (Increase -> positive, Decrease -> negative).<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). | No Rules Found |
| temp_unit | `FOSTempUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) which allows a little more coersion of temperature units. (Like recognizing `"C"` as degrees celsius as opposed to coulombs) | No Rules Found |
| time_unit | `FOSUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) with a class method for enforcing the correct dimensionality of the unit. | No Rules Found |
| rate_unit | Makes use of [`pint`'s dimensionality properties](https://pint.readthedocs.io/en/stable/) to verify that the value is a unit of temperature over time. | No Rules Found |

---

### `Reaction`

[Class Documentation][blockdocs-Reaction]

**[Subclass of `SingleBlock`](#singleblock)**

#### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| nominal_formula | Chemical composition written in a [ChemFormula](https://pypi.org/project/chemformula/) compatible format | No Rules Found |
| nominal_amount | Total amount expected to be recovered from all participating reactants.<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). | No Rules Found |
| nominal_amount_unit | `FOSUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) with a class method for enforcing the correct dimensionality of the unit. | No Rules Found |

#### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | No Rules Found |

---

### `SingleBlock`

[Class Documentation][blockdocs-SingleBlock]

**[Subclass of `Block`](#block)**

#### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |

#### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | No Rules Found |

---

### `Synthesis`

[Class Documentation][blockdocs-Synthesis]

**[Subclass of `FileBlock`](#fileblock)**

#### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| metadata | General information about the file. Additional requirements from basic [file metadata](#metadata). Lines at the beginning of a FOS-formatted file without a header will automatically be interpreted as a `MetaData` dictionary | No Rules Found |
| experimenters | A [simple list](#listblock-and-simple-lists) of [`Experimenter` objects](#experimenter) | No Rules Found |
| reaction | [General reaction information](#reaction) | No Rules Found |
| products | A [simple list](#listblock-and-simple-lists) of [`Product` objects](#product) | No Rules Found |
| materials | A [specialized `ListBlock`](#listblock-and-simple-lists) of [`Material` objects](#material) | No Rules Found |
| treatments | A [simple list](#listblock-and-simple-lists) of [`Treatment` objects](#treatment) | No Rules Found |

#### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | No Rules Found |
| cif | [A single attached CIF file](#attachment) | No Rules Found |
| cifs | A [simple list](#listblock-and-simple-lists) of [attached CIF files](#attachment) | No Rules Found |
| laboratory_conditions | [General Laboratory Conditions](#singleblock-method-subclasses) | No Rules Found |
| equipment | A [simple list](#listblock-and-simple-lists) of [`Equipment` objects](#singleblock-method-subclasses) | No Rules Found |

---

### `SynthesisMeta`

[Class Documentation][blockdocs-SynthesisMeta]

**[Subclass of `MetaData`](#metadata)**

#### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| fos_id | Identifiable ID for the synthesis or sample.<br><br>**For [`Synthesis`](#synthesismeta) files:** this should be kept informative and unique within the scope of the project_id, as it may be used as identification for future database storage.<br>**For [`TemplateSet`](#templateset) files:** it is for convenience. | No Rules Found |
| fos_type | What type of `FileBlock` subclass the file should be interpreted as. Expected values are:<br>`synthesis`<br>`templates` | No Rules Found |
| description | A brief description of the intent for the file (characteristic methods, target products, template category, etc.). | No Rules Found |
| group_id | A unique identifier for the research group or organization.<br><br>**In the future:** unique group_id values should be standardized and/or issued by a central party to ensure that all future database uploads have a unique index location.<br>**For now:** group_id values can be verified unique by ending with the primary investigator's ORCID (example: kovnir-0000-0003-1152-1912). After standardization, tools will be developed to convert group_id values for entire group repositories. | No Rules Found |
| project_id | An identifier that only needs to be unique within the scope of the group_id. This can be more flexible to the needs of the group, but good practice is to keep synthesis files in a folder structure that matches project_id values. A large experimental group, for example, might categorize syntheses by experimenter then project, or vice versa for intra-collaboration. To avoid future conflicts, name-based categories should be given unique suffixes, like university ID/username or the last 4 digits of the ORCID. Some examples:<br> `travis5672/clathrates`, `travis(errthumt)/pnictides`, `thermoelectrics/travis5672/Ba2-TM5-Pn6`<br><br>***Future Tools** will expect project_ids to reflect folder structure using "`/`" or "`\`" delimiters.* | No Rules Found |

#### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | No Rules Found |

---

### `TemplateBlock`

[Class Documentation][blockdocs-TemplateBlock]

**[Subclass of `SingleBlock`](#singleblock)**

#### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| template_name | An identifiable name for the template. | No Rules Found |

#### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | No Rules Found |

`TemplateBlock` is used to make hybridized subclasses of other `SingleBlock` subclasses. Template subclasses override required properties of the original class with template fields that can be later filled in and passed to their validators with the `fill()` method. Refer to the [code example walkthrough](../examples/code_example/index.md) for some uses of templates.


#### TemplateBlock Method Subclasses

These subclasses don't currently have any additional required properties but will either be expanded in the future or have specialized methods.

- `FlexTemplate`: Same functionality as `TemplateBlock`, but automatically interprets missing input as template fields rather than having preset expectations for which fields are unfilled. Used for [`reflex()`](../blocks/blocks.md#FoSpy.blocks.blocks.SingleBlock.reflex) method and [`TemplateList`](../blocks/template.md#FoSpy.blocks.template.TemplateList) construction.---

### `TemplateSet`

[Class Documentation][blockdocs-TemplateSet]

**[Subclass of `FileBlock`](#fileblock)**

#### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| metadata | General information about the file. Lines at the beginning of a FOS-formatted file without a header will automatically be interpreted as a `MetaData` dictionary | No Rules Found |

#### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | No Rules Found |
| experimenters | A list of incomplete [`Experimenter` objects](#experimenter) | No Rules Found |
| materials | A list of incomplete [`Material` objects](#material) | No Rules Found |
| treatments | A list of incomplete [`Treatment` objects](#treatment) | No Rules Found |
| annealings | A list of incomplete [`Annealing` objects](#annealing) | No Rules Found |
| anneal_sections | A list of incomplete [`AnnealSection` objects](#annealsection) | No Rules Found |
| cifs | A [simple list](#listblock-and-simple-lists) of [attached CIF files](#attachment) | No Rules Found |

#### Optional properties

In contrast with a `Synthesis` file, most top-level properties for a `TemplateSet` are expected to contain [lists of templates](#templatelists) of a given type. `TemplateList.Simple()` allows entries to be incomplete and generates hybridized `TemplateBlock` subclasses for them.

Developers are currently working on ways to flexibly allow any template list in a `TemplateSet`. For now, refer to [modifying validation at runtime](#modifying-property-validation-at-runtime) or reach out to developers if current standards are limiting how you want to use templates.

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| metadata | General information about the file. Lines at the beginning of a FOS-formatted file without a header will automatically be interpreted as a `MetaData` dictionary | No Rules Found |

---

### `TraceData`

[Class Documentation][blockdocs-TraceData]

**[Subclass of `SingleBlock`](#singleblock)**

#### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |

#### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | No Rules Found |

---

### `Treatment`

[Class Documentation][blockdocs-Treatment]

**[Subclass of `SingleBlock`](#singleblock)**

#### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| type | What type of treatment was performed | No Rules Found |
| repeats | How many times it was performed in succession (if interrupted by other treatments, add a different treatment block after the interrupting treatments) | No Rules Found |
| observations | General observations | No Rules Found |

#### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | No Rules Found |
| recovered_amount | How much material was recovered after treatment. <br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). | No Rules Found |
| recovered_amount_unit | `FOSUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) with a class method for enforcing the correct dimensionality of the unit. | No Rules Found |
| start_time | What time the treatment was started | No Rules Found |
| end_time | What time the treatment was finished | No Rules Found |

---
