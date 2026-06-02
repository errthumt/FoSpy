
from pathlib import Path
def read_file_safely(path: Path) -> str:
    """Return file contents or a placeholder if missing."""
    if not path.exists():
        return f"# File not found: {path}"
    return path.read_text()


def write_header_and_preamble(f, title: str):
    f.write(f"# {title}\n\n")
    f.write("Each file on this page was generated at the corresponding checkpoint in the [walkthrough](../API_example/index.md) script.\n\n")
    f.write("---\n\n")


def write_code_block(f, header: str, content: str, lang="fos"):
    f.write(f"## {header}\n\n")
    f.write(f"```{lang}\n")
    f.write(content)
    f.write("\n```\n\n")


def add_initial_files(f, file_specs):
    for header, path in file_specs:
        content = read_file_safely(path)
        # detect language
        lang = "json" if path.suffix == ".json" else "fos"
        write_code_block(f, header, content, lang=lang)


def add_checkpoints(f, folder: Path):
    for file in sorted(folder.glob("check*.fos")):
        check_num = int(file.stem.split("check")[1])
        header = f"Checkpoint {check_num}"
        content = read_file_safely(file)
        write_code_block(f, header, content, lang="fos")


# ------------------------------------------------------------
# Main generation logic
# ------------------------------------------------------------

def generate_index(folder: Path, title: str, init_files, source_folder: Path):
    folder.mkdir(parents=True, exist_ok=True)
    index_path = folder / "index.md"

    with index_path.open("w", encoding="utf-8") as f:
        write_header_and_preamble(f, title)
        add_initial_files(f, init_files)
        add_checkpoints(f, source_folder)

    print(f"Generated: {index_path}")