from ..json.core import map_to_fos
from ._utils import file_prompt
from . import load_test

import tempfile, json

from pathlib import Path
import json

def run(filepath=None, map_name=None):
    if filepath is None:
        filepath = file_prompt(
            title="Select a .json input file to be mapped.",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

    mapped_dict = map_to_fos(filepath=filepath, map_name=map_name)

    filename = Path(filepath).stem

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir) / f"{filename}_maptest.json"
        with open(tmp_path, "w") as f:
            json.dump(mapped_dict, f, indent=4)

        load_test.run(str(tmp_path))
