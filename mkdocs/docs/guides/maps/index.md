# Mapping other ELN structures to FOS format using `FoSpy.json`

Many labs already have an established internal format for electronic laboratory notebook (ELN) entries. These formats might already convey experimental methods and results in a serialized, machine-readable format, but don't follow the unified standards set forth by the `FoSpy` project. As the project grows, the developers expect to pre-package tools for converting the most commonly used or standardized formats. However, this will not help smaller or more niche labs that might have their own standards for what to include in an ELN entry.

To address this, `FoSpy` comes with a built-in module that establishes a workflow for automating the conversion of any serialized dictionary format into the FOS format. Generally, the conversion is done in three steps:

1. [**Generate a configuration file unique to your ELN structure.**](#configuration-writing-your-own-map) This configuration file attaches an instruction to each field in *your* format about where it should go in the *FOS* format. If done correctly, this only needs to be done once for an entire set of ELN entries with the same structure.
    - `FoSpy` developers have achieved promising *(preliminary)* results in training large language models (LLMs) to generate this configuration. Keep an eye out for new features taking advantage of this, or consider training your own LLM with inputs like [the expected properties page](../../expected/index.md) or [the code example](../../examples/code_example/index.md). Example FOS files can also be found in the code example page.
2. **Convert each ELN entry into a Python dictionary matching the FOS structure.** In its simplest form, a FoS is an arbitrarily nested dictionary/list structure. Once your configuration is set, all of your ELNs can be converted to this structure automatically
3. **Run the converted dictionary through the validation routines.** By attempting to generate a [`Synthesis` object](../../expected/index.md#synthesis) from the converted dictionary, validation is automatically run to check if all required fields are present and filled in correctly.
---

## Before Starting: Convert your ELN to JSON
stub

## Configuration: Writing Your Own Map

### FOS/JSON Dictionary Example

Since the FoS format is a nested dictionary/list structure, each value in a synthesis file can be uniquely identified by its property name and the path through all of its parents. Here's a simple example:

<table>
<tr><td>FoS Syntax</td><td>JSON Syntax</td></tr>
<tr>
<td>

```FOS
// Excerpted from a FOS synthesis file
[[Experimenters]]
name: Travis Errthum
isu_research_group: Kovnir Group - Iowa State University
orcid: 0009-0006-1937-5672

name: Joseph Race
affiliation: Kovnir Group - Iowa State University
orcid: 0000-0002-8551-3627
```

</td>
<td>

```JSON
// Excerpted from a JSON synthesis file
{
    "metadata": {...},
    "experimenters": [
        {
            "name": "Travis Errthum",
            "affiliation": "Kovnir Group - Iowa State University",
            "orcid": "0009-0006-1937-5672"
        },
        {
            "name": "Joseph Race",
            "affiliation": "Kovnir Group - Iowa State University",
            "orcid": "0000-0002-8551-3627"
        }
    ],
    "products": [...],
    ...
}
```

</td>
</tr>
</table>

- In the JSON-formatted version, `"experimenters"` contains a list (denoted by `[]` brackets) of dictionaries (denoted by `{}` brackets) where each dictionary represents one experimenter. Each experimenter has three `"property":"value"` pairs.
- In the FOS format, the line `name: Travis Errthum` identfies the `"name"` property of the first item in the `"experimenters"` list. This can be abbreviated as `"experimenters[0].name" : "Travis Errthum"`
  - Note that in Python, list indices are 0-based. So `[0]` refers to the first item in the list, `[1]` refers to the second, and so on.
  - This abbreviation format is used for writing the configuration map.

### Map Guides

To give users a summary of all the available fields in the FoS format their abbreviations will be, JSON guide files have been generated to mirror the FOS structure, but all values have been replaced with their abbreviated name. These files give a nice top-level guide for required and optional properties, but the full [expected properties](../../expected/index.md) page can be consulted for more information on the meaning of each property

- **Please Note:**
  - For properties (like `"experimenters"`) expecting a list of items, the guide files provide two items in the list (`[0]` and `[1]`) as an example. For validation, these lists can have as little or as many items as needed.
  - If you are using the [developers testing suite](../../internal/dev_env.md), there is now a test option to generate the JSON guides matching your current running version of FoSpy.
- [Required Map Guide:](./required.md) This JSON contains every field that is required for a FOS to be considered valid.
- [Optional Map Guide:](./optional.md) This JSON contains every field in the required guide, but also contains any optional field that may not be required, but are still configured with validation rules.
  - Some optional fields in this guide are mutually exclusive. If you find that your FOS files are getting rejected, or fields are getting deleted on validation, consult the [expected properties](../../expected/index.md) page.

