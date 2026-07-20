# from FoSpy.blocks import TemplateBlock, PathFile as TestBlock
from pprint import pp

# class TestTemplate(TemplateBlock, TestBlock):
#     pass

# values = TestTemplate.find_dispatch_values()

# pp(values)

# pass


from FoSpy.blocks import Annealing

anneal_dict = {
    "type": "anneal",
    "repeats": 1,
    "program": [
        {
            "type": "ramp",
            "time": "10",
            "time_unit": "min",
            "temp": "800",
            "temp_unit": "C"
        }
    ],
    "start_temp": "25",
    "start_temp_unit": "C"
}

anneal = Annealing.dispatch_subclass(anneal_dict)

anneal_template = anneal.make_template("anneal_template", "program")

serial = anneal_template.serialize()
pp(serial)

anneal_dict["program"] = [{"type": "dwell"}]

reflexed = Annealing.reflex(serialize=False, **anneal_dict)

pp(reflexed.serialize())

pass