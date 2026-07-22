# from FoSpy.blocks import TemplateBlock, PathFile as TestBlock
from pprint import pp

# class TestTemplate(TemplateBlock, TestBlock):
#     pass

# values = TestTemplate.find_dispatch_values()

# pp(values)

# pass


from FoSpy.blocks import Annealing, Attachment, EmbeddedFile, CIFFile, PathFile

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
anneal = Annealing(anneal_dict)

embedded_dict = {
    "file_name": "test.cif",
    "embedded": "this is my embedded file"
}
embedded1 = EmbeddedFile(embedded_dict)
embedded2 = CIFFile(embedded_dict)
embedded3 = Attachment(embedded_dict)

path_dict = {
    "file_name": "idek.idek",
    "path": "../../hello/world"
}
path1 = PathFile(path_dict)
path2 = Attachment(path_dict)

try:
    path3_fail = CIFFile(path_dict)
    raise Exception("Should have failed")
except Exception as e:
    print("Failed as expected")
    print(e)






