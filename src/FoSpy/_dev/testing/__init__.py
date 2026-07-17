from . import (
    load_test,
    map_test,
    map_guides,
    app
)

TESTS = {
    "Validate a Synthesis File": (
        load_test,{
            "Open Results?": ("open_result", True)
        }
    ),
    "Map a JSON to A Synthesis and Validate": (
        map_test,{
            "Open Results?": ("open_result", True),
            "Change Map Name": ("map_name", "default"),
            "Add New Map?": ("make_new", False),
            "Include Missing Values?": ("new_missing", False),
            "Set New Map As Default?": ("new_default", False)
        }
    ),
    "Generate Map Guides": (
        map_guides, {
            "Open Results?": ("open_result", True)
        } 
    ),
    "Open GUI": (
        app, {}
    )
}

REGISTRY = { t.__name__: t for (t,_) in TESTS.values() }
REV_REGISTRY = { v:k for k,v in REGISTRY.items() }

def main(test=None, **args):
    from .ui import get_test, get_options
    
    if test is None:
        while get_test(**args):
            pass
        return False

    else:
        test = REGISTRY.get(test, None)
        if test is None:
            raise ValueError(f"Unknown test name {test}")
        
        for name, (t, options) in TESTS.items():
            if test == t:
                if not args:
                    args = get_options(options, name)
                    if args is None:
                        return True
                    elif not args:
                        return False

                return test.run(**args)

        raise ValueError(f"Could not find arguments for {test.__name__}")


