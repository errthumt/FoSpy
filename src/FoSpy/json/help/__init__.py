from ... import Synthesis
def generate_map_guide(cls=Synthesis, include_optional=False, parent_str=""):
    from ...parsing.validation import required_keys, optional_keys
    from ...blocks import ListBlock, SingleBlock

    opt_set = cls.build_validators() if include_optional else cls.build_req_validators()
    opt_set.pop("ext", None)

    guide = {}

    for key, validator in opt_set.items():
        current_key = parent_str + key
        if isinstance(validator, type):
            if issubclass(validator, SingleBlock):
                guide_dct = generate_map_guide(validator, include_optional=include_optional, parent_str=current_key+".")
                guide[key] = guide_dct
                continue
            elif issubclass(validator, ListBlock):
                reqCls = validator._reqCls
                example = [generate_map_guide(reqCls, include_optional=include_optional, parent_str=current_key+f"[{i}].") for i in range(2)]
                guide[key] = example
                continue
            elif issubclass(validator, list):
                example = [current_key+f"[{i}]" for i in range(2)]
                guide[key] = example
                continue

        guide[key] = current_key

    return guide


