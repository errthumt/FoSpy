def rename_dict(nameDict, cls):
    if not isinstance(nameDict, dict):
        raise TypeError("The rename value must be a dictionary of key:value string pairs.")
    vals = cls.build_validators()
    outDict = nameDict.copy()
    for name, rename in nameDict.items():
        if name.startswith("_"):
            outDict.pop(name)
            continue
        error = f"Cannot rename '{name}' to '{rename}' for '{cls.__name__}' block."
        if name not in vals:
            raise ValueError(error, f"'{name}' is not an expected key.")
        if rename in vals:
            raise ValueError(error, f"'{rename}' is already a registered key.")
        
    return outDict
    
    