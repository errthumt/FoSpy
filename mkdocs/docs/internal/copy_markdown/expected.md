# Expected Properties: Raw Code

There is a copy button in the top right of the code block.

[Click here to go to the rendered version](../../expected/index.md)

````markdown
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
|------------|---------------------------------------|----------------------------------|
| type | Examples: `"dwell", "ramp", "quench"` | <ul><li>Any text entry</li></ul> |

#### Optional properties

| Property | Description | Validation Rules |
|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| rename | Maps default expected property names to custom names. Useful for when expected properties *are* present and matching descriptions, but the default name doesn't align with the niche context. (e.g., `"experimenters"` might be mapped to the more generic `"collaborators"` for computational or meta-contexted FOS files.) | <ul><li>A dictionary of key:value string pairs</li><li>Keys starting with "`_`" are ignored.</li><li>Keys must be expected property names for the block.<ul><li>For unexpected (custom) keys, renaming is not necessary.</li></ul></li><li>Values cannot be registered property names.</li></ul> |

---
### `Annealing`

[Class Documentation][blockdocs-Annealing]

**[Subclass of `Treatment`](#treatment)**

#### Required properties

| Property | Description | Validation Rules |
|-----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| type | What type of treatment was performed. | <ul><li>Any text entry</li></ul> |
| repeats | How many times the treatment was performed in succession *uninterrupted*. If other treatments are performed between repeats, add a different treatment block after the interrupting treatments. | <ul><li>Any integer (positive or negative)</li></ul> |
| program | The temperatures and gradients used during annealing. | <ul><li>A [specialized `ListBlock`][blockdocs-AnnealProgram] of [`AnnealSection` objects.](#annealsection)</li></ul> |
| start_temp | Initial temperature at start of program. | <ul><li>Positive decimal value</li><li>Requires that `start_temp_unit` also be present</li></ul> |
| start_temp_unit | Units for initial temperature. | <ul><li>Validator is a subclass of [`pint`'s `Unit` class](https://pint.readthedocs.io/en/stable/) With more flexibility for recognizing temperature units.</li><li>Must be a recognizable unit for temperature.</li></ul> |

#### Optional properties

| Property | Description | Validation Rules |
|-----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| rename | Maps default expected property names to custom names. Useful for when expected properties *are* present and matching descriptions, but the default name doesn't align with the niche context. (e.g., `"experimenters"` might be mapped to the more generic `"collaborators"` for computational or meta-contexted FOS files.) | <ul><li>A dictionary of key:value string pairs</li><li>Keys starting with "`_`" are ignored.</li><li>Keys must be expected property names for the block.<ul><li>For unexpected (custom) keys, renaming is not necessary.</li></ul></li><li>Values cannot be registered property names.</li></ul> |
| observations | General observations during the treatment | <ul><li>Any text entry</li></ul> |
| recovered_amount | How much material was recovered after treatment. | <ul><li>Positive decimal value</li><li>Requires that `recovered_amount_unit` also be present</li></ul> |
| recovered_amount_unit | Units for treatment recovered amount. | <ul><li>Validator is a subclass of [`pint`'s `Unit` class](https://pint.readthedocs.io/en/stable/) With additional rules enforcing the correct dimensionality of the unit.</li><li>Allowed dimensions:<ul><li>[mass]</li><li>[length]^3</li></ul></li></ul> |
| start_time | What time the treatment was started | <ul><li>Any text entry</li></ul> |
| end_time | What time the treatment was finished | <ul><li>Any text entry</li></ul> |
| gas_flow | Consistent gas flow conditions applied during annealing. | <ul><li>A [simple `ListBlock`](#listblock-and-simple-lists) of [`GasFlow` objects.](#gasflow)</li></ul> |

---
### `Attachment`

[Class Documentation][blockdocs-Attachment]

**[Subclass of `SingleBlock`](#singleblock)**

#### Required properties

| Property | Description | Validation Rules |
|------------|------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| file_name | The name of the attached file (with extension) | <ul><li>A valid filename (no path, no separators, allowed characters only).</li><li>Must include a valid extension.</li><li>Allowed characters: letters, digits, '`_`', '`-`', '`.`'</li><li>Commas are allowed, but may lead to unexpected behavior for some OS or software.</li><li>Paths to nonexistent files will be validated, but may raise errors when the parent `FileBlock` attempts to track the file.</li></ul> |

#### Optional properties

| Property | Description | Validation Rules |
|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| rename | Maps default expected property names to custom names. Useful for when expected properties *are* present and matching descriptions, but the default name doesn't align with the niche context. (e.g., `"experimenters"` might be mapped to the more generic `"collaborators"` for computational or meta-contexted FOS files.) | <ul><li>A dictionary of key:value string pairs</li><li>Keys starting with "`_`" are ignored.</li><li>Keys must be expected property names for the block.<ul><li>For unexpected (custom) keys, renaming is not necessary.</li></ul></li><li>Values cannot be registered property names.</li></ul> |
| embedded | Attachment content embedded as raw `utf-8` line strings. | <ul><li>Mutually exclusive with `path` property.</li><li>Attachment content as a list of raw `utf-8` line strings.</li></ul> |
| path | The filepath to the attached file, relative to the directory containing the parent `FileBlock`. | <ul><li>Mutually exclusive with `embedded` property.</li><li>A valid relative filepath to a directory.</li><li>Path is relative to the directory containing the parent `FileBlock`.</li><li>"`.`" should be used to indicate the same directory as the parent `FileBlock`.</li><li>"`..`" can be used to walk up the directory tree.</li><li>Paths to nonexistent directories will be validated, but may raise errors when the parent `FileBlock` attempts to track the file.</li><li>Examples for a `FileBlock` at `/home/user/synthesis.fos`:<ul><li>"`.`" is `/home/user`</li><li>"`..`" is `/home`</li><li>"`../foo`" is `/home/foo`</li><li>"`./bar`" is `/home/user/bar`</li></ul></li></ul> |

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
|------------|------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| file_name | The name of the attached file (with extension) | <ul><li>A valid filename (no path, no separators, allowed characters only).</li><li>Must include a valid extension.</li><li>Allowed characters: letters, digits, '`_`', '`-`', '`.`'</li><li>Commas are allowed, but may lead to unexpected behavior for some OS or software.</li><li>Paths to nonexistent files will be validated, but may raise errors when the parent `FileBlock` attempts to track the file.</li></ul> |

#### Optional properties

| Property | Description | Validation Rules |
|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| rename | Maps default expected property names to custom names. Useful for when expected properties *are* present and matching descriptions, but the default name doesn't align with the niche context. (e.g., `"experimenters"` might be mapped to the more generic `"collaborators"` for computational or meta-contexted FOS files.) | <ul><li>A dictionary of key:value string pairs</li><li>Keys starting with "`_`" are ignored.</li><li>Keys must be expected property names for the block.<ul><li>For unexpected (custom) keys, renaming is not necessary.</li></ul></li><li>Values cannot be registered property names.</li></ul> |
| embedded | Attachment content embedded as raw `utf-8` line strings. | <ul><li>Mutually exclusive with `path` property.</li><li>Attachment content as a list of raw `utf-8` line strings.</li></ul> |
| path | The filepath to the attached file, relative to the directory containing the parent `FileBlock`. | <ul><li>Mutually exclusive with `embedded` property.</li><li>A valid relative filepath to a directory.</li><li>Path is relative to the directory containing the parent `FileBlock`.</li><li>"`.`" should be used to indicate the same directory as the parent `FileBlock`.</li><li>"`..`" can be used to walk up the directory tree.</li><li>Paths to nonexistent directories will be validated, but may raise errors when the parent `FileBlock` attempts to track the file.</li><li>Examples for a `FileBlock` at `/home/user/synthesis.fos`:<ul><li>"`.`" is `/home/user`</li><li>"`..`" is `/home`</li><li>"`../foo`" is `/home/foo`</li><li>"`./bar`" is `/home/user/bar`</li></ul></li></ul> |

---
### `CSVdata`

[Class Documentation][blockdocs-CSVdata]

**[Subclass of `SingleBlock`](#singleblock)**

#### Optional properties

| Property | Description | Validation Rules |
|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| rename | Maps default expected property names to custom names. Useful for when expected properties *are* present and matching descriptions, but the default name doesn't align with the niche context. (e.g., `"experimenters"` might be mapped to the more generic `"collaborators"` for computational or meta-contexted FOS files.) | <ul><li>A dictionary of key:value string pairs</li><li>Keys starting with "`_`" are ignored.</li><li>Keys must be expected property names for the block.<ul><li>For unexpected (custom) keys, renaming is not necessary.</li></ul></li><li>Values cannot be registered property names.</li></ul> |

---
### `ChemChange`

[Class Documentation][blockdocs-ChemChange]

**[Subclass of `Chemical`](#chemical)**

#### Required properties

| Property | Description | Validation Rules |
|-------------|---------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------|
| formula | Molecular composition. | <ul><li>A chemical formula recognized by the [`chemformula` package.](https://pypi.org/project/chemformula/)</li></ul> |
| amount | The sign-sensitive amount of this chemical that was added (positive) or removed (negative). | <ul><li>Positive decimal value</li></ul> |
| amount_unit | Units for comp change amount. | <ul><li>Any text entry</li></ul> |

#### Optional properties

| Property | Description | Validation Rules |
|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| rename | Maps default expected property names to custom names. Useful for when expected properties *are* present and matching descriptions, but the default name doesn't align with the niche context. (e.g., `"experimenters"` might be mapped to the more generic `"collaborators"` for computational or meta-contexted FOS files.) | <ul><li>A dictionary of key:value string pairs</li><li>Keys starting with "`_`" are ignored.</li><li>Keys must be expected property names for the block.<ul><li>For unexpected (custom) keys, renaming is not necessary.</li></ul></li><li>Values cannot be registered property names.</li></ul> |

---
### `Chemical`

[Class Documentation][blockdocs-Chemical]

**[Subclass of `SingleBlock`](#singleblock)**

#### Required properties

| Property | Description | Validation Rules |
|------------|------------------------|------------------------------------------------------------------------------------------------------------------------|
| formula | Molecular composition. | <ul><li>A chemical formula recognized by the [`chemformula` package.](https://pypi.org/project/chemformula/)</li></ul> |

#### Optional properties

| Property | Description | Validation Rules |
|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| rename | Maps default expected property names to custom names. Useful for when expected properties *are* present and matching descriptions, but the default name doesn't align with the niche context. (e.g., `"experimenters"` might be mapped to the more generic `"collaborators"` for computational or meta-contexted FOS files.) | <ul><li>A dictionary of key:value string pairs</li><li>Keys starting with "`_`" are ignored.</li><li>Keys must be expected property names for the block.<ul><li>For unexpected (custom) keys, renaming is not necessary.</li></ul></li><li>Values cannot be registered property names.</li></ul> |

---
### `CompChange`

[Class Documentation][blockdocs-CompChange]

**[Subclass of `Treatment`](#treatment)**

#### Required properties

| Property | Description | Validation Rules |
|------------|---------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------|
| type | What type of treatment was performed. | <ul><li>Any text entry</li></ul> |
| changes | A list of chemicals that were added or removed from the active reaction in this step. | <ul><li>A [simple `ListBlock`](#listblock-and-simple-lists) of [`ChemChange` objects.](#chemchange)</li></ul> |

#### Optional properties

| Property | Description | Validation Rules |
|-----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| rename | Maps default expected property names to custom names. Useful for when expected properties *are* present and matching descriptions, but the default name doesn't align with the niche context. (e.g., `"experimenters"` might be mapped to the more generic `"collaborators"` for computational or meta-contexted FOS files.) | <ul><li>A dictionary of key:value string pairs</li><li>Keys starting with "`_`" are ignored.</li><li>Keys must be expected property names for the block.<ul><li>For unexpected (custom) keys, renaming is not necessary.</li></ul></li><li>Values cannot be registered property names.</li></ul> |
| observations | General observations during the treatment | <ul><li>Any text entry</li></ul> |
| recovered_amount | How much material was recovered after treatment. | <ul><li>Positive decimal value</li><li>Requires that `recovered_amount_unit` also be present</li></ul> |
| recovered_amount_unit | Units for treatment recovered amount. | <ul><li>Validator is a subclass of [`pint`'s `Unit` class](https://pint.readthedocs.io/en/stable/) With additional rules enforcing the correct dimensionality of the unit.</li><li>Allowed dimensions:<ul><li>[mass]</li><li>[length]^3</li></ul></li></ul> |
| start_time | What time the treatment was started | <ul><li>Any text entry</li></ul> |
| end_time | What time the treatment was finished | <ul><li>Any text entry</li></ul> |

---
### `Dwell`

[Class Documentation][blockdocs-Dwell]

**[Subclass of `AnnealSection`](#annealsection)**

#### Required properties

| Property | Description | Validation Rules |
|------------|-------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| type | Examples: `"dwell", "ramp", "quench"` | <ul><li>Any text entry</li></ul> |
| time | How long the temperature was kept constant in this section. | <ul><li>Positive decimal value</li><li>Requires that `time_unit` also be present</li></ul> |
| time_unit | Units for dwell time. | <ul><li>Validator is a subclass of [`pint`'s `Unit` class](https://pint.readthedocs.io/en/stable/) With additional rules enforcing the correct dimensionality of the unit.</li><li>Allowed dimensions:<ul><li>[time]</li></ul></li></ul> |

#### Optional properties

| Property | Description | Validation Rules |
|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| rename | Maps default expected property names to custom names. Useful for when expected properties *are* present and matching descriptions, but the default name doesn't align with the niche context. (e.g., `"experimenters"` might be mapped to the more generic `"collaborators"` for computational or meta-contexted FOS files.) | <ul><li>A dictionary of key:value string pairs</li><li>Keys starting with "`_`" are ignored.</li><li>Keys must be expected property names for the block.<ul><li>For unexpected (custom) keys, renaming is not necessary.</li></ul></li><li>Values cannot be registered property names.</li></ul> |

---
### `EmbeddedFile`

[Class Documentation][blockdocs-EmbeddedFile]

**[Subclass of `Attachment`](#attachment)**

#### Required properties

| Property | Description | Validation Rules |
|------------|------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| file_name | The name of the attached file (with extension) | <ul><li>A valid filename (no path, no separators, allowed characters only).</li><li>Must include a valid extension.</li><li>Allowed characters: letters, digits, '`_`', '`-`', '`.`'</li><li>Commas are allowed, but may lead to unexpected behavior for some OS or software.</li><li>Paths to nonexistent files will be validated, but may raise errors when the parent `FileBlock` attempts to track the file.</li></ul> |

#### Optional properties

| Property | Description | Validation Rules |
|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| rename | Maps default expected property names to custom names. Useful for when expected properties *are* present and matching descriptions, but the default name doesn't align with the niche context. (e.g., `"experimenters"` might be mapped to the more generic `"collaborators"` for computational or meta-contexted FOS files.) | <ul><li>A dictionary of key:value string pairs</li><li>Keys starting with "`_`" are ignored.</li><li>Keys must be expected property names for the block.<ul><li>For unexpected (custom) keys, renaming is not necessary.</li></ul></li><li>Values cannot be registered property names.</li></ul> |
| embedded | Attachment content embedded as raw `utf-8` line strings. | <ul><li>Mutually exclusive with `path` property.</li><li>Attachment content as a list of raw `utf-8` line strings.</li></ul> |
| path | The filepath to the attached file, relative to the directory containing the parent `FileBlock`. | <ul><li>Mutually exclusive with `embedded` property.</li><li>A valid relative filepath to a directory.</li><li>Path is relative to the directory containing the parent `FileBlock`.</li><li>"`.`" should be used to indicate the same directory as the parent `FileBlock`.</li><li>"`..`" can be used to walk up the directory tree.</li><li>Paths to nonexistent directories will be validated, but may raise errors when the parent `FileBlock` attempts to track the file.</li><li>Examples for a `FileBlock` at `/home/user/synthesis.fos`:<ul><li>"`.`" is `/home/user`</li><li>"`..`" is `/home`</li><li>"`../foo`" is `/home/foo`</li><li>"`./bar`" is `/home/user/bar`</li></ul></li></ul> |

---
### `Equipment`

[Class Documentation][blockdocs-Equipment]

**[Subclass of `SingleBlock`](#singleblock)**

#### Optional properties

| Property | Description | Validation Rules |
|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| rename | Maps default expected property names to custom names. Useful for when expected properties *are* present and matching descriptions, but the default name doesn't align with the niche context. (e.g., `"experimenters"` might be mapped to the more generic `"collaborators"` for computational or meta-contexted FOS files.) | <ul><li>A dictionary of key:value string pairs</li><li>Keys starting with "`_`" are ignored.</li><li>Keys must be expected property names for the block.<ul><li>For unexpected (custom) keys, renaming is not necessary.</li></ul></li><li>Values cannot be registered property names.</li></ul> |

---
### `Experimenter`

[Class Documentation][blockdocs-Experimenter]

**[Subclass of `SingleBlock`](#singleblock)**

#### Required properties

| Property | Description | Validation Rules |
|-------------|------------------------------------|----------------------------------|
| name | Name of the experimenter | <ul><li>Any text entry</li></ul> |
| affiliation | Lab/University/Research Group/etc. | <ul><li>Any text entry</li></ul> |

#### Optional properties

| Property | Description | Validation Rules |
|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| rename | Maps default expected property names to custom names. Useful for when expected properties *are* present and matching descriptions, but the default name doesn't align with the niche context. (e.g., `"experimenters"` might be mapped to the more generic `"collaborators"` for computational or meta-contexted FOS files.) | <ul><li>A dictionary of key:value string pairs</li><li>Keys starting with "`_`" are ignored.</li><li>Keys must be expected property names for the block.<ul><li>For unexpected (custom) keys, renaming is not necessary.</li></ul></li><li>Values cannot be registered property names.</li></ul> |
| orcid | The experimenter's [ORCID](https://orcid.org/) | <ul><li>Any text entry</li></ul> |

---
### `FileBlock`

[Class Documentation][blockdocs-FileBlock]

**[Subclass of `SingleBlock`](#singleblock)**

#### Required properties

| Property | Description | Validation Rules |
|------------|-------------------------------------|-----------------------------------------------------|
| metadata | General information about the file. | <ul><li>[A `MetaData` object.](#metadata)</li></ul> |

#### Optional properties

| Property | Description | Validation Rules |
|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| rename | Maps default expected property names to custom names. Useful for when expected properties *are* present and matching descriptions, but the default name doesn't align with the niche context. (e.g., `"experimenters"` might be mapped to the more generic `"collaborators"` for computational or meta-contexted FOS files.) | <ul><li>A dictionary of key:value string pairs</li><li>Keys starting with "`_`" are ignored.</li><li>Keys must be expected property names for the block.<ul><li>For unexpected (custom) keys, renaming is not necessary.</li></ul></li><li>Values cannot be registered property names.</li></ul> |

---
### `FlexTemplate`

[Class Documentation][blockdocs-FlexTemplate]

**[Subclass of `TemplateBlock`](#templateblock)**

#### Required properties

| Property | Description | Validation Rules |
|---------------|----------------------------------|----------------------------------|
| template_name | An unique name for the template. | <ul><li>Any text entry</li></ul> |

#### Optional properties

| Property | Description | Validation Rules |
|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| rename | Maps default expected property names to custom names. Useful for when expected properties *are* present and matching descriptions, but the default name doesn't align with the niche context. (e.g., `"experimenters"` might be mapped to the more generic `"collaborators"` for computational or meta-contexted FOS files.) | <ul><li>A dictionary of key:value string pairs</li><li>Keys starting with "`_`" are ignored.</li><li>Keys must be expected property names for the block.<ul><li>For unexpected (custom) keys, renaming is not necessary.</li></ul></li><li>Values cannot be registered property names.</li></ul> |

The `FlexTemplate` class is not normally used alone to construct objects. Instead, it is used to make hybridized subclasses with other [`SingleBlock` subclasses](#singleblock), similar to the [`TemplateBlock` class](#templateblock). Unlike `TemplateBlock`s, `FlexTemplate`s dynamically determine what required properties are missing at construction time, and return a `TemplateBlock` instance with those properties marked as template fields.---
### `GasFlow`

[Class Documentation][blockdocs-GasFlow]

**[Subclass of `SingleBlock`](#singleblock)**

#### Optional properties

| Property | Description | Validation Rules |
|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| rename | Maps default expected property names to custom names. Useful for when expected properties *are* present and matching descriptions, but the default name doesn't align with the niche context. (e.g., `"experimenters"` might be mapped to the more generic `"collaborators"` for computational or meta-contexted FOS files.) | <ul><li>A dictionary of key:value string pairs</li><li>Keys starting with "`_`" are ignored.</li><li>Keys must be expected property names for the block.<ul><li>For unexpected (custom) keys, renaming is not necessary.</li></ul></li><li>Values cannot be registered property names.</li></ul> |

---
### `LabConditions`

[Class Documentation][blockdocs-LabConditions]

**[Subclass of `SingleBlock`](#singleblock)**

#### Optional properties

| Property | Description | Validation Rules |
|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| rename | Maps default expected property names to custom names. Useful for when expected properties *are* present and matching descriptions, but the default name doesn't align with the niche context. (e.g., `"experimenters"` might be mapped to the more generic `"collaborators"` for computational or meta-contexted FOS files.) | <ul><li>A dictionary of key:value string pairs</li><li>Keys starting with "`_`" are ignored.</li><li>Keys must be expected property names for the block.<ul><li>For unexpected (custom) keys, renaming is not necessary.</li></ul></li><li>Values cannot be registered property names.</li></ul> |

---
### `Material`

[Class Documentation][blockdocs-Material]

**[Subclass of `Chemical`](#chemical)**

#### Required properties

| Property | Description | Validation Rules |
|-------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------|
| name | A unique name for the material. | <ul><li>Any text entry</li></ul> |
| type | How it was used in the synthesis (e.g., reagent, flux, solvent) | <ul><li>Any text entry</li></ul> |
| formula | Molecular composition. | <ul><li>A chemical formula recognized by the [`chemformula` package.](https://pypi.org/project/chemformula/)</li></ul> |
| supplier | Source of purchase/synthesis | <ul><li>Any text entry</li></ul> |
| cas | CAS ID | <ul><li>Any text entry</li></ul> |
| form | Physical shape or state of the material **at time of acquisition** (e.g., powder, shot, wire, lump). If the material was modified after aquiring but before use in the synthesis (e.g., grinding into powder, drying, etc.), these actions should be specified in the *material's* treatments property (not the synthesis treatments). | <ul><li>Any text entry</li></ul> |
| env | What atmospheric environment the material is stored in. (e.g., ambient, Ar(g)) | <ul><li>Any text entry</li></ul> |
| amount | Amount of the material that was used. | <ul><li>Positive decimal value</li></ul> |
| amount_unit | Units for material amount. | <ul><li>Any text entry</li></ul> |

#### Optional properties

| Property | Description | Validation Rules |
|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| rename | Maps default expected property names to custom names. Useful for when expected properties *are* present and matching descriptions, but the default name doesn't align with the niche context. (e.g., `"experimenters"` might be mapped to the more generic `"collaborators"` for computational or meta-contexted FOS files.) | <ul><li>A dictionary of key:value string pairs</li><li>Keys starting with "`_`" are ignored.</li><li>Keys must be expected property names for the block.<ul><li>For unexpected (custom) keys, renaming is not necessary.</li></ul></li><li>Values cannot be registered property names.</li></ul> |
| purity | 0 < purity <= 1 | <ul><li>Decimal value within range:<ul><li>0 < val <= 1</li></ul></li></ul> |
| treatments | Treatments that were applied to the material before use in the synthesis. | <ul><li>A [simple `ListBlock`](#listblock-and-simple-lists) of [`Treatment` objects.](#treatment)</li></ul> |

---
### `MetaData`

[Class Documentation][blockdocs-MetaData]

**[Subclass of `SingleBlock`](#singleblock)**

#### Required properties

| Property | Description | Validation Rules |
|-------------|--------------------------------------------------------------------------------------------------------------------|----------------------------------|
| fos_id | A reaction ID unique within the scope of the applicable context. (e.g., a synthesis ID, template ID, etc.) | <ul><li>Any text entry</li></ul> |
| fos_type | What type of `FileBlock` subclass the file should be interpreted as. | <ul><li>Any text entry</li></ul> |
| description | A brief description of the intent for the file (characteristic methods, target products, template category, etc.). | <ul><li>Any text entry</li></ul> |

#### Optional properties

| Property | Description | Validation Rules |
|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| rename | Maps default expected property names to custom names. Useful for when expected properties *are* present and matching descriptions, but the default name doesn't align with the niche context. (e.g., `"experimenters"` might be mapped to the more generic `"collaborators"` for computational or meta-contexted FOS files.) | <ul><li>A dictionary of key:value string pairs</li><li>Keys starting with "`_`" are ignored.</li><li>Keys must be expected property names for the block.<ul><li>For unexpected (custom) keys, renaming is not necessary.</li></ul></li><li>Values cannot be registered property names.</li></ul> |

---
### `PathFile`

[Class Documentation][blockdocs-PathFile]

**[Subclass of `Attachment`](#attachment)**

#### Required properties

| Property | Description | Validation Rules |
|------------|------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| file_name | The name of the attached file (with extension) | <ul><li>A valid filename (no path, no separators, allowed characters only).</li><li>Must include a valid extension.</li><li>Allowed characters: letters, digits, '`_`', '`-`', '`.`'</li><li>Commas are allowed, but may lead to unexpected behavior for some OS or software.</li><li>Paths to nonexistent files will be validated, but may raise errors when the parent `FileBlock` attempts to track the file.</li></ul> |

#### Optional properties

| Property | Description | Validation Rules |
|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| rename | Maps default expected property names to custom names. Useful for when expected properties *are* present and matching descriptions, but the default name doesn't align with the niche context. (e.g., `"experimenters"` might be mapped to the more generic `"collaborators"` for computational or meta-contexted FOS files.) | <ul><li>A dictionary of key:value string pairs</li><li>Keys starting with "`_`" are ignored.</li><li>Keys must be expected property names for the block.<ul><li>For unexpected (custom) keys, renaming is not necessary.</li></ul></li><li>Values cannot be registered property names.</li></ul> |
| embedded | Attachment content embedded as raw `utf-8` line strings. | <ul><li>Mutually exclusive with `path` property.</li><li>Attachment content as a list of raw `utf-8` line strings.</li></ul> |
| path | The filepath to the attached file, relative to the directory containing the parent `FileBlock`. | <ul><li>Mutually exclusive with `embedded` property.</li><li>A valid relative filepath to a directory.</li><li>Path is relative to the directory containing the parent `FileBlock`.</li><li>"`.`" should be used to indicate the same directory as the parent `FileBlock`.</li><li>"`..`" can be used to walk up the directory tree.</li><li>Paths to nonexistent directories will be validated, but may raise errors when the parent `FileBlock` attempts to track the file.</li><li>Examples for a `FileBlock` at `/home/user/synthesis.fos`:<ul><li>"`.`" is `/home/user`</li><li>"`..`" is `/home`</li><li>"`../foo`" is `/home/foo`</li><li>"`./bar`" is `/home/user/bar`</li></ul></li></ul> |

---
### `Product`

[Class Documentation][blockdocs-Product]

**[Subclass of `Chemical`](#chemical)**

#### Required properties

| Property | Description | Validation Rules |
|--------------|-------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------|
| formula | Molecular composition. | <ul><li>A chemical formula recognized by the [`chemformula` package.](https://pypi.org/project/chemformula/)</li></ul> |
| name | A unique name for the product. | <ul><li>Any text entry</li></ul> |
| expected | Whether or not the product was expected from the synthesis. | <ul><li>True or False</li></ul> |
| obtained | Whether or not the product obtained from the synthesis. | <ul><li>True or False</li></ul> |
| observations | General observations about the product. | <ul><li>Any text entry</li></ul> |

#### Optional properties

| Property | Description | Validation Rules |
|----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| rename | Maps default expected property names to custom names. Useful for when expected properties *are* present and matching descriptions, but the default name doesn't align with the niche context. (e.g., `"experimenters"` might be mapped to the more generic `"collaborators"` for computational or meta-contexted FOS files.) | <ul><li>A dictionary of key:value string pairs</li><li>Keys starting with "`_`" are ignored.</li><li>Keys must be expected property names for the block.<ul><li>For unexpected (custom) keys, renaming is not necessary.</li></ul></li><li>Values cannot be registered property names.</li></ul> |
| expected_amount | How much of the product was nominally expected to be obtained from the synthesis | <ul><li>Positive decimal value</li><li>Requires that `expected_amount_unit` also be present</li></ul> |
| expected_amount_unit | Units for product expected amount. | <ul><li>Validator is a subclass of [`pint`'s `Unit` class](https://pint.readthedocs.io/en/stable/) With additional rules enforcing the correct dimensionality of the unit.</li><li>Allowed dimensions:<ul><li>[mass]</li><li>[length]^3</li></ul></li></ul> |
| obtained_amount | How much of the product was actually obtained from the synthesis.. | <ul><li>Positive decimal value</li><li>Requires that `obtained_amount_unit` also be present</li></ul> |
| obtained_amount_unit | Units for product obtained amount | <ul><li>Validator is a subclass of [`pint`'s `Unit` class](https://pint.readthedocs.io/en/stable/) With additional rules enforcing the correct dimensionality of the unit.</li><li>Allowed dimensions:<ul><li>[mass]</li><li>[length]^3</li></ul></li></ul> |
| characterizations | Description of characterization methods used to determine/quantitate the product. | <ul><li>Any text entry</li></ul> |
| structure_comments | General description of the structure of the product. | <ul><li>Any text entry</li></ul> |

---
### `Quench`

[Class Documentation][blockdocs-Quench]

**[Subclass of `AnnealSection`](#annealsection)**

#### Required properties

| Property | Description | Validation Rules |
|------------|---------------------------------------------------------------------|----------------------------------|
| type | Examples: `"dwell", "ramp", "quench"` | <ul><li>Any text entry</li></ul> |
| medium | What medium the reaction vessel was quenched in (e.g., water, air). | <ul><li>Any text entry</li></ul> |

#### Optional properties

| Property | Description | Validation Rules |
|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| rename | Maps default expected property names to custom names. Useful for when expected properties *are* present and matching descriptions, but the default name doesn't align with the niche context. (e.g., `"experimenters"` might be mapped to the more generic `"collaborators"` for computational or meta-contexted FOS files.) | <ul><li>A dictionary of key:value string pairs</li><li>Keys starting with "`_`" are ignored.</li><li>Keys must be expected property names for the block.<ul><li>For unexpected (custom) keys, renaming is not necessary.</li></ul></li><li>Values cannot be registered property names.</li></ul> |

---
### `Ramp`

[Class Documentation][blockdocs-Ramp]

**[Subclass of `AnnealSection`](#annealsection)**

#### Required properties

During construction of a `Ramp` object, it is required to have at least 2 of the following optional properties, with their respective units:

- `temp`
- `time`
- `rate`

If all three are provided, the last one found during reading will be discarded as redundant data, and the object is [dispatched](#dispatching-subclasses) to a `Ramp` subclass with a "retrieval" method for calculating the missing property (e.g., `get_temp()`, `get_time()`, or `get_rate()`) When working with `Ramp` objects in the FoSpy framework, it is best practice to always use the "retrieval" methods. For subclasses that *do* have the desired property, retrieval methods default to returning it directly.

| Property | Description | Validation Rules |
|------------|---------------------------------------|----------------------------------|
| type | Examples: `"dwell", "ramp", "quench"` | <ul><li>Any text entry</li></ul> |

#### Optional properties

| Property | Description | Validation Rules |
|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| rename | Maps default expected property names to custom names. Useful for when expected properties *are* present and matching descriptions, but the default name doesn't align with the niche context. (e.g., `"experimenters"` might be mapped to the more generic `"collaborators"` for computational or meta-contexted FOS files.) | <ul><li>A dictionary of key:value string pairs</li><li>Keys starting with "`_`" are ignored.</li><li>Keys must be expected property names for the block.<ul><li>For unexpected (custom) keys, renaming is not necessary.</li></ul></li><li>Values cannot be registered property names.</li></ul> |
| temp | The next temperature in the program. | <ul><li>Positive decimal value</li><li>Requires that `temp_unit` also be present</li></ul> |
| time | Length of time from the previous temperature to the new temperature. | <ul><li>Positive decimal value</li><li>Requires that `time_unit` also be present</li></ul> |
| rate | The sign-sensitive rate at which temperature was changed to get to the new temperature. (Increase -> positive, Decrease -> negative). | <ul><li>Any decimal value (positive or negative)</li><li>Requires that `rate_unit` also be present</li></ul> |
| temp_unit | Units for ramp temperature. | <ul><li>Validator is a subclass of [`pint`'s `Unit` class](https://pint.readthedocs.io/en/stable/) With more flexibility for recognizing temperature units.</li><li>Must be a recognizable unit for temperature.</li></ul> |
| time_unit | Units for ramp time. | <ul><li>Validator is a subclass of [`pint`'s `Unit` class](https://pint.readthedocs.io/en/stable/) With additional rules enforcing the correct dimensionality of the unit.</li><li>Allowed dimensions:<ul><li>[time]</li></ul></li></ul> |
| rate_unit | Units for ramp rate. | <ul><li>Validator is a subclass of [`pint`'s `Unit` class](https://pint.readthedocs.io/en/stable/) with more flexibility for recognizing temperature units.</li><li>Must be a recognizable unit for temperature *over time*.</li></ul> |

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
|------------|---------------------------------------|----------------------------------|
| type | Examples: `"dwell", "ramp", "quench"` | <ul><li>Any text entry</li></ul> |

#### Optional properties

| Property | Description | Validation Rules |
|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| rename | Maps default expected property names to custom names. Useful for when expected properties *are* present and matching descriptions, but the default name doesn't align with the niche context. (e.g., `"experimenters"` might be mapped to the more generic `"collaborators"` for computational or meta-contexted FOS files.) | <ul><li>A dictionary of key:value string pairs</li><li>Keys starting with "`_`" are ignored.</li><li>Keys must be expected property names for the block.<ul><li>For unexpected (custom) keys, renaming is not necessary.</li></ul></li><li>Values cannot be registered property names.</li></ul> |
| temp | The next temperature in the program. | <ul><li>Positive decimal value</li><li>Requires that `temp_unit` also be present</li></ul> |
| time | Length of time from the previous temperature to the new temperature. | <ul><li>Positive decimal value</li><li>Requires that `time_unit` also be present</li></ul> |
| rate | The sign-sensitive rate at which temperature was changed to get to the new temperature. (Increase -> positive, Decrease -> negative). | <ul><li>Any decimal value (positive or negative)</li><li>Requires that `rate_unit` also be present</li></ul> |
| temp_unit | Units for ramp temperature. | <ul><li>Validator is a subclass of [`pint`'s `Unit` class](https://pint.readthedocs.io/en/stable/) With more flexibility for recognizing temperature units.</li><li>Must be a recognizable unit for temperature.</li></ul> |
| time_unit | Units for ramp time. | <ul><li>Validator is a subclass of [`pint`'s `Unit` class](https://pint.readthedocs.io/en/stable/) With additional rules enforcing the correct dimensionality of the unit.</li><li>Allowed dimensions:<ul><li>[time]</li></ul></li></ul> |
| rate_unit | Units for ramp rate. | <ul><li>Validator is a subclass of [`pint`'s `Unit` class](https://pint.readthedocs.io/en/stable/) with more flexibility for recognizing temperature units.</li><li>Must be a recognizable unit for temperature *over time*.</li></ul> |

---
### `RampNoTemp`

[Class Documentation][blockdocs-RampNoTemp]

**[Subclass of `Ramp`](#ramp)**

#### Required properties

| Property | Description | Validation Rules |
|------------|---------------------------------------|----------------------------------|
| type | Examples: `"dwell", "ramp", "quench"` | <ul><li>Any text entry</li></ul> |

#### Optional properties

| Property | Description | Validation Rules |
|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| rename | Maps default expected property names to custom names. Useful for when expected properties *are* present and matching descriptions, but the default name doesn't align with the niche context. (e.g., `"experimenters"` might be mapped to the more generic `"collaborators"` for computational or meta-contexted FOS files.) | <ul><li>A dictionary of key:value string pairs</li><li>Keys starting with "`_`" are ignored.</li><li>Keys must be expected property names for the block.<ul><li>For unexpected (custom) keys, renaming is not necessary.</li></ul></li><li>Values cannot be registered property names.</li></ul> |
| temp | The next temperature in the program. | <ul><li>Positive decimal value</li><li>Requires that `temp_unit` also be present</li></ul> |
| time | Length of time from the previous temperature to the new temperature. | <ul><li>Positive decimal value</li><li>Requires that `time_unit` also be present</li></ul> |
| rate | The sign-sensitive rate at which temperature was changed to get to the new temperature. (Increase -> positive, Decrease -> negative). | <ul><li>Any decimal value (positive or negative)</li><li>Requires that `rate_unit` also be present</li></ul> |
| temp_unit | Units for ramp temperature. | <ul><li>Validator is a subclass of [`pint`'s `Unit` class](https://pint.readthedocs.io/en/stable/) With more flexibility for recognizing temperature units.</li><li>Must be a recognizable unit for temperature.</li></ul> |
| time_unit | Units for ramp time. | <ul><li>Validator is a subclass of [`pint`'s `Unit` class](https://pint.readthedocs.io/en/stable/) With additional rules enforcing the correct dimensionality of the unit.</li><li>Allowed dimensions:<ul><li>[time]</li></ul></li></ul> |
| rate_unit | Units for ramp rate. | <ul><li>Validator is a subclass of [`pint`'s `Unit` class](https://pint.readthedocs.io/en/stable/) with more flexibility for recognizing temperature units.</li><li>Must be a recognizable unit for temperature *over time*.</li></ul> |

---
### `RampNoTime`

[Class Documentation][blockdocs-RampNoTime]

**[Subclass of `Ramp`](#ramp)**

#### Required properties

| Property | Description | Validation Rules |
|------------|---------------------------------------|----------------------------------|
| type | Examples: `"dwell", "ramp", "quench"` | <ul><li>Any text entry</li></ul> |

#### Optional properties

| Property | Description | Validation Rules |
|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| rename | Maps default expected property names to custom names. Useful for when expected properties *are* present and matching descriptions, but the default name doesn't align with the niche context. (e.g., `"experimenters"` might be mapped to the more generic `"collaborators"` for computational or meta-contexted FOS files.) | <ul><li>A dictionary of key:value string pairs</li><li>Keys starting with "`_`" are ignored.</li><li>Keys must be expected property names for the block.<ul><li>For unexpected (custom) keys, renaming is not necessary.</li></ul></li><li>Values cannot be registered property names.</li></ul> |
| temp | The next temperature in the program. | <ul><li>Positive decimal value</li><li>Requires that `temp_unit` also be present</li></ul> |
| time | Length of time from the previous temperature to the new temperature. | <ul><li>Positive decimal value</li><li>Requires that `time_unit` also be present</li></ul> |
| rate | The sign-sensitive rate at which temperature was changed to get to the new temperature. (Increase -> positive, Decrease -> negative). | <ul><li>Any decimal value (positive or negative)</li><li>Requires that `rate_unit` also be present</li></ul> |
| temp_unit | Units for ramp temperature. | <ul><li>Validator is a subclass of [`pint`'s `Unit` class](https://pint.readthedocs.io/en/stable/) With more flexibility for recognizing temperature units.</li><li>Must be a recognizable unit for temperature.</li></ul> |
| time_unit | Units for ramp time. | <ul><li>Validator is a subclass of [`pint`'s `Unit` class](https://pint.readthedocs.io/en/stable/) With additional rules enforcing the correct dimensionality of the unit.</li><li>Allowed dimensions:<ul><li>[time]</li></ul></li></ul> |
| rate_unit | Units for ramp rate. | <ul><li>Validator is a subclass of [`pint`'s `Unit` class](https://pint.readthedocs.io/en/stable/) with more flexibility for recognizing temperature units.</li><li>Must be a recognizable unit for temperature *over time*.</li></ul> |

---
### `Reaction`

[Class Documentation][blockdocs-Reaction]

**[Subclass of `SingleBlock`](#singleblock)**

#### Required properties

| Property | Description | Validation Rules |
|---------------------|----------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| nominal_formula | Total expected chemical composition from all final products. | <ul><li>A chemical formula recognized by the [`chemformula` package.](https://pypi.org/project/chemformula/)</li></ul> |
| nominal_amount | Total amount expected to be recovered from all final products. | <ul><li>Positive decimal value</li></ul> |
| nominal_amount_unit | Units for reaction nominal amount. | <ul><li>Validator is a subclass of [`pint`'s `Unit` class](https://pint.readthedocs.io/en/stable/) With additional rules enforcing the correct dimensionality of the unit.</li><li>Allowed dimensions:<ul><li>[mass]</li><li>[length]^3</li></ul></li></ul> |

#### Optional properties

| Property | Description | Validation Rules |
|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| rename | Maps default expected property names to custom names. Useful for when expected properties *are* present and matching descriptions, but the default name doesn't align with the niche context. (e.g., `"experimenters"` might be mapped to the more generic `"collaborators"` for computational or meta-contexted FOS files.) | <ul><li>A dictionary of key:value string pairs</li><li>Keys starting with "`_`" are ignored.</li><li>Keys must be expected property names for the block.<ul><li>For unexpected (custom) keys, renaming is not necessary.</li></ul></li><li>Values cannot be registered property names.</li></ul> |

---
### `SingleBlock`

[Class Documentation][blockdocs-SingleBlock]

**[Subclass of `Block`][blockdocs-Block]**

#### Optional properties

| Property | Description | Validation Rules |
|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| rename | Maps default expected property names to custom names. Useful for when expected properties *are* present and matching descriptions, but the default name doesn't align with the niche context. (e.g., `"experimenters"` might be mapped to the more generic `"collaborators"` for computational or meta-contexted FOS files.) | <ul><li>A dictionary of key:value string pairs</li><li>Keys starting with "`_`" are ignored.</li><li>Keys must be expected property names for the block.<ul><li>For unexpected (custom) keys, renaming is not necessary.</li></ul></li><li>Values cannot be registered property names.</li></ul> |

`SingleBlock` is the parent class of all block classes representing a single entity. `SingleBlock`s are rarely constructed without subclassing, but may be used if you want to take advantage of the rigorous attribute assignment and methods that all other block classes inherit, without defining any expected properties.---
### `Synthesis`

[Class Documentation][blockdocs-Synthesis]

**[Subclass of `FileBlock`](#fileblock)**

#### Required properties

| Property | Description | Validation Rules |
|---------------|----------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|
| metadata | General information about the file. | <ul><li>[A `SynthesisMeta` object.](#synthesismeta)</li></ul> |
| experimenters | Experimenters who participated in any treatments described in the synthesis. | <ul><li>A [simple `ListBlock`](#listblock-and-simple-lists) of [`Experimenter` objects.](#experimenter)</li></ul> |
| reaction | General information applying to the entire synthetic reaction. | <ul><li>[A `Reaction` object.](#reaction)</li></ul> |
| products | Products expected or obtained from the synthesis. | <ul><li>A [simple `ListBlock`](#listblock-and-simple-lists) of [`Product` objects.](#product)</li></ul> |
| materials | Starting chemicals and materials used in the synthesis. | <ul><li>A [specialized `ListBlock`][blockdocs-MaterialList] of [`Material` objects.](#material)</li></ul> |
| treatments | Sequence of individual actions performed on the materials or active reaction to carry out the synthesis. | <ul><li>A [simple `ListBlock`](#listblock-and-simple-lists) of [`Treatment` objects.](#treatment)</li></ul> |

#### Optional properties

| Property | Description | Validation Rules |
|-----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| rename | Maps default expected property names to custom names. Useful for when expected properties *are* present and matching descriptions, but the default name doesn't align with the niche context. (e.g., `"experimenters"` might be mapped to the more generic `"collaborators"` for computational or meta-contexted FOS files.) | <ul><li>A dictionary of key:value string pairs</li><li>Keys starting with "`_`" are ignored.</li><li>Keys must be expected property names for the block.<ul><li>For unexpected (custom) keys, renaming is not necessary.</li></ul></li><li>Values cannot be registered property names.</li></ul> |
| cif | A single attached CIF file applicable to the entire synthesis. | <ul><li>[A `CIFFile` object.](#ciffile)</li></ul><ul></ul> |
| cifs | Multiple attached CIF files applicable to the entire synthesis. | <ul><li>A [simple `ListBlock`](#listblock-and-simple-lists) of [`EnforcedAttachment` objects.](#attachment)</li></ul> |
| laboratory_conditions | General conditions of the laboratory during the synthesis. | <ul><li>[A `LabConditions` object.](#labconditions)</li></ul> |
| equipment | Specialized equipment or apparatuses used during the synthesis. | <ul><li>A [simple `ListBlock`](#listblock-and-simple-lists) of [`Equipment` objects.](#equipment)</li></ul> |

---
### `SynthesisMeta`

[Class Documentation][blockdocs-SynthesisMeta]

**[Subclass of `MetaData`](#metadata)**

#### Required properties

| Property | Description | Validation Rules |
|-------------|--------------------------------------------------------------------------------------------------------------------|----------------------------------|
| fos_id | A reaction ID unique within the scope of the applicable context. (e.g., a synthesis ID, template ID, etc.) | <ul><li>Any text entry</li></ul> |
| fos_type | What type of `FileBlock` subclass the file should be interpreted as. | <ul><li>Any text entry</li></ul> |
| description | A brief description of the intent for the file (characteristic methods, target products, template category, etc.). | <ul><li>Any text entry</li></ul> |
| group_id | The unique identifier for the generating research group or organization. | <ul><li>Any text entry</li></ul> |
| project_id | Describes the context or purpose of the synthesis within the scope of the `group_id` and/or lead experimenter. | <ul><li>Any text entry</li></ul> |

#### Optional properties

| Property | Description | Validation Rules |
|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| rename | Maps default expected property names to custom names. Useful for when expected properties *are* present and matching descriptions, but the default name doesn't align with the niche context. (e.g., `"experimenters"` might be mapped to the more generic `"collaborators"` for computational or meta-contexted FOS files.) | <ul><li>A dictionary of key:value string pairs</li><li>Keys starting with "`_`" are ignored.</li><li>Keys must be expected property names for the block.<ul><li>For unexpected (custom) keys, renaming is not necessary.</li></ul></li><li>Values cannot be registered property names.</li></ul> |

---
### `TemplateBlock`

[Class Documentation][blockdocs-TemplateBlock]

**[Subclass of `SingleBlock`](#singleblock)**

#### Required properties

| Property | Description | Validation Rules |
|---------------|----------------------------------|----------------------------------|
| template_name | An unique name for the template. | <ul><li>Any text entry</li></ul> |

#### Optional properties

| Property | Description | Validation Rules |
|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| rename | Maps default expected property names to custom names. Useful for when expected properties *are* present and matching descriptions, but the default name doesn't align with the niche context. (e.g., `"experimenters"` might be mapped to the more generic `"collaborators"` for computational or meta-contexted FOS files.) | <ul><li>A dictionary of key:value string pairs</li><li>Keys starting with "`_`" are ignored.</li><li>Keys must be expected property names for the block.<ul><li>For unexpected (custom) keys, renaming is not necessary.</li></ul></li><li>Values cannot be registered property names.</li></ul> |

The `TemplateBlock` class is not normally used alone to construct objects. Instead, it is used to make hybridized subclasses of other `SingleBlock` subclasses. Template subclasses override required properties of the original class with template fields that can be later filled in and passed to their validators with the `fill()` method. Refer to the [code example walkthrough](../examples/code_example/index.md) for some uses of templates.

Instances of the base `TemplateBlock` class are usually constructed by calling the [`TemplateClass` class method](../blocks/blocks.md#FoSpy.blocks.blocks.SingleBlock.TemplateClass) on an existing block. To construct a a `TemplateBlock` from an incomplete property dictionary, it is recommended to use [`FlexTemplate` instead.](#flextemplate)---
### `TemplateSet`

[Class Documentation][blockdocs-TemplateSet]

**[Subclass of `FileBlock`](#fileblock)**

#### Required properties

| Property | Description | Validation Rules |
|------------|-------------------------------------|-----------------------------------------------------|
| metadata | General information about the file. | <ul><li>[A `MetaData` object.](#metadata)</li></ul> |

#### Optional properties

| Property | Description | Validation Rules |
|-----------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| rename | Maps default expected property names to custom names. Useful for when expected properties *are* present and matching descriptions, but the default name doesn't align with the niche context. (e.g., `"experimenters"` might be mapped to the more generic `"collaborators"` for computational or meta-contexted FOS files.) | <ul><li>A dictionary of key:value string pairs</li><li>Keys starting with "`_`" are ignored.</li><li>Keys must be expected property names for the block.<ul><li>For unexpected (custom) keys, renaming is not necessary.</li></ul></li><li>Values cannot be registered property names.</li></ul> |
| experimenters | A list of incomplete templates describing experimenters. | <ul><li>A [simple `ListBlock`](#listblock-and-simple-lists) of flexible [`Experimenter` *templates.*](#experimenter)<ul><li>[`FlexTemplate` subclasses](#flextemplate) are defined with a parent [`SingleBlock` subclass](#singleblock). They automatically detect which required properties are missing at construction time, and instantiate a [dynamic `TemplateBlock`](#templateblock) with template fields in those properties.</li></ul></li></ul> |
| materials | A list of incomplete templates describing materials. | <ul><li>A [simple `ListBlock`](#listblock-and-simple-lists) of flexible [`Material` *templates.*](#material)<ul><li>[`FlexTemplate` subclasses](#flextemplate) are defined with a parent [`SingleBlock` subclass](#singleblock). They automatically detect which required properties are missing at construction time, and instantiate a [dynamic `TemplateBlock`](#templateblock) with template fields in those properties.</li></ul></li></ul> |
| treatments | A list of incomplete templates describing treatments. | <ul><li>A [simple `ListBlock`](#listblock-and-simple-lists) of flexible [`Treatment` *templates.*](#treatment)<ul><li>[`FlexTemplate` subclasses](#flextemplate) are defined with a parent [`SingleBlock` subclass](#singleblock). They automatically detect which required properties are missing at construction time, and instantiate a [dynamic `TemplateBlock`](#templateblock) with template fields in those properties.</li></ul></li></ul> |
| annealings | A list of incomplete templates describing annealing treatments. | <ul><li>A [simple `ListBlock`](#listblock-and-simple-lists) of flexible [`Annealing` *templates.*](#annealing)<ul><li>[`FlexTemplate` subclasses](#flextemplate) are defined with a parent [`SingleBlock` subclass](#singleblock). They automatically detect which required properties are missing at construction time, and instantiate a [dynamic `TemplateBlock`](#templateblock) with template fields in those properties.</li></ul></li></ul> |
| anneal_sections | A list of incomplete templates describing annealing sections. | <ul><li>A [simple `ListBlock`](#listblock-and-simple-lists) of flexible [`AnnealSection` *templates.*](#annealsection)<ul><li>[`FlexTemplate` subclasses](#flextemplate) are defined with a parent [`SingleBlock` subclass](#singleblock). They automatically detect which required properties are missing at construction time, and instantiate a [dynamic `TemplateBlock`](#templateblock) with template fields in those properties.</li></ul></li></ul> |
| cifs | A list of CIF files attached to the template set. | <ul><li>A [simple `ListBlock`](#listblock-and-simple-lists) of [`EnforcedAttachment` objects.](#attachment)</li></ul> |

In contrast with a `Synthesis` file, most top-level properties for a `TemplateSet` are expected to contain [lists of templates](#templatelists) of a given type. The [`TemplateList.Simple()` class method](../blocks/template.md#FoSpy.blocks.template.TemplateList.Simple) dynamically determines template fields using the [`FlexTemplate` subclass](#flextemplate)

Developers are currently working on ways to flexibly allow any template list in a `TemplateSet`. For now, refer to [modifying validation at runtime](#modifying-property-validation-at-runtime) or reach out to developers if current standards are limiting how you want to use templates.---
### `TraceData`

[Class Documentation][blockdocs-TraceData]

**[Subclass of `SingleBlock`](#singleblock)**

#### Optional properties

| Property | Description | Validation Rules |
|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| rename | Maps default expected property names to custom names. Useful for when expected properties *are* present and matching descriptions, but the default name doesn't align with the niche context. (e.g., `"experimenters"` might be mapped to the more generic `"collaborators"` for computational or meta-contexted FOS files.) | <ul><li>A dictionary of key:value string pairs</li><li>Keys starting with "`_`" are ignored.</li><li>Keys must be expected property names for the block.<ul><li>For unexpected (custom) keys, renaming is not necessary.</li></ul></li><li>Values cannot be registered property names.</li></ul> |

---
### `Treatment`

[Class Documentation][blockdocs-Treatment]

**[Subclass of `SingleBlock`](#singleblock)**

#### Required properties

| Property | Description | Validation Rules |
|------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------|
| type | What type of treatment was performed. | <ul><li>Any text entry</li></ul> |
| repeats | How many times the treatment was performed in succession *uninterrupted*. If other treatments are performed between repeats, add a different treatment block after the interrupting treatments. | <ul><li>Any integer (positive or negative)</li></ul> |

#### Optional properties

| Property | Description | Validation Rules |
|-----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| rename | Maps default expected property names to custom names. Useful for when expected properties *are* present and matching descriptions, but the default name doesn't align with the niche context. (e.g., `"experimenters"` might be mapped to the more generic `"collaborators"` for computational or meta-contexted FOS files.) | <ul><li>A dictionary of key:value string pairs</li><li>Keys starting with "`_`" are ignored.</li><li>Keys must be expected property names for the block.<ul><li>For unexpected (custom) keys, renaming is not necessary.</li></ul></li><li>Values cannot be registered property names.</li></ul> |
| observations | General observations during the treatment | <ul><li>Any text entry</li></ul> |
| recovered_amount | How much material was recovered after treatment. | <ul><li>Positive decimal value</li><li>Requires that `recovered_amount_unit` also be present</li></ul> |
| recovered_amount_unit | Units for treatment recovered amount. | <ul><li>Validator is a subclass of [`pint`'s `Unit` class](https://pint.readthedocs.io/en/stable/) With additional rules enforcing the correct dimensionality of the unit.</li><li>Allowed dimensions:<ul><li>[mass]</li><li>[length]^3</li></ul></li></ul> |
| start_time | What time the treatment was started | <ul><li>Any text entry</li></ul> |
| end_time | What time the treatment was finished | <ul><li>Any text entry</li></ul> |

---

````
