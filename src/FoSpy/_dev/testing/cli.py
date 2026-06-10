cli_args = {
    "--test" : "test",
    "--loop" : "loop",
    "--help" : "help",
    "--switch" : "switch"
}

from . import TESTS

for label, (test, options) in TESTS.items():
    for k in options.keys():
        cli_args[f"--{k.replace('_', '-')}"] = k

shortcuts = {
    "-t" : "--test",
    "-l" : "--loop",
    "-h" : "--help",
    "-s" : "--switch"
}

from . import main as _main, REV_REGISTRY
from ._utils import print_logo
#_main(test="test_name", **args)
# returns True to continue loop

def main():
    test_name, args, loop_flag, switch_flag = _get_args()
    if test_name == "HELP":
        _print_help()
        return

    if test_name == "STOP":
        print("Try --help or -h for more information.")
        return
    
    if switch_flag:
        from ._utils import toggle_branches
        toggle_branches()
        return

    print_logo()
    if loop_flag:
        while _main(test=test_name, **args):
            pass
        return

    _main(test=test_name, **args)


import sys

def _get_args():
    argv = sys.argv[1:]

    # Expand shortcuts
    expanded = [shortcuts.get(arg, arg) for arg in argv]

    # Help check BEFORE parsing anything else
    if "--help" in expanded or "-h" in expanded:
        return "HELP", {}, False, False

    parsed = {}
    i = 0

    while i < len(expanded):
        arg = expanded[i]

        if arg not in cli_args:
            print(f"Unknown argument: {arg}")
            return "STOP", {}, False, False

        key = cli_args[arg]

        if key in ("loop", "switch"):
            parsed[key] = True
            i += 1
            continue

        if key == "help":
            return "HELP", {}, False, False

        # Flags requiring a value
        if i + 1 >= len(expanded):
            print(f"Flag {arg} requires a value.")
            return "STOP", {}, False, False

        parsed[key] = expanded[i + 1]
        i += 2

    test_name = parsed.get("test")

    args = {}
    for k, v in parsed.items():
        if k in ("test", "loop", "switch"):
            continue

        coerced = _coerce_value(k, v, test_name)
        if coerced is None:
            return "STOP", {}, False, False

        # Map internal key → actual argument name
        arg_name, _ = TESTS[test_name][1][k]
        args[arg_name] = coerced


    loop_flag = parsed.get("loop", False)
    switch_flag = parsed.get("switch", False)

    return test_name, args, loop_flag, switch_flag

def _infer_type_from_default(default):
    typ = type(default)

    if typ in (int, float, bool):
        return typ
    return str


def _coerce_value(key, value, test_name):
    if not test_name or test_name not in TESTS:
        return value

    _, options = TESTS[test_name]

    if key not in options:
        return value

    arg_name, default = options[key]
    expected_type = _infer_type_from_default(default)

    # Boolean coercion
    if expected_type is bool:
        v = value.lower()
        if v in ("1", "true", "yes", "y", "on"):
            return True
        if v in ("0", "false", "no", "n", "off"):
            return False
        print(f"Invalid boolean for --{key.replace('_','-')}: {value}")
        return None

    # Numeric coercion
    if expected_type in (int, float):
        try:
            return expected_type(value)
        except ValueError:
            print(f"Invalid {expected_type.__name__} for --{key.replace('_','-')}: {value}")
            return None

    # Default: string
    return value



def _print_help():
    print("Usage: fos-dev-test [options]\n")
    print("Global options:")
    print("  --test <name>       Select a test to run")
    print("  --loop              Repeat until test returns False")
    print("  --switch            Switch between main/dev feature branches")
    print("  --help, -h          Show this help message\n")
    print("  <no options>        Open UI Loop\n")

    print("Available tests:")
    for label, (test, options) in TESTS.items():
        print(f"  {label} ('{REV_REGISTRY[test]}')")
        for label, (opt,default) in options.items():
            flag = f"--{opt.replace('_', '-')}"
            typ = _infer_type_from_default(default)
            typename = (
                "bool" if typ is bool
                else typ.__name__
            )
            print(f"    {flag} <{typename}>   (default={default}) | {label}")
        print()

