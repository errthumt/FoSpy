from ..._docs.properties import _validator_rules

@_validator_rules(
    "Each property of a `Rename` object renames its parent's expected "
    "property of the same name to the provided value.",
    "Renaming properties starting with \"`_`\" is not allowed.",
    "Properties must be expected property names for the parent block.",[
        "For unexpected (custom) keys, adding a rename mapping is not necessary.",
        "(There is no required/optional validator to redirect to.)"
    ],
    "You cannot rename a property to a different expected property. (Unexpected names only.)"
)
def rename_value(val, blk_cls, prop_name, **kwargs):
    if val.startswith("_"):
        raise ValueError("Renaming properties starting with \"_\" is not allowed.")

    validators = blk_cls.build_validators()

    error = f"Cannot rename '{prop_name}' to '{val}'."
    if prop_name not in validators:
        raise ValueError(error, f"'{prop_name}' is not an expected key.")
    if val in validators:
        raise ValueError(error, f"'{val}' is already a registered key.")

    return val


@_validator_rules(
    "A dictionary of key:value string pairs",
    "Keys starting with \"`_`\" are ignored.",
    "Keys must be expected property names for the block.",[
        "For unexpected (custom) keys, renaming is not necessary."
    ],
    "Values cannot be registered property names."
)
def rename_dict(nameDict, blk_cls, **kwargs):
    from FoSpy.blocks.blocks import SingleBlock
    if not isinstance(nameDict, dict):
        raise TypeError("The rename value must be a dictionary of key:value string pairs.")
    vals = blk_cls.build_validators()
    outDict = nameDict.copy()
    for name, rename in nameDict.items():
        if name.startswith("_"):
            outDict.pop(name)
            continue
        error = f"Cannot rename '{name}' to '{rename}' for '{blk_cls.__name__}' block."
        if name not in vals:
            raise ValueError(error, f"'{name}' is not an expected key.")
        if rename in vals:
            raise ValueError(error, f"'{rename}' is already a registered key.")
        
    return SingleBlock.dispatch_subclass(outDict)
    
    