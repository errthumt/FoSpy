The `TemplateBlock` class is not normally used alone to construct objects. Instead, it is used to make hybridized subclasses of other `SingleBlock` subclasses. Template subclasses override required properties of the original class with template fields that can be later filled in and passed to their validators with the `fill()` method. Refer to the [code example walkthrough](../examples/code_example/index.md) for some uses of templates.

Instances of the base `TemplateBlock` class are usually constructed by calling the [`TemplateClass` class method](../blocks/blocks.md#FoSpy.blocks.blocks.SingleBlock.TemplateClass) on an existing block, but some template classes can dynamically determine which fields are missing and redirect to the appropriate template class.


#### Required properties

<prop_table>

#### Optional properties

<prop_table>