from FoSpy import Synthesis, TemplateSet, ListBlock, EmbeddedCIF, TemplateList, Material
from chemformula import ChemFormula

from FoSpy._debug import all_debugs_on
all_debugs_on(False)

"""
The beginning and end results of this file can be found in the same folder of
the github. Click on the "example" folder in FoSpy / example / example.py
"""

# load synthesis and templates from files
my_synthesis = Synthesis.fromFile(r"example/start_synthesis.fos")
my_templates = TemplateSet.fromFile(r"example/start_templates.fos")

# change some metadata for my synthesis
my_synthesis.metadata.name = "TE002"
my_synthesis.metadata.date = "05-17-2026"
my_synthesis.metadata.internal_project_ID = "Arsenide 28+d clathrates"

# template file has a template for Joe, but it's missing an affiliation value.
# So I fill in the affiliation and add it to the experimenters on my synthesis
joe_template = my_templates.experimenters.get_first(template_name="Joe")
joe = joe_template.fill(affiliation="Graham's Dad")
my_synthesis.metadata.experimenters.append(joe)

# python indexes are zero-based, so this changes the first material (Barium)'s
# ratio to 8
my_synthesis.materials[0].ratio = 8

# I find zinc in my materials, change it's ratio, and also generate a template
# from it.
zinc = my_synthesis.materials.get_first(form="powder")
zinc.ratio = 11

# The template name is "A generic metal powder, purity 0.995", and it has empty
# fields for name, formula, cas, and ratio
powder_template = zinc.make_template("A generic metal powder, purity 0.995",
                                      "name","formula","cas","ratio")
powder_template.default_key_order()

# This saves my powder template to a new category of templates titled "Generic
# Materials"
my_templates.generic_materials = powder_template.serialize()

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
my_synthesis.materials.append(copper)

# Here I'm using the arsenic template that was already in the template file to
# replace antimony.
arsenic_template = my_templates.materials.get_first(formula=ChemFormula("As"))
arsenic = arsenic_template.fill(type="reagent", ratio=28.5)
my_synthesis.materials.remove_any(cas="7440-36-0") # This removes the antimony from my synthesis
my_synthesis.materials.append(arsenic)

# Building templates from the existing annealing program on my synthesis so that
# I can replace it with a different program.
anneal_template = my_synthesis.treatments[2].make_template("600/10hr, 120hr", "repeats", "observations","program")
ramp_template = my_synthesis.treatments[2].program[0].make_template("Any ramp", "temp", "time")
dwell_template = my_synthesis.treatments[2].program[1].make_template("Any dwell", "time")

# Filling in my annealing templates
ramp1 = ramp_template.fill(temp="550 C", time="2 hr")
ramp2 = ramp_template.fill(temp="650 C", time = "10 hr")
dwell1 = dwell_template.fill(time="12 hr")
dwell2 = dwell_template.fill(time="72 hr")

# This line will be cleaner in the future. Right now I have to do some sneaky
# python stuff to remove the last two treatments from my synthesis.
my_synthesis.treatments._objs = my_synthesis.treatments._objs[0:2]

# Using my anneal template to create two different annealing treatments with my
# different program sections.
anneal1 = anneal_template.fill(repeats=1, observations="None", program=[ramp1, dwell1])
anneal2 = anneal_template.fill(repeats=1, observations="None", program=[ramp2, dwell2])

# Adding both annealing treatments to my synthesis
for anneal in (anneal1, anneal2):
    my_synthesis.treatments.append(anneal)

# Copying Phil's cif from my templates into my synthesis.
py618 = my_templates.cifs[0].copy()
my_synthesis.cifs.append(py618)

# copying the Ba2Zn5Sb6 cif from my synthesis to my templates
Ba2Zn5Sb6 = my_synthesis.cifs[0]
my_templates.cifs.insert(0,Ba2Zn5Sb6)

#removing the Ba2Zn5Sb6 from my synthesis because it's not applicable for this sample.
my_synthesis.cifs.remove_any(file_name="Ba2Zn5Sb6_ICSD")

# some reordering stuff to make the final printout more consistent.
my_templates.default_key_order()
my_templates.generic_materials.set_list_type("explicit")
my_synthesis.materials.set_list_type("looped")

# save the files to new files so that they don't overwrite the old ones.
my_synthesis.save(r"example/end_synthesis.fos")
my_templates.save(r"example/end_templates.fos")

new_templates = TemplateSet.fromFile(r"example/end_templates.fos")

pass # break point for debugging.