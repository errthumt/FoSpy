from FoSpy import TemplateSet, Synthesis

from pprint import pp

from parseTest import READ_PATH, WRITE_PATH
TEMPLATE_PATH = r'tests\test_fos\template_test.fos'
WRITE_TEMPLATE_PATH = r'tests\test_fos\template_write_test.fos'

def tempTest1():
    my_templates = TemplateSet.fromFile(TEMPLATE_PATH)
    my_synthesis = Synthesis.fromFile(READ_PATH)

    antimony = my_templates.materials.get_obj("Antimony, Glovebox")
    antimony.ratio = "6.0"

    my_synthesis.materials.append(antimony)
    my_synthesis.materials.remove_any(name="Arsenic")

    my_synthesis.save(WRITE_PATH)

    zinc = my_synthesis.materials[1]

    my_templates.materials.append(zinc, "Zinc powder, Glovebox")
    my_templates.treatments.remove_any(type="anneal")
    my_templates.save(WRITE_TEMPLATE_PATH)

def tempTest2():
    mySyn = Synthesis.fromFile(READ_PATH)

    zinc = mySyn.materials[1]

    mySyn.materials.remove_any(name="Zinc")

    mat_template = zinc.make_template("basic material","name", "formula", "supplier", "ratio")
    copper_dict = {
        "name": "Copper",
        "formula": "Cu",
        "supplier" : "Sigma-Aldrich",
        "ratio" : "13.0000"
    }

    copper = mat_template.fill(**copper_dict)
    copper.add_calc_routine("add_MW")
    mySyn.materials.append(copper)
    mySyn.save(WRITE_PATH)

if __name__  == "__main__":
    tempTest2()