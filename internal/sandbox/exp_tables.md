
## `AnnealSection`

[Class Documentation][blockdocs-AnnealSection]

**[Subclass of `SingleBlock`](#singleblock)**

### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| type | Examples: `"dwell", "ramp", "quench"` | Rules not found |

### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | Rules not found |


## `Annealing`

[Class Documentation][blockdocs-Annealing]

**[Subclass of `Treatment`](#treatment)**

### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| type | What type of treatment was performed | Rules not found |
| repeats | How many times it was performed in succession (if interrupted by other treatments, add a different treatment block after the interrupting treatments) | Rules not found |
| observations | General observations | Rules not found |
| program | A [specialized `ListBlock`](#listblock-and-simple-lists) of [`AnnealSection` objects](#annealsection) | Rules not found |
| start_temp | The initial temperature of the annealing profile.<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). | Rules not found |
| start_temp_unit | `FOSTempUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) which allows a little more coersion of temperature units. (Like recognizing `"C"` as degrees celsius as opposed to coulombs) | Rules not found |

### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | Rules not found |
| recovered_amount | How much material was recovered after treatment. <br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). | Rules not found |
| recovered_amount_unit | `FOSUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) with a class method for enforcing the correct dimensionality of the unit. | Rules not found |
| start_time | What time the treatment was started | Rules not found |
| end_time | What time the treatment was finished | Rules not found |
| gas_flow | A [simple list](#listblock-and-simple-lists) of [`GasFlow` objects](#singleblock-method-subclasses) | Rules not found |


## `Attachment`

[Class Documentation][blockdocs-Attachment]

**[Subclass of `SingleBlock`](#singleblock)**

### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| file_name | A name for the file that does not contain any incompatible characters ( `\ / : * ? " < > \|`). Must include a valid extension. Some subclasses (like `CIFFile`) are dispatched based on detected file extension. | Rules not found |

### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | Rules not found |
| embedded | A list of raw utf-8 line strings copied from the embedded file. See [attachments guide](../guides/attachments.md) for syntax. | Rules not found |
| path | Instead of directly embedding contents, refers to a relative path from the folder containing the parent `FileBlock`. Can use relative characters like "." and "..". See [attachments guide](../guides/attachments.md) for more information.<br> `PathPosix` validator is a subclass of `pathlib.Path` which always uses back slashes (`/`) instead of forward slashes (`\`) when serialized, regardless of OS | Rules not found |

#### Additional Requirements

In addition to the required properties above, all `Attachment` objects must be constructed with one of the following optional properties:

- `embedded`
- `path`

The first matching property found will be used and the remainder will be discarded. The presence of one of these properties is used to identify what form of file attachment it is. Refer to the [attachments guide](../guides/attachments.md) for more information

---


#### Attachment Method Subclasses

Attachment Subclasses are hybridized between an **attachment type** and a **file type**. Attachment types share most method names to be called by *file type* methods, but method source code differs on the basis of how the file was attached. For example, `_get_filepath()` for [`PathFile`](../blocks/attachments.md#FoSpy.blocks.attachments.PathFile._get_filepath) simply returns an absolute filepath resolved from the value in its `path` attribute, whereas [`EmbeddedFile`](../blocks/attachments.md#FoSpy.blocks.attachments.EmbeddedFile._get_filepath) objects create a temporary file to print their embedded lines to before returning its filepath.

Attachment types are dispatched based on which optional properties they have. File types are dispatched based on extension. Unrecognized extensions simply don't add any special file type methods.

##### Attachment Types

- `EmbeddedFile`
- `PathFile`

---

##### File Types

- `CIFFile`

---
## `CIFFile`

[Class Documentation][blockdocs-CIFFile]

**[Subclass of `Attachment`](#attachment)**

### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| file_name | A name for the file that does not contain any incompatible characters ( `\ / : * ? " < > \|`). Must include a valid extension. Some subclasses (like `CIFFile`) are dispatched based on detected file extension. | Rules not found |

### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | Rules not found |
| embedded | A list of raw utf-8 line strings copied from the embedded file. See [attachments guide](../guides/attachments.md) for syntax. | Rules not found |
| path | Instead of directly embedding contents, refers to a relative path from the folder containing the parent `FileBlock`. Can use relative characters like "." and "..". See [attachments guide](../guides/attachments.md) for more information.<br> `PathPosix` validator is a subclass of `pathlib.Path` which always uses back slashes (`/`) instead of forward slashes (`\`) when serialized, regardless of OS | Rules not found |


## `CSVdata`

[Class Documentation][blockdocs-CSVdata]

**[Subclass of `SingleBlock`](#singleblock)**

### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |

### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | Rules not found |


## `Dwell`

[Class Documentation][blockdocs-Dwell]

**[Subclass of `AnnealSection`](#annealsection)**

### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| type | Examples: `"dwell", "ramp", "quench"` | Rules not found |
| time | How long the temperature was kept constant in this section.<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). | Rules not found |
| time_unit | `FOSUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) with a class method for enforcing the correct dimensionality of the unit. | Rules not found |

### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | Rules not found |


## `EmbeddedFile`

[Class Documentation][blockdocs-EmbeddedFile]

**[Subclass of `Attachment`](#attachment)**

### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| file_name | A name for the file that does not contain any incompatible characters ( `\ / : * ? " < > \|`). Must include a valid extension. Some subclasses (like `CIFFile`) are dispatched based on detected file extension. | Rules not found |

### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | Rules not found |
| embedded | A list of raw utf-8 line strings copied from the embedded file. See [attachments guide](../guides/attachments.md) for syntax. | Rules not found |
| path | Instead of directly embedding contents, refers to a relative path from the folder containing the parent `FileBlock`. Can use relative characters like "." and "..". See [attachments guide](../guides/attachments.md) for more information.<br> `PathPosix` validator is a subclass of `pathlib.Path` which always uses back slashes (`/`) instead of forward slashes (`\`) when serialized, regardless of OS | Rules not found |


## `Equipment`

[Class Documentation][blockdocs-Equipment]

**[Subclass of `SingleBlock`](#singleblock)**

### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |

### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | Rules not found |


## `Experimenter`

[Class Documentation][blockdocs-Experimenter]

**[Subclass of `SingleBlock`](#singleblock)**

### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| name | Name of the experimenter | Rules not found |
| affiliation | Lab/University/Research Group/etc. | Rules not found |

### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | Rules not found |
| orcid | The experimenter's [ORCID](https://orcid.org/) | Rules not found |


## `FileBlock`

[Class Documentation][blockdocs-FileBlock]

**[Subclass of `SingleBlock`](#singleblock)**

### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| metadata | General information about the file. Lines at the beginning of a FOS-formatted file without a header will automatically be interpreted as a `MetaData` dictionary | Rules not found |

### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | Rules not found |


## `FlexTemplate`

[Class Documentation][blockdocs-FlexTemplate]

**[Subclass of `TemplateBlock`](#templateblock)**

### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| template_name | An identifiable name for the template. | Rules not found |

### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | Rules not found |


## `GasFlow`

[Class Documentation][blockdocs-GasFlow]

**[Subclass of `SingleBlock`](#singleblock)**

### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |

### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | Rules not found |


## `LabConditions`

[Class Documentation][blockdocs-LabConditions]

**[Subclass of `SingleBlock`](#singleblock)**

### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |

### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | Rules not found |


## `Material`

[Class Documentation][blockdocs-Material]

**[Subclass of `SingleBlock`](#singleblock)**

### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| name | Identifiable name for the material | Rules not found |
| type | How it was used in the synthesis (e.g., reagent, flux, solvent) | Rules not found |
| formula | Chemical composition written in a [ChemFormula](https://pypi.org/project/chemformula/) compatible format | Rules not found |
| supplier | Source of purchase/synthesis (may be internal) | Rules not found |
| cas | CAS ID. May be "unknown" | Rules not found |
| form | Physical shape or state of the material **at time of acquisition** (e.g., powder, shot, wire, lump). If the material was modified after aquiring but before use in the synthesis (like grinding into powder, drying, etc.), these actions should be specified in the *material's* treatments property (not the synthesis treatments). | Rules not found |
| env | What environment the material is stored in. (e.g., ambient, Ar(g)) | Rules not found |
| amount | Amount that was used.<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). | Rules not found |
| amount_unit | Descriptive unit for amount. Dimensionality may be enforced in the future once more input is gained from experimenters. | Rules not found |

### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | Rules not found |
| purity | 0 < purity ≤ 1 | Rules not found |
| treatments | A [simple list](#listblock-and-simple-lists) of [`Treatment` objects](#treatment)<br>Any modifications to the material between acquisition and use in the synthesis. | Rules not found |


## `MetaData`

[Class Documentation][blockdocs-MetaData]

**[Subclass of `SingleBlock`](#singleblock)**

### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| fos_id | Identifiable ID for the synthesis or sample.<br><br>**For [`Synthesis`](#synthesismeta) files:** this should be kept informative and unique within the scope of the project_id, as it may be used as identification for future database storage.<br>**For [`TemplateSet`](#templateset) files:** it is for convenience. | Rules not found |
| fos_type | What type of `FileBlock` subclass the file should be interpreted as. Expected values are:<br>`synthesis`<br>`templates` | Rules not found |
| description | A brief description of the intent for the file (characteristic methods, target products, template category, etc.). | Rules not found |

### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | Rules not found |


## `PathFile`

[Class Documentation][blockdocs-PathFile]

**[Subclass of `Attachment`](#attachment)**

### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| file_name | A name for the file that does not contain any incompatible characters ( `\ / : * ? " < > \|`). Must include a valid extension. Some subclasses (like `CIFFile`) are dispatched based on detected file extension. | Rules not found |

### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | Rules not found |
| embedded | A list of raw utf-8 line strings copied from the embedded file. See [attachments guide](../guides/attachments.md) for syntax. | Rules not found |
| path | Instead of directly embedding contents, refers to a relative path from the folder containing the parent `FileBlock`. Can use relative characters like "." and "..". See [attachments guide](../guides/attachments.md) for more information.<br> `PathPosix` validator is a subclass of `pathlib.Path` which always uses back slashes (`/`) instead of forward slashes (`\`) when serialized, regardless of OS | Rules not found |


## `Product`

[Class Documentation][blockdocs-Product]

**[Subclass of `SingleBlock`](#singleblock)**

### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| name | Identifiable name for the product. | Rules not found |
| expected | Whether or not it was expected from the synthesis. | Rules not found |
| obtained | Whether or not it was obtained from the synthesis. | Rules not found |
| formula | Chemical composition written in a [ChemFormula](https://pypi.org/project/chemformula/) compatible format. | Rules not found |
| observations | General observations about the product. | Rules not found |

### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | Rules not found |
| expected_amount | How much of the product was nominally expected to be obtained from the synthesis.<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). | Rules not found |
| expected_amount_unit | `FOSUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) with a class method for enforcing the correct dimensionality of the unit. (In this case mass or volume) | Rules not found |
| obtained_amount | How much of the product was actually obtained from the synthesis.<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). | Rules not found |
| obtained_amount_unit | `FOSUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) with a class method for enforcing the correct dimensionality of the unit. (In this case mass or volume) | Rules not found |
| characterizations | Description of characterization methods used to determine/quantitate the product. | Rules not found |
| structure_comments | General description on the structure of the product. | Rules not found |


## `Quench`

[Class Documentation][blockdocs-Quench]

**[Subclass of `AnnealSection`](#annealsection)**

### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| type | Examples: `"dwell", "ramp", "quench"` | Rules not found |
| medium | What medium the reaction vessel was quenched in (e.g., water, air). | Rules not found |

### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | Rules not found |


## `Ramp`

[Class Documentation][blockdocs-Ramp]

**[Subclass of `AnnealSection`](#annealsection)**

### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| type | Examples: `"dwell", "ramp", "quench"` | Rules not found |

### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | Rules not found |
| temp | The next temperature in the program.<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). | Rules not found |
| time | How long it took to get from the last temperature to the new temperature.<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). | Rules not found |
| rate | The sign-sensitive rate at which temperature was changed to get to the new temperature. (Increase -> positive, Decrease -> negative).<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). | Rules not found |
| temp_unit | `FOSTempUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) which allows a little more coersion of temperature units. (Like recognizing `"C"` as degrees celsius as opposed to coulombs) | Rules not found |
| time_unit | `FOSUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) with a class method for enforcing the correct dimensionality of the unit. | Rules not found |
| rate_unit | Makes use of [`pint`'s dimensionality properties](https://pint.readthedocs.io/en/stable/) to verify that the value is a unit of temperature over time. | Rules not found |

#### Required properties

During construction of a `Ramp` object, it is required to have at least 2 of the following optional properties, with their respective units:

- `temp`
- `time`
- `rate`

If all three are provided, the last one found during reading will be discarded as redundant data, and the object is [dispatched](#dispatching-subclasses) to a `Ramp` subclass with a "retrieval" method for calculating the missing property (e.g., `get_temp()`, `get_time()`, or `get_rate()`) When working with `Ramp` objects in the FoSpy framework, it is best practice to always use the "retrieval" methods. For subclasses that *do* have the desired property, retrieval methods default to returning it directly.


| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | Rules not found |
| temp | The next temperature in the program.<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). | Rules not found |
| time | How long it took to get from the last temperature to the new temperature.<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). | Rules not found |
| rate | The sign-sensitive rate at which temperature was changed to get to the new temperature. (Increase -> positive, Decrease -> negative).<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). | Rules not found |
| temp_unit | `FOSTempUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) which allows a little more coersion of temperature units. (Like recognizing `"C"` as degrees celsius as opposed to coulombs) | Rules not found |
| time_unit | `FOSUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) with a class method for enforcing the correct dimensionality of the unit. | Rules not found |
| rate_unit | Makes use of [`pint`'s dimensionality properties](https://pint.readthedocs.io/en/stable/) to verify that the value is a unit of temperature over time. | Rules not found |


---


#### Ramp Method Subclasses

The following subclasses are dispatched based on the redundant parameter (see [Required Properties](#ramp) above) and override the retrieval method to calculate the missing parameter instead of getting it from attributes:

- `RampNoRate`: overrides [`get_rate()`](../blocks/treatments.md#FoSpy.blocks.treatments.RampNoRate.get_rate)
- `RampNoTemp`: overrides [`get_temp()`](../blocks/treatments.md#FoSpy.blocks.treatments.RampNoRate.get_temp)
- `RampNoTime`: overrides [`get_time()`](../blocks/treatments.md#FoSpy.blocks.treatments.RampNoRate.get_time)

---
## `RampNoRate`

[Class Documentation][blockdocs-RampNoRate]

**[Subclass of `Ramp`](#ramp)**

### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| type | Examples: `"dwell", "ramp", "quench"` | Rules not found |

### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | Rules not found |
| temp | The next temperature in the program.<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). | Rules not found |
| time | How long it took to get from the last temperature to the new temperature.<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). | Rules not found |
| rate | The sign-sensitive rate at which temperature was changed to get to the new temperature. (Increase -> positive, Decrease -> negative).<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). | Rules not found |
| temp_unit | `FOSTempUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) which allows a little more coersion of temperature units. (Like recognizing `"C"` as degrees celsius as opposed to coulombs) | Rules not found |
| time_unit | `FOSUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) with a class method for enforcing the correct dimensionality of the unit. | Rules not found |
| rate_unit | Makes use of [`pint`'s dimensionality properties](https://pint.readthedocs.io/en/stable/) to verify that the value is a unit of temperature over time. | Rules not found |


## `RampNoTemp`

[Class Documentation][blockdocs-RampNoTemp]

**[Subclass of `Ramp`](#ramp)**

### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| type | Examples: `"dwell", "ramp", "quench"` | Rules not found |

### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | Rules not found |
| temp | The next temperature in the program.<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). | Rules not found |
| time | How long it took to get from the last temperature to the new temperature.<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). | Rules not found |
| rate | The sign-sensitive rate at which temperature was changed to get to the new temperature. (Increase -> positive, Decrease -> negative).<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). | Rules not found |
| temp_unit | `FOSTempUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) which allows a little more coersion of temperature units. (Like recognizing `"C"` as degrees celsius as opposed to coulombs) | Rules not found |
| time_unit | `FOSUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) with a class method for enforcing the correct dimensionality of the unit. | Rules not found |
| rate_unit | Makes use of [`pint`'s dimensionality properties](https://pint.readthedocs.io/en/stable/) to verify that the value is a unit of temperature over time. | Rules not found |


## `RampNoTime`

[Class Documentation][blockdocs-RampNoTime]

**[Subclass of `Ramp`](#ramp)**

### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| type | Examples: `"dwell", "ramp", "quench"` | Rules not found |

### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | Rules not found |
| temp | The next temperature in the program.<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). | Rules not found |
| time | How long it took to get from the last temperature to the new temperature.<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). | Rules not found |
| rate | The sign-sensitive rate at which temperature was changed to get to the new temperature. (Increase -> positive, Decrease -> negative).<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). | Rules not found |
| temp_unit | `FOSTempUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) which allows a little more coersion of temperature units. (Like recognizing `"C"` as degrees celsius as opposed to coulombs) | Rules not found |
| time_unit | `FOSUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) with a class method for enforcing the correct dimensionality of the unit. | Rules not found |
| rate_unit | Makes use of [`pint`'s dimensionality properties](https://pint.readthedocs.io/en/stable/) to verify that the value is a unit of temperature over time. | Rules not found |


## `Reaction`

[Class Documentation][blockdocs-Reaction]

**[Subclass of `SingleBlock`](#singleblock)**

### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| nominal_formula | Chemical composition written in a [ChemFormula](https://pypi.org/project/chemformula/) compatible format | Rules not found |
| nominal_amount | Total amount expected to be recovered from all participating reactants.<br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). | Rules not found |
| nominal_amount_unit | `FOSUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) with a class method for enforcing the correct dimensionality of the unit. | Rules not found |

### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | Rules not found |


## `SingleBlock`

[Class Documentation][blockdocs-SingleBlock]

**[Subclass of `Block`](#block)**

### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |

### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | Rules not found |


## `Synthesis`

[Class Documentation][blockdocs-Synthesis]

**[Subclass of `FileBlock`](#fileblock)**

### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| metadata | General information about the file. Additional requirements from basic [file metadata](#metadata). Lines at the beginning of a FOS-formatted file without a header will automatically be interpreted as a `MetaData` dictionary | Rules not found |
| experimenters | A [simple list](#listblock-and-simple-lists) of [`Experimenter` objects](#experimenter) | Rules not found |
| reaction | [General reaction information](#reaction) | Rules not found |
| products | A [simple list](#listblock-and-simple-lists) of [`Product` objects](#product) | Rules not found |
| materials | A [specialized `ListBlock`](#listblock-and-simple-lists) of [`Material` objects](#material) | Rules not found |
| treatments | A [simple list](#listblock-and-simple-lists) of [`Treatment` objects](#treatment) | Rules not found |

### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | Rules not found |
| cif | [A single attached CIF file](#attachment) | Rules not found |
| cifs | A [simple list](#listblock-and-simple-lists) of [attached CIF files](#attachment) | Rules not found |
| laboratory_conditions | [General Laboratory Conditions](#singleblock-method-subclasses) | Rules not found |
| equipment | A [simple list](#listblock-and-simple-lists) of [`Equipment` objects](#singleblock-method-subclasses) | Rules not found |


## `SynthesisMeta`

[Class Documentation][blockdocs-SynthesisMeta]

**[Subclass of `MetaData`](#metadata)**

### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| fos_id | Identifiable ID for the synthesis or sample.<br><br>**For [`Synthesis`](#synthesismeta) files:** this should be kept informative and unique within the scope of the project_id, as it may be used as identification for future database storage.<br>**For [`TemplateSet`](#templateset) files:** it is for convenience. | Rules not found |
| fos_type | What type of `FileBlock` subclass the file should be interpreted as. Expected values are:<br>`synthesis`<br>`templates` | Rules not found |
| description | A brief description of the intent for the file (characteristic methods, target products, template category, etc.). | Rules not found |
| group_id | A unique identifier for the research group or organization.<br><br>**In the future:** unique group_id values should be standardized and/or issued by a central party to ensure that all future database uploads have a unique index location.<br>**For now:** group_id values can be verified unique by ending with the primary investigator's ORCID (example: kovnir-0000-0003-1152-1912). After standardization, tools will be developed to convert group_id values for entire group repositories. | Rules not found |
| project_id | An identifier that only needs to be unique within the scope of the group_id. This can be more flexible to the needs of the group, but good practice is to keep synthesis files in a folder structure that matches project_id values. A large experimental group, for example, might categorize syntheses by experimenter then project, or vice versa for intra-collaboration. To avoid future conflicts, name-based categories should be given unique suffixes, like university ID/username or the last 4 digits of the ORCID. Some examples:<br> `travis5672/clathrates`, `travis(errthumt)/pnictides`, `thermoelectrics/travis5672/Ba2-TM5-Pn6`<br><br>***Future Tools** will expect project_ids to reflect folder structure using "`/`" or "`\`" delimiters.* | Rules not found |

### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | Rules not found |


## `TemplateBlock`

[Class Documentation][blockdocs-TemplateBlock]

**[Subclass of `SingleBlock`](#singleblock)**

### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| template_name | An identifiable name for the template. | Rules not found |

### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | Rules not found |

`TemplateBlock` is used to make hybridized subclasses of other `SingleBlock` subclasses. Template subclasses override required properties of the original class with template fields that can be later filled in and passed to their validators with the `fill()` method. Refer to the [code example walkthrough](../examples/code_example/index.md) for some uses of templates.


#### TemplateBlock Method Subclasses

These subclasses don't currently have any additional required properties but will either be expanded in the future or have specialized methods.

- `FlexTemplate`: Same functionality as `TemplateBlock`, but automatically interprets missing input as template fields rather than having preset expectations for which fields are unfilled. Used for [`reflex()`](../blocks/blocks.md#FoSpy.blocks.blocks.SingleBlock.reflex) method and [`TemplateList`](../blocks/template.md#FoSpy.blocks.template.TemplateList) construction.

---
## `TemplateSet`

[Class Documentation][blockdocs-TemplateSet]

**[Subclass of `FileBlock`](#fileblock)**

### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| metadata | General information about the file. Lines at the beginning of a FOS-formatted file without a header will automatically be interpreted as a `MetaData` dictionary | Rules not found |

### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | Rules not found |
| experimenters | A list of incomplete [`Experimenter` objects](#experimenter) | Rules not found |
| materials | A list of incomplete [`Material` objects](#material) | Rules not found |
| treatments | A list of incomplete [`Treatment` objects](#treatment) | Rules not found |
| annealings | A list of incomplete [`Annealing` objects](#annealing) | Rules not found |
| anneal_sections | A list of incomplete [`AnnealSection` objects](#annealsection) | Rules not found |
| cifs | A [simple list](#listblock-and-simple-lists) of [attached CIF files](#attachment) | Rules not found |

#### Optional properties

In contrast with a `Synthesis` file, most top-level properties for a `TemplateSet` are expected to contain [lists of templates](#templatelists) of a given type. `TemplateList.Simple()` allows entries to be incomplete and generates hybridized `TemplateBlock` subclasses for them.

Developers are currently working on ways to flexibly allow any template list in a `TemplateSet`. For now, refer to [modifying validation at runtime](#modifying-property-validation-at-runtime) or reach out to developers if current standards are limiting how you want to use templates.

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| metadata | General information about the file. Lines at the beginning of a FOS-formatted file without a header will automatically be interpreted as a `MetaData` dictionary | Rules not found |


---
## `TraceData`

[Class Documentation][blockdocs-TraceData]

**[Subclass of `SingleBlock`](#singleblock)**

### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |

### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | Rules not found |


## `Treatment`

[Class Documentation][blockdocs-Treatment]

**[Subclass of `SingleBlock`](#singleblock)**

### Required properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| type | What type of treatment was performed | Rules not found |
| repeats | How many times it was performed in succession (if interrupted by other treatments, add a different treatment block after the interrupting treatments) | Rules not found |
| observations | General observations | Rules not found |

### Optional properties

| Property | Description | Validation Rules |
| -------- | ----------- | ---------------- |
| rename | A dictionary of old_name:new_name pairs for renaming properties within the `SingleBlock` subclass while keeping them in sync with their validators. Refer to the [code example walkthrough](../examples/code_example/index.md) for usage. | Rules not found |
| recovered_amount | How much material was recovered after treatment. <br>Values are attached to the required unit and constructed into a [`pint.Quantity` object](https://pint.readthedocs.io/en/stable/). | Rules not found |
| recovered_amount_unit | `FOSUnit` is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) with a class method for enforcing the correct dimensionality of the unit. | Rules not found |
| start_time | What time the treatment was started | Rules not found |
| end_time | What time the treatment was finished | Rules not found |

