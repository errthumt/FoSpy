from FoSpy.json.utils import map_data_from_json, fill_properties
from FoSpy.blocks.synthesis import Synthesis
from FoSpy.blocks.blocks import ListBlock, SingleBlock
from FoSpy.parsing import validation
import json

def main():
    # Input Files
    DATA_PATH = "SSMC-CI_2026/json_example/input/eln_data.json"
    MAP_PATH = "SSMC-CI_2026/json_example/input/eln_map.json"
    MISSING_PATH = "SSMC-CI_2026/json_example/input/missing.json"

    # Output Files
    PROPERTY_PATH = "SSMC-CI_2026/json_example/output/properties.json"
    SYNTHESIS_JSON_PATH = "SSMC-CI_2026/json_example/output/synthesis.json"
    SYNTHESIS_ORDERED_PATH = "SSMC-CI_2026/json_example/output/synthesis-ordered.json"
    SYNTHESIS_FOS_PATH = "SSMC-CI_2026/json_example/output/synthesis.fos"

    # Generate top-level dict mapping synthesis-relative property strings to values
    property_dict = map_data_from_json(DATA_PATH, MAP_PATH, MISSING_PATH)
    with open(PROPERTY_PATH, "w") as f:
        json.dump(property_dict, f, indent=4)

    # Generate structured dict matching structure required by Synthesis constructor
    synthesis_dict = fill_properties({},**property_dict)
    with open(SYNTHESIS_JSON_PATH, "w") as f:
        json.dump(synthesis_dict, f, indent=4)

    # Construct synthesis and rearrange key orders for easy reading
    my_synthesis = Synthesis(synthesis_dict)
    my_synthesis.default_key_order(deep=True)
    my_synthesis.key_to_idx("laboratory", 2)

    # Set gas_flow list to use "looped" list type for example
    my_synthesis.treatments[0].gas_flow.set_list_type("looped")

    # Save finalized json and fos files.
    my_synthesis.to_json(SYNTHESIS_ORDERED_PATH)
    my_synthesis.save(SYNTHESIS_FOS_PATH)
    pass


if __name__ == "__main__":
    main()