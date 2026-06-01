import ast
from pathlib import Path
import textwrap

# -----------------------------
# CONFIGURATION
# -----------------------------
SOURCE_DIR = Path("src/FoSpy/blocks")
DOCS_DIR = Path("mkdocs/docs")
BLOCKS_DIR_NAME = "blocks"
OUTPUT_DIR = DOCS_DIR / BLOCKS_DIR_NAME
PACKAGE_ROOT = "FoSpy.blocks"
# -----------------------------


def get_all_symbols(py_file: Path) -> list[str]:
    """Parse __all__ from a module and return a list of symbol names."""
    tree = ast.parse(py_file.read_text(encoding="utf-8"))
    symbols: list[str] = []

    for node in tree.body:
        if isinstance(node, ast.Assign):
            # Look for __all__ = [...]
            targets = [t.id for t in node.targets if isinstance(t, ast.Name)]
            if "__all__" in targets and isinstance(node.value, (ast.List, ast.Tuple)):
                for elt in node.value.elts:
                    if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                        symbols.append(elt.value)
    return symbols


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    py_files = SOURCE_DIR.glob("*.py")
    paths = []
    for py_file in py_files:
        # Skip private modules and __init__.py
        if py_file.name.startswith("_") or py_file.name == "__init__.py":
            continue

        module_name = py_file.stem
        symbols = get_all_symbols(py_file)

        md_path = OUTPUT_DIR / f"{module_name}.md"
        with md_path.open("w", encoding="utf-8") as f:
            f.write(f"# {module_name.capitalize()}\n\n")

            attach_pre = """
                ## Methods attached to any object
                When [assigning an object as an
                attribute][FoSpy.blocks.blocks.SingleBlock.__setattr__],
                `SingleBlock`s attach special methods that are used to edit
                their own comment metadata.

                ---

                ### `add_comments(self_attr, *comments)`
                ::: FoSpy.blocks.blocks._add_comments_to_parent

                ---

                ### `clear_comments(self_attr)`
                ::: FoSpy.blocks.blocks._clear_comments_from_parent

                ---

                ## Block Types in this Module
                
            """

            f.write(textwrap.dedent(attach_pre).lstrip("\n"))

            if not symbols:
                # Fallback: no __all__ found, nothing to document explicitly
                f.write(f"::: {PACKAGE_ROOT}.{module_name}\n")
                f.write("    options:\n")
                f.write("        members: true\n")

            for sym in symbols:
                f.write("---\n")
                f.write(f"### `{sym}`\n")
                f.write(f"::: {PACKAGE_ROOT}.{module_name}.{sym}\n")

        paths.append(f"{BLOCKS_DIR_NAME}/{module_name}.md")

    print("Markdown stubs generated.")
    return paths


if __name__ == "__main__":
    print(main())
