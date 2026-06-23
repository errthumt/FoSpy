import os
from ._utils import dir_prompt, get_current_branch
from ...json.help import generate_map_guide

from pathlib import Path
import json
from textwrap import dedent

SUB_DIR = "FoSpy_Map_Guides"

EXPECTED_FN = "optional_fields"
REQUIRED_FN = "required_fields"

def run(dirpath=None, open_result=True):
    if dirpath is None:
        try:
            dirpath = dir_prompt(title="Select a folder to save the map guides to.")
        except Exception:
            print("Failed to select directory. Aborting...")
            return

    
        
    outdir = Path(dirpath) / SUB_DIR

    if str(dirpath).endswith(SUB_DIR):
        outdir = outdir.parent
    
    os.makedirs(outdir, exist_ok=True)

    guides = {
        EXPECTED_FN: generate_map_guide(include_optional=True),
        REQUIRED_FN: generate_map_guide(include_optional=False)
    }

    for name, guide in guides.items():
        with open(outdir / f"{name}.json", "w") as f:
            json.dump(guide, f, indent=4)

    readme = dedent(f"""
    # FoSpy Map Guides

    This folder contains guide files for creating JSON maps FoSpy. Consult
    https://errthumt.github.io/FoSpy/incoming/guides/maps for more information. The
    documentation site has similar guide files, but the guide files generated here
    are up-to-date with the version of FoSpy you were using at the time of
    generation ({get_current_branch()} branch). This may be different than the version used to generate the guide
    files on the website.
    """)

    with open(outdir / "README.txt", "w") as f:
        f.write(readme)

    if open_result:
        os.startfile(outdir)