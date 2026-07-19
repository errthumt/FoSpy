In contrast with a `Synthesis` file, most top-level properties for a `TemplateSet` are expected to contain [lists of templates](#templatelists) of a given type. The [`TemplateList.Simple()` class method](../blocks/template.md#FoSpy.blocks.template.TemplateList.Simple) dynamically determines template fields using the [`FlexTemplate` subclass](#flextemplate)

`TemplateSets` do not have many expected properties by default, but you can add a list of templates for any block to a `TemplateSet` using an *alias*. Aliases are ways of signaling to a block that you are creating an unexpected property, but you want it to be a certain block type anyway. You do this by adding "`$`", followed by the name of the block type in all lowercase, to the end of the property name.

For example:

```FOS
[[Experimenters]]
name: Travis Errthum
affiliation: Kovnir Group - Iowa State University
orcid: 0009-0006-1937-5672
colleague$experimenter: [
    name: Joseph Race
    affiliation: Graham's Dad
    orcid: 0000-0002-8551-3627
]
```

Here, the experimenter has the normal expected properties, but it also has an unexpected property, `colleague`, aliased with `experimenter`. This signals that the contents should be interpreted as an experimenter.

Unlike most blocks, for `TemplateSet`s, all top-level property aliases are intepreted to mean a list of items, not just a single item. So if I add this to my templates file:

```FOS
[[experimenter_templates$experimenter]]
name: Travis Errthum
affiliation: Kovnir Group - Iowa State University
-orcid: <!TEMPLATE-FIELD>

name: Joseph Race
-affiliation: <!TEMPLATE-FIELD>
orcid: 0000-0002-8551-3627
```

The experimenters property will be correctly interpreted as a list of [`Experimenter` objects](#experimenter). Putting the same block (with filled templates) into a [`Synthesis` file](#synthesis) would result in an error, because syntheses expect the `$experimenter` alias to mean only one experimenter (use `$experimenterlist` to contain multiple).


#### Required properties

<prop_table>

#### Optional properties

<prop_table>