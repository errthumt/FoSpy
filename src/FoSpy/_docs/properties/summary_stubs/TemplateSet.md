#### Optional properties

In contrast with a `Synthesis` file, most top-level properties for a `TemplateSet` are expected to contain [lists of templates](#templatelists) of a given type. `TemplateList.Simple()` allows entries to be incomplete and generates hybridized `TemplateBlock` subclasses for them.

Developers are currently working on ways to flexibly allow any template list in a `TemplateSet`. For now, refer to [modifying validation at runtime](#modifying-property-validation-at-runtime) or reach out to developers if current standards are limiting how you want to use templates.

<prop_table>