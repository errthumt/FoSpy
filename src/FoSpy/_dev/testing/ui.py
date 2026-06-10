
def get_test(**args):
    import questionary
    from . import TESTS
    from ...config import values as cfg
    from ._utils import toggle_branches, get_current_branch

    cfg.DEV.branch = get_current_branch()

    show_advanced = args == {}
    advanced = False

    while True:
        current_branch = cfg.DEV.branch
        next_branch = "main" if current_branch == "dev" else "dev"
        branch_label = f"[Switch to {next_branch} feature branch (currently on {current_branch})]"

        choices = {}

        for name, (test, options) in TESTS.items():
            if advanced:
                choices[name] = _get_opts_and_run(test, options, name)
            elif not args:
                choices[name] = test.run
            else:
                def try_test(t=test, a=args):
                    try:
                        t.run(**a)
                    except Exception as e:
                        print("Failed to run test with provided arguments", e)

                choices[name] = try_test
        
        choices[questionary.Separator()] = None
        
        if show_advanced:
            advanced_label = "[x] Advanced options" if advanced else "[ ] Advanced options"
            choices[advanced_label] = "toggle_advanced"

        choices["[Quit]"] = False
        choices[branch_label] = toggle_branches

        label = questionary.select(
            "Select a test to run:",
            choices=list(choices.keys())
        ).ask()

        selection = choices[label]

        if selection == "toggle_advanced":
            advanced = not advanced
            continue

        elif callable(selection):
            out = selection()
            if out is None:
                continue
            return out

        else:
            return selection


def _get_opts_and_run(test, options, choice_name):
    def func():
        args = get_options(options, choice_name)
        if not args:
            return args
        test.run(**args)
    
    return func

def get_options(options, choice_name):
    import questionary
    args = {o:v for o,v in options.values()}

    bools = [k for k,v in [(k,v[1]) for k,v in options.items()] if isinstance(v, bool)]
    strings = [k for k,v in [(k,v[1]) for k,v in options.items()] if isinstance(v, str)]

    toggles = { o:(f"[ ] {o}", f"[x] {o}") for o in bools }

    def update_string(args, choice):
        opt = options[choice][0]

        args[opt] = questionary.text(f"{choice} (current: {args[opt]}): ").ask()

        return args
    
    def update_bool(args, choice):
        opt = options[choice][0]

        args[opt] = not args[opt]

        return args
    
    exits = {
        "[Run Test]": lambda args: args,
        "[Back]": lambda args: None,
        "[Quit]": lambda args: False
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