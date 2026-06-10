from ..json.core import map_to_fos, new_map
from ._utils import file_prompt
from . import load_test

import tempfile, json

from pathlib import Path
import json

def run(filepath=None, map_name=None, make_new=False, new_missing=False, new_default=False, open_result=False):
    if filepath is None:
        filepath = file_prompt(
            title="Select a .json input file to be mapped.",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

    if make_new:
        map_path = file_prompt(
            title="Select a new .json map file.",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        
        missing_path = None
        if new_missing:
            missing_path = file_prompt(
                title="Select a new .json missing values file.",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        
        new_map(filepath=map_path, map_name=map_name, missing_path=missing_path, set_default=new_default)

    elif map_name not in (None, "default") and new_default:
        from ..config import values as cfg, save as cfg_save
        cfg.default = map_name
        cfg_save(prompt=False)

    mapped_dict = map_to_fos(filepath=filepath, map_name=map_name)

    filename = Path(filepath).stem

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir) / f"{filename}_maptest.json"
        with open(tmp_path, "w") as f:
            json.dump(mapped_dict, f, indent=4)

        load_test.run(str(tmp_path), open_result=open_result)
