import yaml
from pathlib import Path

import block_stubs
import full_stubs

NAV_HEADER_PATH = Path("mkdocs/nav_header.yml")
NAV_OUTPUT_PATH = Path("mkdocs/nav.yml")


def build_full_nav(tree: dict) -> list:
    """
    Convert nested dict structure from full_stubs into MkDocs nav list.
    Produces ONLY {name: path} or {folder: [...]}, never bare paths.
    """
    nav_list = []

    # Files directly in this folder: "." maps to {page_name: path}
    files = tree.get(".", {})
    file_items = list(files.items())  # [(page_name, path), ...]

    # Subfolders
    subfolders = [(k, v) for k, v in tree.items() if k != "."]

    # Case 1: folder contains exactly one file and no subfolders → collapse
    if len(file_items) == 1 and not subfolders:
        page_name, path = file_items[0]
        nav_list.append({page_name: path})
        return nav_list

    # Case 2: normal folder → list files first
    for page_name, path in file_items:
        nav_list.append({page_name: path})

    # Then subfolders
    for key, subtree in subfolders:
        subnav = build_full_nav(subtree)

        # Collapse subfolder if it contains exactly one {name: path}
        if len(subnav) == 1 and isinstance(subnav[0], dict):
            nav_list.append({key: subnav[0]})
        else:
            nav_list.append({key: subnav})

    return nav_list



def main():
    import os
    os.chdir(Path(__file__).parent.parent.parent)

    # 1. Run stub generators
    block_paths = block_stubs.main()      # list[str]
    full_tree = full_stubs.main()         # nested dict

    # 2. Load nav header
    with NAV_HEADER_PATH.open("r", encoding="utf-8") as f:
        nav_header = yaml.safe_load(f)

    # 3. Build Block Modules section
    block_section = {
        "Block Modules": block_paths
    }

    # 4. Build Full Documentation section
    full_section = {
        "Full Documentation": build_full_nav(full_tree)
    }

    # 5. Combine everything
    nav = nav_header + [block_section, full_section]

    # 6. Write mkdocs/nav.yml
    with NAV_OUTPUT_PATH.open("w", encoding="utf-8") as f:
        yaml.dump({"nav": nav}, f, sort_keys=False)

    print("mkdocs/nav.yml generated.")


if __name__ == "__main__":
    main()
