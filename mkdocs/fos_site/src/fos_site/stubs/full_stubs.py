import os
from pathlib import Path
from textwrap import dedent

# ---------------------------------------
# CONFIGURATION
# ---------------------------------------
SOURCE_ROOT = Path("src/FoSpy")
DOCS_ROOT = Path("mkdocs/docs")
FULL_DIR_NAME = "full"
OUTPUT_ROOT = DOCS_ROOT / FULL_DIR_NAME
PACKAGE_ROOT = "FoSpy"
# ---------------------------------------


def module_path_from_file(py_file: Path) -> str:
    """
    Convert a file path like src/FoSpy/a/b/c.py
    into a dotted module path FoSpy.a.b.c
    """
    rel = py_file.relative_to(SOURCE_ROOT)
    parts = rel.with_suffix("").parts
    return ".".join((PACKAGE_ROOT, *parts))


def ensure_folder(tree: dict, parts: list[str]) -> dict:
    """
    Walk/create nested folder dictionaries.
    Returns the dictionary corresponding to the deepest folder.
    """
    current = tree
    for part in parts:
        if part not in current:
            current[part] = {".": {}}
        current = current[part]
    return current

def sort_tree(tree: dict) -> dict:
    """
    Recursively sort a nested dictionary by keys.
    """
    sorted_tree = {}
    for key in sorted(tree.keys()):
        if isinstance(tree[key], dict):
            sorted_tree[key] = sort_tree(tree[key])
        else:
            sorted_tree[key] = tree[key]
    return sorted_tree

def main():
    paths: dict[str, dict] = {".": {}}

    for py_file in SOURCE_ROOT.rglob("*.py"):

        if py_file.name == "__init__.py":
            continue

        dotted = module_path_from_file(py_file)

        rel_dir = py_file.parent.relative_to(SOURCE_ROOT)
        out_dir = OUTPUT_ROOT / rel_dir
        out_dir.mkdir(parents=True, exist_ok=True)

        md_path = out_dir / f"{py_file.stem}.md"
        nav_path = md_path.relative_to(DOCS_ROOT).as_posix()  # e.g. "full/blocks/a.md"

        # Strip leading "full/"
        rel = nav_path.split("/", 1)[1] if nav_path.startswith(FULL_DIR_NAME + "/") else nav_path

        # Split into folder parts + filename
        parts = rel.split("/")
        folders, filename = parts[:-1], parts[-1]

        # Insert into nested dictionary
        folder_dict = ensure_folder(paths, folders)
        folder_dict["."][py_file.stem] = nav_path

        # Write stub
        with md_path.open("w", encoding="utf-8") as f:
            f.write(dedent("""
                    Full documentation pages are generated for docstring
                    reference only and may contain symbols imported from other
                    modules. Imported symbols are not distinguished from locally
                    defined symbols and will appear in any module that they are
                    imported into. For better information on where symbols should
                    be imported from, [review the sourcecode on the
                    github.](https://github.com/errthumt/FoSpy/tree/main/src/FoSpy)\n\n
                    """))
            f.write(f"::: {dotted}\n")
            f.write("    options:\n")
            f.write("        members: true\n")
            f.write("        show_if_no_docstring: true\n")
            f.write("        show_root_heading: true\n")
            f.write("        heading_level: 2\n")
            f.write("        show_source: true\n")
            f.write("        separate_signature: true\n")

    paths = sort_tree(paths)
    root = {"Full Docs Home": "full/index.md"}
    root.update(paths["."])
    paths["."] = root

    return paths

if __name__ == "__main__":
    print(main())
