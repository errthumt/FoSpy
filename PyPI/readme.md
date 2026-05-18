# FoSpy
A package for opening, editing, and saving Files of Synthesis (*.fos)
* [Main Github](https://github.com/errthumt/FoSpy)
* [GUI Proof of Concept](https://github.com/errthumt/CyFoS-alpha)
  * FOS syntax for the GUI alpha is an earlier iteration and may not be in use.


## Code Example
```python
from FoSpy import Synthesis, TemplateSet

# load synthesis and templates from files
my_synthesis = Synthesis.fromFile(r"example/synthesis.fos")
my_templates = TemplateSet.fromFile(r"example/templates.fos")

# change some metadata for my synthesis
my_synthesis.metadata.name = "TE002"
my_synthesis.metadata.date = "05-17-2026"
my_synthesis.metadata.internal_project_ID = "Arsenide 28+d clathrates"
my_synthesis.reaction.nominal_formula = "Ba8Cu13Zn11As28.5"

# load a template and fill it in before adding to synthesis
arsenic_template = my_templates.materials.get_first(formula=ChemFormula("As"))
arsenic = arsenic_template.fill(type="reagent", ratio=28.5)
my_synthesis.materials.append(arsenic)

# save changes
saved = [file.save() for file in (my_templates, my_synthesis)]
```

## A Simple FOS File
```
name: TE001
date: 03-11-2026
// This comment will remain attached to the experimenters when saving.
experimenters: [
    name: Travis Errthum
    affiliation: Kovnir Group - Iowa State University
    orcid: 0009-0006-1937-5672
]
// ! Comments starting with a ! do not get read from the file.
internal_project_ID: Ba2-TM5-Pn6
internal_project_description: Unique Clathrate

[Reaction]
nominal_formula: Ba2Zn5Sb6
nominal_mass: 250.0
nominal_mass_units: mg

[[Materials]]
:name
:type
:formula
:supplier
:cas
:form
:purity
:env
:ratio
:treatments

    Barium
    reagent
    Ba
    Thermofisher
    7440-39-3
    lump
    0.999
    Ar (g)
    // The comment below will be correctly re-calculated when saving,
    // ...provided that the materials.add_weight_pcts routine is scheduled.
    // otherwise it will be removed altogether.
    // ! Total weight percent: 200%
    2.0
    [
        type: cutting
        repeats: 1
        observations: smaller pieces improve homogenization
    ]
```

