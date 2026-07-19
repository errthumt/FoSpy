# FoSpy
A framework for opening, editing, and saving Files of Synthesis (*.fos)
* [Main Github](https://github.com/errthumt/FoSpy)
* [GUI Proof of Concept](https://github.com/errthumt/CyFoS-alpha)
  * FOS syntax for the GUI alpha is an earlier iteration and may no longer be in use.


[Code Example](https://errthumt.github.io/FoSpy/examples/API_example/)

## A Simple FOS File

```fos
fos_id: TE001
fos_type: synthesis
// This comment will stay attached to the description when saving
// (Until comments are cleared)
description: My First Synthesis
group_id: kovnir-0000-0003-1152-1912
project_id: travis5672/clathrates/Ba2-TM5-Sb6

[Experimenters]
name: Travis Errthum
affiliation: Kovnir Group - Iowa State University
orcid: 0009-0006-1937-5672

// Single brackets on a header mean there is only one group
[Reaction]
nominal_formula: Ba2Zn5Sb6
nominal_amount: 250.0
nominal_amount_unit: milligram

[Products]
name: Barium Zinc Antimonide (2-5-6)
formula: Ba2Zn5Sb6
expected: True
obtained: True
expected_amount: 250.0
expected_amount_unit: milligram
obtained_amount: 200.0
obtained_amount_unit: milligram
observations: Black Powder
characterizations: PXRD, EDS, Eyeballs
structure_comments: Unique clathrate with novel polyhedra. Space group Pnma

// Double brackets on a header mean there are multiple similar groups
[Materials]
name: Barium
type: reagent
formula: Ba
supplier: Thermofisher
cas: 7440-39-3
form: lump
purity: 0.999
env: Ar (g)
// The comment below will be correctly re-calculated using a calc_routine
amount: 2.0
amount_unit: mol ratio
// Similar to headers, single brackets mean there is only one group,
// in this case for treatments of Barium
treatments: [
    type: cutting
    repeats: 1
    observations: smaller pieces improve homogenization
]

// This is a comment on the treatments block
[Treatments]

[[Attachments]]
// You can also attach files with relative paths.
file_name: attached.cif
path: projects/my_cifs

file_name: Ba2Zn5Sb6_ICSD.cif
embedded: {{{
['Embedded CIF Text Goes Here\n']
#################### END FOS EMBED }}}
```
