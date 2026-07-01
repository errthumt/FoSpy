`TemplateBlock` is used to make hybridized subclasses of other `SingleBlock` subclasses. Template subclasses override required properties of the original class with template fields that can be later filled in and passed to their validators with the `fill()` method. Refer to the [code example walkthrough](../examples/code_example/index.md) for some uses of templates.


#### TemplateBlock Method Subclasses

These subclasses don't currently have any additional required properties but will either be expanded in the future or have specialized methods.

- `FlexTemplate`: Same functionality as `TemplateBlock`, but automatically interprets missing input as template fields rather than having preset expectations for which fields are unfilled. Used for [`reflex()`](../blocks/blocks.md#FoSpy.blocks.blocks.SingleBlock.reflex) method and [`TemplateList`](../blocks/template.md#FoSpy.blocks.template.TemplateList) construction.