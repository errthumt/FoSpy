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