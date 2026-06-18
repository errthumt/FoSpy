from FoSpy import Synthesis
import json

if __name__ == "__main__":
    from _utils import set_sandbox_cwd
    set_sandbox_cwd()
    empty_dict = Synthesis.reflex(serialize=True, include_temp_names=False, clean=True)

    with open("assets/empty_synthesis.json", "w") as f:
        json.dump(empty_dict, f, indent=4)