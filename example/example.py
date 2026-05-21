from FoSpy import Synthesis, TemplateSet, ListBlock, EmbeddedCIF, TemplateList, Material, SubContainer
from chemformula import ChemFormula

# No debug messages by default, but they can be turned on like this.
from FoSpy._debug import all_debugs_on, all_debugs_off
all_debugs_on(soundoff=False)

# change the width of your debug screen so that module labels print on one line.
from FoSpy import _debug as db
db.DEBUG_WIDTH = 140

# Optional way to turn on/off one module's debug messages.
from FoSpy.blocks.blocks import _debug as block_debug
block_debug.on = True

"""
The beginning and end results of this file can be found in the same folder of
the github. Click on the "example" folder in FoSpy / example / example.py
"""

# load synthesis and templates from files
my_synthesis = Synthesis.fromFile(r"example/start_synthesis.fos")
my_templates = TemplateSet.fromFile(r"example/start_templates.fos")

# save the files to new files so that they don't overwrite the old ones.
my_synthesis.save(r"example/end_synthesis.fos")
my_templates.save(r"example/end_templates.fos")

# some shortcuts so I don't need to keep referencing my_synthesis
my_meta = my_synthesis.metadata
my_exps = my_synthesis.experimenters
my_reaction = my_synthesis.reaction
my_mats = my_synthesis.materials
my_treats = my_synthesis.treatments

# more shortcuts
exp_temps = my_templates.experimenters
mat_temps = my_templates.materials
cif_temps = my_templates.cifs

# change some metadata for my synthesis
my_meta.name = "TE002"
my_meta.date = "05-17-2026"
my_meta.internal_project_ID = "Arsenide 28+d clathrates"
my_reaction.nominal_formula = "Ba8Cu13Zn11As28.5"

# attach a new comment to the nominal_mass
my_reaction.add_comments("nominal_mass", "I attached this comment in python")

# template file has a template for Joe, but it's missing an affiliation value.
# So I fill in the affiliation and add it to the experimenters on my synthesis
joe_template = exp_temps.get_first(template_name="Joe")
joe = joe_template.fill(affiliation="Graham's Dad")
my_exps.append(joe)
my_synthesis.add_comments("experimenters",
                          "Note that now there are two experimenters, so the",
                          "experimenters header has changed to double brackets")

# python indexes are zero-based, so this changes the first material (Barium)'s
# ratio to 8
my_mats[0].ratio = 8

# I find zinc in my materials, change its ratio, and also generate a template
# from it.
zinc = my_mats.get_first(form="powder")
zinc.ratio = 11

# The template name is "A generic metal powder, purity 0.995", and it has empty
# fields for name, formula, cas, and ratio
powder_template = zinc.make_template("A generic metal powder, purity 0.995",
                                      "name","formula","cas","ratio")
powder_template.default_key_order()

# This saves my powder template to a new category of templates titled "Generic
# Materials"
my_templates.generic_materials = [powder_template]

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
copper.clear_comments()
my_mats.append(copper)

# Here I'm using the arsenic template that was already in the template file to
# replace antimony.
arsenic_template = mat_temps.get_first(formula=ChemFormula("As"))
arsenic = arsenic_template.fill(type="reagent", ratio=28.5)
my_mats.remove_any(cas="7440-36-0") # This removes the antimony from my synthesis
my_mats.append(arsenic)

# Building templates from the existing annealing program on my synthesis so that
# I can replace it with a different program.
anneal_template = my_treats[2].make_template("Empty Anneal Template",
                                             "repeats", "observations","program")
anneal_template.clear_comments()
ramp_template = my_treats[2].program[0].make_template("Any ramp",
                                                      "temp", "time")
dwell_template = my_treats[2].program[1].make_template("Any dwell",
                                                       "time")

from FoSpy import Treatment
test = Treatment.reflex()

# Save my new templates to my template file.
my_templates.treatments = [anneal_template]
my_templates.anneal_sections = [ramp_template, dwell_template]

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

# Remove all treatments except the first two
my_treats.remove_idx(from_idx=2)

# Adding both annealing treatments to my synthesis
for anneal in (anneal1, anneal2):
    my_treats.append(anneal)

# Copying Phil's cif from my templates into my synthesis.
py618 = cif_temps[0].copy()
my_synthesis.cifs.append(py618)

# copying the Ba2Zn5Sb6 cif from my synthesis to my templates
Ba2Zn5Sb6 = my_synthesis.cifs[0]
cif_temps.insert(0,Ba2Zn5Sb6)

# removing the Ba2Zn5Sb6 from my synthesis because it's not applicable for this
# sample.
my_synthesis.cifs.remove_any(file_name="Ba2Zn5Sb6_ICSD")

# Every material gets a weight percent comment added above their ratio
my_synthesis.add_calc_routine("materials.add_weight_pcts")

# some reordering stuff to make the final printout more consistent.
my_templates.default_key_order()
my_templates.generic_materials.set_list_type("explicit")
my_mats.set_list_type("looped")


# save all my changes
saved = [file.save() for file in (my_templates, my_synthesis)]


# Silence all debugs except the one used for checking equality.
all_debugs_off(soundoff=False)
db._debug.on = True

# Check to see if the saved file matches the object.
print(my_synthesis.matches_file())
print(my_templates.matches_file())

pass # break point for debugging.