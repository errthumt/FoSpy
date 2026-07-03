import json
from ..blocks.synthesis import Synthesis
from warnings import warn


def block_from_file(file_path, block_class=Synthesis):
    """
    Load a block from a JSON file.

    Args:
        file_path (str): The path to the JSON file.
        block_class (class): The class of the block to instantiate. Defaults to SingleBlock.
    """
    with open(file_path, 'r') as f:
        blockDict = json.load(f)
    
    return block_class.dispatch_subclass(blockDict)

def fill_properties(block_dict, **kwargs):
    """
    Fill the properties of a block dictionary with additional keyword arguments.

    Property strings in kwargs can be used to specify nested properties using dot notation for nested dictionaries and bracket notation for lists.

    Example:
        ```
        _fill_properties({}, property1='value1', property2.subproperty='value2', property3[0].subproperty='value3')
        # Returns:
        {
            "property1": "value1",
            "property2": {
                "subproperty": "value2"
            },
            "property3": [
                {
                    "subproperty": "value3"
                }
            ]
        }
        ```

    Args:
        block_dict (dict): The block dictionary to fill.
        **kwargs: Additional properties to add to the block dictionary.
    """
    current_dict = block_dict
    for key, value in kwargs.items():
        if "." in key:
            # Handle nested properties
            parent, child = key.split(".",1)
            if "[" in parent and "]" in parent:
                list_key, idx = parent[:-1].split("[")
                idx = int(idx)
                current_dict.setdefault(list_key, [])
                while len(current_dict[list_key]) <= idx:
                    current_dict[list_key].append({})
                current_dict[list_key][idx] = fill_properties(current_dict[list_key][idx], **{child: value})
            else:
                current_dict.setdefault(parent, {})
                current_dict[parent] = fill_properties(current_dict[parent], **{child: value})
        elif "[" in key and "]" in key:
            raise ValueError(f"Error setting property: {key}.Cannot set property inside a list directly. "
                             "It must be nested inside a dictionary. Entire lists of literal values can "
                             "be passed as values in kwargs.")
        else:
            current_dict[key] = value
    
    return current_dict

def build_property_dict(data, key_map, current={}):
    """Map FoS property abbreviations to values.

    The output dictionary uses abbreviations for nested structures in the FOS
    format. For example, `{"foo[0].bar": 1}` -> `{"foo" : [ {"bar": 1} ] }`.

    Args:
        data (dict): Any JSON-like data structure.
        
        key_map (dict):
            A mirror of the data structure, where values are replaced with FoS
            property abbreviations.
        current (dict, optional):
            Maintains changes on recursion. Defaults to {}.

    Returns:
        dict: Flattened dictionary mapping abbreviated FoS properties to values.
    """
    property_dict = current
    if isinstance(key_map, str):
        if isinstance(data, (dict, list)):
            print()
            warn(f"Structure mismatch: dict or list values can be mapped to string keys, "
                 f"but you may have intended to use a nested mapping for: key_map={key_map}, data={data}.", stacklevel=4)
        if key_map in property_dict:
            print()
            warn(f"Key '{key_map}' was already mapped. Overwriting the existing value.", stacklevel=4)
        property_dict[key_map] = data
        return property_dict
    if isinstance(key_map, dict):
        if not isinstance(data, dict):
            print()
            warn(f"Structure mismatch: cannot map a non-dictionary to a dictionary. Skipping the mapping: "
                 f"key_map={key_map}, data={data}.", stacklevel=4)
            return property_dict
        for key, value in data.items():
            map_value = key_map.get(key, None)
            property_dict = build_property_dict(value, map_value, current=property_dict)
    elif isinstance(key_map, list):
        if not isinstance(data, list):
            print()
            warn(f"Structure mismatch: cannot map a list to a non-list. Skipping the mapping: "
                 f"key_map={key_map}, data={data}.", stacklevel=4)
            return property_dict
        elif len(data) != len(key_map):
            print()
            warn(f"List length mismatch: expected {len(key_map)}, got {len(data)}. Keys will be mapped up to the length of the shorter list.", stacklevel=4)
        
        for key, value in zip(key_map, data):
            property_dict = build_property_dict(value, key_map=key_map, current=property_dict)
        return property_dict
    
    else:
        if key_map is None:
            print()
            warn(f"Skipped: No key mapped for:\n{data}", stacklevel=4)
        else:
            print()
            warn(f"Invalid key_map type: {type(key_map).__name__}. Expected str, dict, or list. Skipping this mapping.", stacklevel=4)
    
    return property_dict

def map_data_to_properties(data_dict, map_dict, missing_dict={}):
    """
    Map a data dictionary to a property dictionary using a mapping dictionary.

    Args:
        data_dict (dict): The data dictionary containing the values.
        map_dict (dict): The mapping dictionary mirroring the structure of the data
            dictionary, where values are replaced with destination property
            names to be passed to `fill_properties()`.

    Returns:
        dict: The constructed property dictionary.
    """
    full_dict = missing_dict
    full_dict.update(build_property_dict(data_dict, map_dict))

    return full_dict

def map_data_from_json(data_path, map_path, missing_path=None):
    """
    Map a data JSON file to a property dictionary using a mapping JSON file.
    Optional missing values can be provided in a separated JSON file.

    Args:
        data_path (str): The path to the JSON file containing the data.
        map_path (str): The path to the JSON file containing the mapping.
        missing_path (str): The path to the JSON file containing any missing values. Defaults to an empty dictionary.

    Returns:
        dict: The constructed property dictionary.
    """

    filepaths = {
        "data_dict": data_path,
        "map_dict": map_path,
        "missing_dict": missing_path
    }

    kwargs = {}

    for name, path in filepaths.items():
        if name == "missing_dict" and path is None:
            kwargs[name] = {}
            continue
        with open(path, 'r') as f:
            kwargs[name] = json.load(f)

    return map_data_to_properties(**kwargs)