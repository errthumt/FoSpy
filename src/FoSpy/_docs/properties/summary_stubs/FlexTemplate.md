The `FlexTemplate` class is not normally used alone to construct objects. Instead, it is used to make hybridized subclasses with other [`SingleBlock` subclasses](#singleblock), similar to the [`TemplateBlock` class](#templateblock). Unlike `TemplateBlock`s, `FlexTemplate`s dynamically determine what required properties are missing at construction time, and return a `TemplateBlock` instance with those properties marked as template fields.



#### Required properties

<prop_table>

#### Optional properties

<prop_table>