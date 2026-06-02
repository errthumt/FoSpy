# Full Example Script

Uninterrupted code extracted from the [API example walkthrough](./index.md).

```python
def main():
    from FoSpy.blocks.synthesis import Synthesis
    from FoSpy.blocks.template import TemplateSet
    from chemformula import ChemFormula


    # No debug messages by default, but they can be turned on like this.
    from FoSpy._debug import all_debugs_on, all_debugs_off
    all_debugs_on(soundoff=False)

    # Change the width of your debug screen so that module labels print on one line.
    from FoSpy import _debug as db
    db.DEBUG_WIDTH = 120

    # Optional way to turn on/off one module's debug messages.
    from FoSpy.blocks.blocks import _debug as block_debug
    block_debug.on = True


    # load synthesis and templates from files
    my_synthesis = Synthesis.fromFile(r"synthesis/start_synthesis.fos")
    my_templates = TemplateSet.fromFile(r"templates/start_templates.fos")

    # save the synthesis to a json for comparison
    my_synthesis.save(r"synthesis/start_synthesis.json")

    # save the files to new files so that they don't overwrite the old ones.
    my_synthesis.save(r"synthesis/check01.fos")
    my_templates.save(r"templates/check01.fos")


    # some shortcuts so I don't need to keep referencing my_synthesis
    my_meta = my_synthesis.metadata
    my_exps = my_synthesis.experimenters
    my_reaction = my_synthesis.reaction
    my_mats = my_synthesis.cifs
    my_mats = my_synthesis.materials
    my_treats = my_synthesis.treatments


    my_synthesis.clear_all_comments()
    my_synthesis.rename_block("materials","reagents")
    my_mats = my_synthesis.reagents
    my_synthesis.rename.add_comments("This new block has been added because I renamed a required block.")
    my_synthesis.rename.materials.add_comments("Synthesis files are required to have a materials block, so",
                                               "This line specifies that it has been renamed to reagents.")

    my_exps[0].rename_block("affiliation","isu_research_group")
    my_synthesis.keys_to_end("cifs")
    my_synthesis.save("synthesis/check02.fos")


    # change some metadata for my synthesis
    my_meta.name = "TE002"
    my_meta.date = "05-17-2026"
    my_meta.internal_project_ID = "Arsenide 28+d clathrates"
    my_reaction.nominal_formula = "Ba8Cu13Zn11As28.5"

    my_synthesis.products = [{
        "name": "Barium transition-metal arsenide (8-24-28.5)",
        "formula": "Ba8Cu13Zn11As28.5",
        "expected": True,
        "obtained": True,
        "expected_amount": "250.0",
        "expected_amount_unit": "mg",
        "obtained_amount": "150.0",
        "obtained_amount_unit": "mg",
        "observations": "Gray Powder",
        "characterizations": "PXRD",
        "structure_comments": "Unique clathrate with variable occupancy on hyper-coordinate Arsenic site. Space group Cmcm"
    }]

    my_synthesis.save("synthesis/check03.fos")


    my_synthesis.clear_all_comments()
    # more shortcuts
    exp_temps = my_templates.experimenters
    mat_temps = my_templates.materials
    cif_temps = my_templates.cifs

    # template file has a template for Joe, but it's missing an affiliation value.
    # So I fill in the affiliation and add it to the experimenters on my synthesis
    joe_template = exp_temps.get_first(template_name="Joe")
    joe = joe_template.fill(affiliation="Kovnir Group - Iowa State University")
    my_exps.append(joe)
    my_exps.add_comments("Note that now there are two experimenters, so the",
                         "experimenters header has changed to double brackets")
    my_synthesis.save("synthesis/check04.fos")


    my_synthesis.clear_all_comments()

    travis = my_synthesis.experimenters[0]
    travis.add_block("friend","experimenter",joe.copy())
    travis.friend.affiliation = "Graham's Dad"

    travis.rename_block("friend","colleague")

    travis.colleague.add_comments("This copy of Joe has information about him as Travis's colleague")
    joe.name.add_comments("This copy of Joe has information about him as an experimenter")
    my_exps.add_comments("Note that there are now multiple experimenters in this block,",
                         "So the header now has double brackets")

    my_synthesis.save("synthesis/check05.fos")


    # Changing Barium's molar ratio
    my_mats[0].amount = 8


    # I find zinc in my materials, change its ratio, and also generate a template
    # from it.
    zinc = my_mats.get_first(form="powder")
    zinc.amount = 11

    # The template name is "A generic metal powder, purity 0.995", and it has empty
    # fields for name, formula, cas, and ratio
    powder_template = zinc.make_template("A generic metal powder, purity 0.995",
                                          "name","formula","cas","amount")
    powder_template.default_key_order()

    # This saves my powder template to a new category of templates titled "Generic$materials"
    my_templates.add_block("generic","materials", powder_template)
    my_templates.keys_to_end("cifs")


    # Setting up information that I want to fill into the powder template
    copper_info = {
        "name": "Copper",
        "formula": "Cu",
        "cas": "7440-50-8",
        "amount": 13
    }

    # Generate a new material, copper, from the template I made earlier and add it
    # to my synthesis materials
    copper = powder_template.fill(**copper_info)
    copper.clear_comments()
    my_mats.append(copper)

    # Here I'm using the arsenic template that was already in the template file to
    # replace antimony.
    arsenic_template = mat_temps.get_first(formula=ChemFormula("As"))
    arsenic = arsenic_template.fill(type="reagent", amount=28.5)
    my_mats.remove_any(cas="7440-36-0") # This removes the antimony from my synthesis
    my_mats.append(arsenic)

    clear = [file.clear_all_comments() for file in (my_synthesis, my_templates)]
    my_synthesis.save("synthesis/check06.fos")
    my_templates.save("templates/check06.fos")


    # Building templates from the existing annealing program on my synthesis so that
    # I can replace it with a different program.
    anneal_template = my_treats[2].make_template("Empty Anneal Template",
                                                 "repeats", "observations","program")
    anneal_template.clear_comments()
    ramp_template = my_treats[2].program[0].make_template("Any ramp",
                                                          "temp", "time")
    dwell_template = my_treats[2].program[1].make_template("Any dwell",
                                                           "time")
    # Save my new templates to my template file.
    my_templates.treatments = [anneal_template]
    my_templates.anneal_sections = [ramp_template, dwell_template]
    my_templates.keys_to_end("cifs")

    # Filling in my annealing templates
    ramp1 = ramp_template.fill(temp="550", time="2")
    ramp2 = ramp_template.fill(temp="650", time = "10")
    dwell1 = dwell_template.fill(time="12")
    dwell2 = dwell_template.fill(time="72")

    # Using my anneal template to create two different annealing treatments with my
    # different program sections.
    anneal1 = anneal_template.fill(repeats=1,
                                   observations="None",
                                   program=[ramp1, dwell1])
    anneal2 = anneal_template.fill(repeats=1,
                                   observations="None",
                                   program=[ramp2, dwell2])

    anneal1.program.append({"type":"quench","medium":"water"})

    my_templates.save("templates/check07.fos")


    # Remove all treatments except the first two
    my_treats.remove_idx(from_idx=2)

    # Adding both annealing treatments to my synthesis
    for anneal in (anneal1, anneal2):
        my_treats.append(anneal)

    my_synthesis.save("synthesis/check08.fos")


    # Copying Phil's cif from my templates into my synthesis.
    py618 = cif_temps[0].copy()
    my_synthesis.cifs.append(py618)

    # copying the Ba2Zn5Sb6 cif from my synthesis to my templates
    Ba2Zn5Sb6 = my_synthesis.cifs[0]
    cif_temps.insert(0,Ba2Zn5Sb6)

    # removing the Ba2Zn5Sb6 from my synthesis because it's not applicable for this
    # sample.
    my_synthesis.cifs.remove_any(file_name="Ba2Zn5Sb6_ICSD")

    my_templates.save("templates/check09.fos")
    my_synthesis.save("synthesis/check09.fos")


    # Every material gets a weight percent comment added above their ratio
    my_synthesis.add_calc_routine("reagents.add_weight_pcts")
    '''for anneal in my_synthesis.treatments.get_any(type="anneal"):
        anneal.add_calc_routine("program.add_all_missing_parameters")'''
    my_synthesis.reagents[0].amount.add_comments("Weight percents were calculated automatically when saving.")


    # some reordering stuff to make the final printout more consistent.
    my_templates.default_key_order()
    my_templates.key_to_idx("generic", 3)
    my_templates.key_to_idx("anneal_sections", 5)
    my_templates.generic.set_list_type("explicit")

    my_synthesis.default_key_order()
    my_synthesis.key_to_idx("reagents", 5)
    my_mats.set_list_type("looped")

    my_templates.save("templates/check10.fos")
    my_synthesis.save("synthesis/check10.fos")

    # Silence all debugs except the one used for checking equality.
    all_debugs_off(soundoff=False)
    db._debug.on = True

    # Check to see if the saved file matches the current python object.
    print(f"Synthesis matches: {my_synthesis.matches_file()}")
    print(f"Templates match:   {my_templates.matches_file()}")


    my_synthesis.cifs[0].quick_pattern(subprocess=True)


    my_synthesis.treatments.get_first(type="anneal").show_plot()

if __name__ == '__main__':
    main()
```