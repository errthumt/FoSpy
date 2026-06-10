import questionary

from . import (
    load_test,
    map_test
)

TESTS = {
    "Validate a Synthesis File": (
        load_test,{
            "Open Results?": ("open_result", False)
        }
    ),
    "Map a JSON to A Synthesis and Validate": (
        map_test,{
            "Open Results?": ("open_result", False),
            "Change Map Name": ("map_name", "default"),
            "Add New Map?": ("make_new", False),
            "Include Missing Values?": ("new_missing", False),
            "Set New Map As Default?": ("new_default", False)
        }
    )
}

import questionary

from ..config import values as cfg, save as cfg_save
from ._utils import run_interactive_batch
dev_cfg = cfg.DEV

def main(branch_batch=None):
    advanced = False

    while True:
        toggle_label = "[x] Advanced options" if advanced else "[ ] Advanced options"

        
        current_branch = dev_cfg.branch
        next_branch = "main" if current_branch == "dev" else "dev"

        branch_label = f"--Switch to {next_branch} branch (currently on {current_branch})--"


        choice = questionary.select(
            "Select a test to run:",
            choices=list(TESTS.keys()) + [
                questionary.Separator(),
                toggle_label,
                "Quit",
                questionary.Separator(),
                branch_label
            ]
        ).ask()

        if choice == branch_label:
            run_interactive_batch(branch_batch)
            dev_cfg.branch = next_branch
            cfg_save(prompt=False)
            continue

        if choice == toggle_label:
            advanced = not advanced
            continue

        if choice == "Quit":
            return

        test, options = TESTS[choice]

        if advanced:
            args = get_test_options(options, choice)
            if args == None:
                continue
            elif not args:
                return
            test.run(**args)
        else:
            test.run()

def get_test_options(options, choice_name):
    args = {o:v for o,v in options.values()}
    print(args)

    bools = [k for k,v in [(k,v[1]) for k,v in options.items()] if isinstance(v, bool)]
    strings = [k for k,v in [(k,v[1]) for k,v in options.items()] if isinstance(v, str)]

    toggles = { o:(f"[ ] {o}", f"[x] {o}") for o in bools }

    def update_string(args, choice):
        opt = options[choice][0]
        print(args[opt])
        args[opt] = questionary.text(f"{choice} (current: {args[opt]}): ").ask()
        print(args[opt])
        return args
    
    def update_bool(args, choice):
        opt = options[choice][0]
        print(args[opt])
        args[opt] = not args[opt]
        print(args[opt])
        return args
    
    exits = {
        "Run Test": lambda args: args,
        "Back": lambda args: None,
        "Quit": lambda args: False
    }

    while True:
        toggle_labels = { toggles[o][1] if args[options[o][0]] else toggles[o][0] : o for o in bools }
        string_labels = { f"{o}: ({args[options[o][0]]})" : o for o in strings }

        all_labels = {**toggle_labels, **string_labels}


        updates = {**{choice:update_bool for choice in toggle_labels.values()},
                   **{choice:update_string for choice in string_labels.values()}}

        choice = questionary.select(
            f"Additional Options for Test: {choice_name}",
            choices=[
                *all_labels,
                questionary.Separator(),
                *exits
            ]
        ).ask()

        if choice in exits:
            return exits[choice](args)

        choice = all_labels.get(choice, None)
        print(choice)
        args = updates.get(choice, lambda args, choice: args)(args, choice)


