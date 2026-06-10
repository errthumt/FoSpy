def map_to_fos(filepath=None, map_name=None):
    from .utils import map_data_to_properties, fill_properties
    from .. import cfg
    import json
    from tkinter import Tk, filedialog
    root = False

    maps = cfg.json_maps

    if filepath is None:
        root = Tk()
        root.withdraw()
        filepath = filedialog.askopenfilename(title="Select a .json input file to be mapped.", filetypes=[("JSON files", "*.json")])

    with open(filepath, "r") as f:
        input_data = json.load(f)

    if map_name is None:
        if maps.get("default") is None:
            map_name = input("\nNo default map found. Please enter an existing map name (Press Enter to load new map): ")

            if not map_name:
                if not root:
                    root = Tk()
                    root.withdraw()
                filepath = filedialog.askopenfilename(title="Select a new .json map file.", filetypes=[("JSON files", "*.json")])
                print(f"\nLoaded map file: {filepath}")
                
                get_missing = input("\nLoad missing values? (y/n): ").lower().strip() == "y"
                if get_missing:
                    missing_path = filedialog.askopenfilename(title="Select a .json missing values file.", filetypes=[("JSON files", "*.json")])
                    print(f"\nLoaded missing values file: {missing_path}")
                else:
                    missing_path = None

                map_name = input("\nEnter a name for the new map: ")

                new_map(filepath, map_name, missing_path)
        else:
            map_name = maps.default
            print(f"\nNo map specified. Loaded default map: {map_name}\n"
                  "- To use a different map, use the map_name argument.\n"
                  "- To create a new map or overwrite an existing one, "
                  "use the new_map() function. New maps can be set "
                  "immediately as default using "
                  "new_map(..., set_default=True)")
    
    map_dict = maps.get(map_name, {})
    if not map_dict:
        raise ValueError(f"Map {map_name} not found.")
    if root:
        root.destroy()
    property_dict = map_data_to_properties(input_data, **map_dict)
    return fill_properties({}, **property_dict)
    


def new_map(filepath, map_name=None, missing_path=None, save=None, set_default=False):
    from ..config import save as cfg_save, values as cfg
    import json
    import os
    maps = cfg.json_maps

    with open(os.path.abspath(filepath), 'r') as f:
        map_data = json.load(f)

    if missing_path is not None:
        with open(os.path.abspath(missing_path), 'r') as f:
            missing = json.load(f)
    else:
        missing = {}

    map_dict = {"map_dict": map_data, "missing_dict": missing}

    setattr(maps, map_name, map_dict)

    if maps.get("default") is None or set_default:
        maps.default = map_name

    if save is None:
        save = input("\nThe new map is saved to the current session only. "
                     "Saving now will also save any other changes within this session. "
                     "Save changes to config? (y/n): ").lower().strip() == "y"
    
    if save:
        cfg_save(prompt=False)
