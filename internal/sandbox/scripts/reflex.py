from FoSpy import Synthesis
from FoSpy.json.help import generate_map_guide
import json

if __name__ == "__main__":
    from _utils import set_sandbox_cwd
    set_sandbox_cwd()
    empty_dict = Synthesis.reflex(serialize=True, include_temp_names=False, clean=True)

    with open("assets/empty_synthesis.json", "w") as f:
        json.dump(empty_dict, f, indent=4)

    guides = {
        "simple": generate_map_guide(),
        "full": generate_map_guide(include_optional=True)
    }

    for name, dct in guides.items():
        with open(f"assets/guides/{name}.json", "w") as f:
            json.dump(dct, f, indent=4)
