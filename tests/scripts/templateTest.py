from FoSpy import TemplateSet, Synthesis

from pprint import pp

from parseTest import READ_PATH, WRITE_PATH
TEMPLATE_PATH = r'tests\test_fos\template_test.fos'
WRITE_TEMPLATE_PATH = r'tests\test_fos\template_write_test.fos'

from FoSpy._debug import all_debugs_on
all_debugs_on()

def tempTest1():
    my_templates = TemplateSet.fromFile(TEMPLATE_PATH)
    my_synthesis = Synthesis.fromFile(READ_PATH)

    antimony = my_templates.materials.get_any(template_name="Antimony, Glovebox")[0]
    antimony = antimony.fill(type="special reagent",ratio="6.0")

    my_synthesis.materials.append(antimony)
    arsenic = my_synthesis.materials.get_any(name="Arsenic")[0]
    my_templates.materials.append(arsenic.make_template("Arsenic, Glovebox", "type"))
    my_synthesis.materials.remove_any(name="Arsenic")

    my_synthesis.save(WRITE_PATH)
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
    tempTest1()