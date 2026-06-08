# What is a `Block`?
In `FoSpy`, a `Block` is a Python subclass object representing a section of information read from the FOS format. Blocks can be read at the top level from each section underneath a `[Heading]` or `[[Heading]]` in a FOS:

```fos
[Block_name]
property1: foo
property2: bar
```

Or, they can be nested inside another block as one of its properties:

```fos
[Block_name]
property1: hello world!
blockproperty: [
    foo: bar
]
```

There are two primary types of `Block` types: [`SingleBlock`][FoSpy.blocks.blocks.SingleBlock] and [`ListBlock`][FoSpy.blocks.blocks.ListBlock]. When a FOS-formatted file is read, it's parsed as a single dictionary of nested list/dict structures. Each "sub" dictionary within this structure is constructed into a `SingleBlock` object, whereas each list of constructed objects is constructed into a parent `ListBlock` object.

* `ListBlock` subclasses are primarily used for enforcing that all the blocks within the list are the same `SingleBlock` subclass (e.g., `Materials` or `Treatments`), but may also have special methods for working with multiple items within that list at once, such as finding the weight percent of each material.
* `SingleBlock` subclasses are used for enforcing the expected properties for a given set of data. `Synthesis`, for example, is a `SingleBlock` subclass that is required to have certain properties, like a `Reaction` block and a `Materials` list. It also has optional properties, which are not required but are expected to be of a certain type. The `[CIFs]` heading in a FOS, for instance, is expected to be a list of `EmbeddedCIF` objects.

When a `SingleBlock` is constructed from a dictionary, each key in the dictionary is set as one of its attributes. [Some attribute names have specific requirements](../expected/index.md) unique to that subclass, which are enforced during construction. Because attributes are assigned at construction, you will not find complete documentation in a subclass's sourcecode of all it's available attributes. Instead, you must refer to the dictionaries at [parsing.validation][FoSpy.parsing.validation.required_keys] or the associated [documentation page](../expected/index.md).

Docstring documentation for public methods of each `Block` subclass can be found in the adjacent pages. All docstrings (private and public) can be found in the [full documentation](../full/index.md).