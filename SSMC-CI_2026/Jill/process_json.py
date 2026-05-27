import json
from FoSpy.blocks.synthesis import Synthesis

from FoSpy.parsing import validation

def main():

    validation.optional_keys[Synthesis]["laboratory"] = validation.LabConditions
    validation.optional_keys[Synthesis]["equipment"] = validation.EquipmentList


    eln_data = None
    with open("SSMC-CI_2026/Jill/aksha_eln_record.json", "r") as f:
        eln_data = json.load(f)


    template_dict= None
    def save_json(filename):
        with open(filename, "w") as f:
            json.dump(template_dict, f, indent=4)

    def map_to_fill(eln_data, key_map):
        fill_dict = {}
        for key, value in key_map.items():
            if isinstance(value, dict):
                fill_dict.update(map_to_fill(eln_data.get(key), value))
                continue
            fill_dict[value] = eln_data.get(key, "Unknown")
        return fill_dict
    
    def fill_field(temp_dict, key, value):
        temp_dict = temp_dict
        if "." in key:
            parent_key, child_key = key.split(".", 1)
            try:
                idx = int(parent_key)
                if isinstance(temp_dict, dict):
                    temp_dict = []
                while len(temp_dict) <= idx:
                    temp_dict.append({})
                temp_dict[idx] = fill_field(temp_dict[idx], child_key, value)
            except:
                temp_dict.setdefault(parent_key, {})
                temp_dict[parent_key] = fill_field(temp_dict[parent_key], child_key, value)
        else:
            temp_dict[key] = value
        return temp_dict
    

    template_dict = Synthesis.reflex()
    save_json("SSMC-CI_2026/Jill/0_start.json")


    precursor_dict = {
        "name": "Unknown Precursor",
        "type": "precursor",
        "formula": "H",
        "supplier": "Unknown",
        "cas": "Unknown",
        "form": "Unknown",
        "env": "Unknown",
        "ratio": "1.0"
    }

    template_dict["materials"] = [precursor_dict]

    save_json("SSMC-CI_2026/Jill/1_precursor.json")


    eln_map = None
    with open("SSMC-CI_2026/Jill/eln_map.json", "r") as f:
        eln_map = json.load(f)
    
    def fill_template(template_dict, eln_map, eln_data):
        template_dict = template_dict
        for eln_key, template_key in eln_map.items():
            if isinstance(template_key, dict):
                template_dict = fill_template(template_dict, template_key, eln_data.get(eln_key, {}))
            else:
                value = eln_data.get(eln_key, "Unknown")
                template_dict = fill_field(template_dict, template_key, value)
        return template_dict
    
    template_dict = fill_template(template_dict, eln_map, eln_data)

    save_json("SSMC-CI_2026/Jill/2_filled.json")

    remainder = None
    with open("SSMC-CI_2026/Jill/remainder.json", "r") as f:
        remainder = json.load(f)
    
    for key, value in remainder.items():
        template_dict = fill_field(template_dict, key, value)
    save_json("SSMC-CI_2026/Jill/3_filled_remainder.json")

    ramp_time = template_dict["treatments"][0]["program"][0]["temp"]/template_dict["treatments"][0]["program"][0]["rate"]
    ramp_time /= 60.0
    template_dict["treatments"][0]["program"][0]["time"] = ramp_time

    my_synthesis = Synthesis.reflex(serialize=False, **template_dict)
    my_synthesis = my_synthesis.fill()

    for block in (
        my_synthesis,
        my_synthesis.experimenters[0],
        my_synthesis.reaction,
        my_synthesis.materials[0],
        my_synthesis.treatments[0],
        my_synthesis.treatments[0].program[0]
    ):
        block.default_key_order()

    my_synthesis.save("SSMC-CI_2026/Jill/4_final.fos")
    pass



if __name__ == "__main__":
    main()

