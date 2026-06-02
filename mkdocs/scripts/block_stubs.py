import ast
from pathlib import Path
import textwrap

# -----------------------------
# CONFIGURATION
# -----------------------------
SYMBOL_LIST_NAME = "__block_classes__"
SOURCE_DIR = Path("src/FoSpy/blocks")
DOCS_DIR = Path("mkdocs/docs")
BLOCKS_DIR_NAME = "blocks"
OUTPUT_DIR = DOCS_DIR / BLOCKS_DIR_NAME
PACKAGE_ROOT = "FoSpy.blocks"
# -----------------------------


def get_all_symbols(py_file: Path, list_name: str = SYMBOL_LIST_NAME) -> list[str]:
    """
    Parse a custom symbol list (e.g. __doc_classes__) from a module
    and return a list of symbol names.
    """
    tree = ast.parse(py_file.read_text(encoding="utf-8"))
    symbols: list[str] = []

    for node in tree.body:
        if isinstance(node, ast.Assign):
            # Look for list_name = [...]
            targets = [t.id for t in node.targets if isinstance(t, ast.Name)]
            if list_name in targets and isinstance(node.value, (ast.List, ast.Tuple)):
                for elt in node.value.elts:
                    if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                        symbols.append(elt.value)

    return symbols



def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    py_files = SOURCE_DIR.glob("*.py")
    paths = {}
    for py_file in py_files:
        # Skip private modules and __init__.py
        if py_file.name.startswith("_") or py_file.name == "__init__.py":
            continue

        module_name = py_file.stem
        symbols = get_all_symbols(py_file)

        md_path = OUTPUT_DIR / f"{module_name}.md"
        with md_path.open("w", encoding="utf-8") as f:
            f.write(f"# `FoSpy.blocks.{module_name}`\n\n")

            attach_pre = """

                This site only contains documentation for the
                [`Block`][FoSpy.blocks.blocks.Block] subclasses defined in this
                module, not the entire module API. For a complete reference of
                all functions, classes, and variables, see the [full API
                documentation](../full/index.md).

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
                f.write("    options:\n")
                f.write("        show_if_no_docstring: true\n")

        paths[module_name] = f"{BLOCKS_DIR_NAME}/{module_name}.md"

    print("Markdown stubs generated.")

    out = {"What is a Block?": "blocks/index.md"}

    for k, v in sorted(paths.items()):
        out[k] = v

    return out


if __name__ == "__main__":
    print(main())
