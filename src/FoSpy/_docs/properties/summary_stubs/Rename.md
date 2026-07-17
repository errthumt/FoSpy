Any [`SingleBlock` object](#singleblock) can have `rename` as one of its properties, which contains an instance of a `Rename` block. These can be used to alter the expected (required *or* optional) property names to custom names instead. This is useful for when expected properties *are* present and matching descriptions, but the default name doesn't align with the niche context. (e.g., `\"experimenters\"` might be mapped to the more generic `\"collaborators\"` for computational or meta-contexted FOS files.)

`Rename` blocks are available as a "stop-gap" for scientists who are trying to make use of the FoS format, but whose areas of expertise are significantly deviated from the context FoS was designed for. Renaming is not intended as a long-term solution.

- **If the descriptions/validation routines for the renamed property are still appropriate, but the property name itself is inaccurate:** Consider reaching out to developers about altering the FoS standards to better reflect the growing community.
- **If you are working with a very niche application that requires fundamental alteration of the FoS standards:** Consider [modifying validation at runtime](#modifying-property-validation-at-runtime) or creating a fork of the [GitHub](https://github.com/errthumt/FoSpy) to make changes to the sourcecode.

Note that renaming a property will keep all relevant validation rules attached to the new custom name (e.g., for the aforementioned example, the same rules that apply to the `\"experimenters\"` property now apply to the new `\"collaborators\"` property instead.). This allows researchers to make modifications for *clarity purposes only*, without bypassing any FoS standards.

#### Required properties

<prop_table>