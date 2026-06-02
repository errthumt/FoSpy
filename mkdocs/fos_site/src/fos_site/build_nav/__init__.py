import yaml
from pathlib import Path

NAV_HEADER_PATH = Path("mkdocs/nav_header.yml")
NAV_OUTPUT_PATH = Path("mkdocs/nav.yml")


def main():
    from stubs import block_stubs, full_stubs
    from .helpers import build_full_nav
    from .._utils import ch2repo
    ch2repo()

    # 1. Run stub generators
    block_paths = block_stubs.make_stubs()      # list[str]
    full_tree = full_stubs.make_stubs()

    block_tree = {".": block_paths}

    # 2. Load nav header
    with NAV_HEADER_PATH.open("r", encoding="utf-8") as f:
        nav_header = yaml.safe_load(f)

    # 3. Build Block Modules section
    block_section = {
        "Block Modules": helpers(block_tree)
    }

    # 4. Build Full Documentation section
    full_section = {
        "Full Documentation": helpers(full_tree)
    }

    # 5. Combine everything
    nav = nav_header + [block_section, full_section]

    # 6. Write mkdocs/nav.yml
    with NAV_OUTPUT_PATH.open("w", encoding="utf-8") as f:
        yaml.dump({"nav": nav}, f, sort_keys=False)

    print("mkdocs/nav.yml generated.")

