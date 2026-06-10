REGISTRY = {
    "str": str,
    "bool": bool,
    "int": int,
    "float": float
}


def enforce_config():
    from . import module
    from ._load import get_enforced_file
    import json

    with open(get_enforced_file(), 'r') as f:
        enforced_dict = json.load(f)

    checks = _generate_checks(enforced_dict)

    module.values = _add_enforcement(module.values, checks)

def _add_enforcement(module, checks):
    module._enforced = {}

    for key, val in checks.items():
        if isinstance(val, dict):
            setattr(module, key, _add_enforcement(getattr(module, key), val))
        elif isinstance(val, tuple):
            module._enforced[key] = val

    return module

def _generate_checks(enforced_dict):
    out = {}

    for key, val in enforced_dict.items():

        if isinstance(val, dict):
            out[key] = _generate_checks(val)

        elif isinstance(val, list):
            if (
                not len(val)==3 or 
                not all([isinstance(v, list) for v in val[:2]]) or 
                not isinstance(val[2], str)):
                raise ValueError("Enforcement json should contain a [goodchecks, badchecks, hint] set for each enforced key")
            
            goodchecks, badchecks, hint = val
            enforce = []
            for checkset in val[:2]:
                checks = []
                for typestr in checkset:
                    if ":" in typestr:
                        typ, arg = typestr.split(":")
                        typ = REGISTRY.get(typ, None)
                        if typ is None:
                            raise ValueError(f"Unknown enforcement type '{typ}' in {key}")
                        checks.append(lambda x, t=typ, a=arg: x == t(a))
                    
                    else:
                        typ = REGISTRY.get(typestr, None)
                        if typ is None:
                            raise ValueError(f"Unknown enforcement type '{typestr}' in {key}")
                        checks.append(lambda x, t=typ: isinstance(x, t))

                enforce.append(checks)
            out[key] = (*enforce, hint)

        else:
            raise ValueError(f"Enforcement json should contain a [goodchecks, badchecks, hint] set for each enforced key")
    
    return out
