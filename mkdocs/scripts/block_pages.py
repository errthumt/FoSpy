import os
from pathlib import Path

# -----------------------------
# CONFIGURATION
# -----------------------------
SOURCE_DIR = Path("src/FoSpy/blocks")
OUTPUT_DIR = Path("mkdocs/docs/Block_Modules")
PACKAGE_ROOT = "FoSpy.blocks"
# -----------------------------


def main():
    for py_file in SOURCE_DIR.glob("*.py"):

        if py_file.name.startswith("_"):
            continue

        module_name = py_file.stem  # submodule name without .py
        md_path = OUTPUT_DIR / f"{module_name}.md"
        md_path.parent.mkdir(parents=True, exist_ok=True)

        with md_path.open("w", encoding="utf-8") as f:
            f.write(f"# {module_name.capitalize()}\n")
            f.write(f"::: {PACKAGE_ROOT}.{module_name}\n")
            f.write("    options:\n")
            f.write("        members: true\n")

    print("Markdown stubs generated.")


if __name__ == "__main__":
    main()
