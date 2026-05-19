# Example Usage for FoSpy

The files in this folder are examples of what a script-side editing session might look like for Synthesis and Template files using the FOS format.

Most users won't want to write scripts like these for every synthesis, but given enough script capabilites, we can move toward writing scripts that automate generating synthesis files from many similar data inputs.

The full script can be found in [example.py](./example.py), but each snippet is pulled apart here and explained.

The full script was run on the files in this folder:
* [start_synthesis.fos](./start_synthesis.fos)
* [start_templates.fos](./start_templates.fos)

The result files were created directly by python with no user editing:
* [end_synthesis.fos](./end_synthesis.fos)
* [end_templates.fos](./end_templates.fos)

## Opening Files and Saving Copies
This code loads my synthesis and my templates from my respective files, and then saves them to a different location. Once the location has been changed, calling `save()` without a filename will now just re-save them in the new location
```python
# open files
my_synthesis = Synthesis.fromFile(r"example/start_synthesis.fos")
my_templates = TemplateSet.fromFile(r"example/start_templates.fos")
# save the files to new files so that they don't overwrite the old ones.
my_synthesis.save(r"example/end_synthesis.fos")
my_templates.save(r"example/end_templates.fos")
```
## Object-Oriented Shortcuts
The nice thing about python is that if you set a variable equal to something, in most cases, it just points at that thing instead of making a new variable. So any edits to `my_meta`, for example, will also be edits to `my_synthesis.metadata`.
```python
# some shortcuts so I don't need to keep referencing my_synthesis
my_meta = my_synthesis.metadata
my_reaction = my_synthesis.reaction
my_mats = my_synthesis.materials
my_treats = my_synthesis.treatments

# more shortcuts
exp_temps = my_templates.experimenters
mat_temps = my_templates.materials
cif_temps = my_templates.cifs
```

## Changing MetaData
Here I change some of the important metadata for my synthesis. Certain variables are automatically converted. For example, the `nominal_formula` is coded to be a `ChemFormula` object, so when I set that variable, it automatically converts the text into a true formula object and raises an error if it's not able to read it.
```python
# change some metadata for my synthesis
my_meta.name = "TE002"
my_meta.date = "05-17-2026"
my_meta.internal_project_ID = "Arsenide 28+d clathrates"
my_reaction.nominal_formula = "Ba8Cu13Zn11As28.5"
```

## Adding Comments
Comments are attached to the information below them when being read from the file so that they can be preserved when saved. I can also add another comment that will be attached to the `nominal_mass` when saving the file.
```python
# attach a new comment to the nominal_mass
my_reaction.add_comment("nominal_mass", "I attached this comment in python")
```

## Filling in Templates
My template file contains a template for an experimenter named Joe, but it's programmed to be missing an affiliation value. I can generate a new, complete experimenter by calling the `fill()` command on the template. Then I add that experimenter to my synthesis metadata.
```python
joe_template = exp_temps.get_first(template_name="Joe")
joe = joe_template.fill(affiliation="Graham's Dad")
my_meta.experimenters.append(joe)
```

## Editing objects in listed blocks
The materials block of my synthesis (`my_mats = my_synthesis.materials`) is a fancy list of `Material` objects. I can access an individual item in that list with an index in brackets (`my_mats[i]`).
```python
# python indexes are zero-based, so this changes the first material (Barium)'s
# ratio to 8
my_mats[0].ratio = 8
```

## Finding objects in listed blocks
Listed blocks have two finding commands, `get_any()` and `get_first`. `get_any()` returns a list of objects that match the criteria you give. `get_first()` returns the first match. Objects returned by these functions point to the actual objects in the synthesis, not copies, so I can edit them after finding them and the edits go into the synthesis.
```python
# I find zinc in my materials, change its ratio, and also generate a template
# from it.
zinc = my_mats.get_first(form="powder")
zinc.ratio = 11
```

## Generating templates from existing objects.
Here, I have already identified a `Material` object called zinc. But I have lots of materials in my lab with many of the same properties as zinc. So I generate a generic "powder" template, and specify which fields I want to be empty in the template. This template cannot be converted back into `Material` objects unless all of the required fields are filled back in.
```python
# The template name is "A generic metal powder, purity 0.995", and it has empty
# fields for name, formula, cas, and ratio
powder_template = zinc.make_template("A generic metal powder, purity 0.995",
                                      "name","formula","cas","ratio")
powder_template.default_key_order()

# This saves my powder template to a new category of templates titled "Generic
# Materials"
my_templates.generic_materials = [powder_template]
```

## Filling in templates with lots of information
Sometimes its tedious to fill in templates with all the information in one line, like `fill(arg1="foo", arg2="bar", arg3=...)`. This can be sped up if I already have a dictionary of what the missing properties are that I want to fill in.
```python
# Setting up information that I want to fill into the powder template
copper_info = {
    "name": "Copper",
    "formula": "Cu",
    "cas": "7440-50-8",
    "ratio": 13
}

# Generate a new material, copper, from the template I made earlier and add it
# to my synthesis materials
copper = powder_template.fill(**copper_info)
my_mats.append(copper)
```

## Removing objects from listed blocks
My new synthesis has arsenic in it, not antimony. So I fill in the type and ratio from my arsenic template, then I remove antimony and add arsenic to the synthesis. Note that I remove antimony using the `remove_any()` command with `cas="7440-36-0"`. You can remove or find objects in a listed block with any identfying variable, as long as it's been defined for the object you're looking for.
```python
# Here I'm using the arsenic template that was already in the template file to
# replace antimony.
arsenic_template = mat_temps.get_first(formula=ChemFormula("As"))
arsenic = arsenic_template.fill(type="reagent", ratio=28.5)
my_mats.remove_any(cas="7440-36-0") # This removes the antimony from my synthesis
my_mats.append(arsenic)
```

## Re-using templates
When you fill in a template, it creates a copy with all the values filled in. So once I build a template of, say, a ramp section of an annealing profile, I can use that template to create several different ramp sections with different filled in values.
```python
# Building templates from the existing annealing program on my synthesis so that
# I can replace it with a different program.
anneal_template = my_treats[2].make_template("600/10hr, 120hr",
                                             "repeats", "observations","program")
ramp_template = my_treats[2].program[0].make_template("Any ramp",
                                                      "temp", "time")
dwell_template = my_treats[2].program[1].make_template("Any dwell",
                                                       "time")

# Filling in my annealing templates
ramp1 = ramp_template.fill(temp="550 C", time="2 hr")
ramp2 = ramp_template.fill(temp="650 C", time = "10 hr")
dwell1 = dwell_template.fill(time="12 hr")
dwell2 = dwell_template.fill(time="72 hr")

# Using my anneal template to create two different annealing treatments with my
# different program sections.
anneal1 = anneal_template.fill(repeats=1,
                               observations="None",
                               program=[ramp1, dwell1])
anneal2 = anneal_template.fill(repeats=1,
                               observations="None",
                               program=[ramp2, dwell2])
```

## Removing listed blocks by index
This code will be cleaner in the future, but for now, I redefine the treatments in my synthesis as being only the first two of the original synthesis.
```python
# Remove all but the first two treatments.
my_treats.remove_idx(from_idx=2, to_idx=None)

# After removing the old treatments, I can add in the two new annealings that I made.
for anneal in (anneal1, anneal2):
    my_treats.append(anneal)
```

## Managing embedded Files
Embedded files are just blocks like every other section, except they have a special `embedded` property that stores the un-edited lines of the original file.
```python
# Copying Phil's cif from my templates into my synthesis.
py618 = cif_temps[0].copy()
my_synthesis.cifs.append(py618)

# copying the Ba2Zn5Sb6 cif from my synthesis to my templates
Ba2Zn5Sb6 = my_synthesis.cifs[0]
cif_temps.insert(0,Ba2Zn5Sb6)

# removing the Ba2Zn5Sb6 from my synthesis because it's not applicable for this
# sample.
my_synthesis.cifs.remove_any(file_name="Ba2Zn5Sb6_ICSD")
```

## Calculation Routines
There is the capability to add "calculation_routines" to be executed when saving the file. This schedules commands to be run right before saving, so that calculated values are correct for the current state of the synthesis. Here, I schedule a calculation routine that will add a comment with weight percent above the ratio of every material with matching type. Calculated comments are given a special syntax so that they are stored when reading a FOS file, and they can be overwritten at any time with a new updated value.
```python
# Every material gets a weight percent comment added above their ratio
my_synthesis.add_calc_routine("materials.add_weight_pcts", type="reagent")
```

## Cleaning up.
All of the information in my new synthesis is now stored, and all the changes to my templates are now stored. But in the process, some of the information has been moved around or tacked on in ways that will make the FOS file hard to read in plain text. This doesn't matter for programs that are loading, editing, and saving files many files directly, but we can also clean up some things so that the file is easy to read:
* Rearrange the blocks in the template file to the default order so that the CIFS are at the bottom of the file.
* Set the generic templates block to use the "explicit" key:value syntax for all of its templates
* Set the synthesis materials block to use the "looped" syntax where all the keys are specified at the beginning of the block.

```python
# some reordering stuff to make the final printout more consistent.
my_templates.default_key_order()
my_templates.generic_materials.set_list_type("explicit")
my_mats.set_list_type("looped")

# save all my changes
saved = [file.save() for file in (my_templates, my_synthesis)]
```