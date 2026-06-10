
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

def copy_fos_to_PyPI(fos_path: Path, pypi_path: Path):
    from FoSpy import Synthesis, cfg
    from FoSpy.parsing import write
    import tempfile
    from pathlib import Path

    cfg.track_attachments.ignore=True

    my_synth = Synthesis.fromFile(fos_path)
    my_synth.materials.remove_idx(from_idx=1)
    my_synth.treatments = []
    my_synth.cifs[0].embedded = ["Embedded CIF Test Goes Here\n"]
    my_synth.cifs.insert(0, {
        "file_name": "attached_cif",
        "extension": ".cif",
        "path": "./projects/my_cifs"
    })

    # write to temporary file
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp) / "synthesis.fos"
        my_synth.save(str(tmp_path))

        fos_text = tmp_path.read_text(encoding="utf-8")

    original = pypi_path.read_text(encoding="utf-8").splitlines()
    
    heading = "## A Simple FOS File"
    try:
        idx = next(i for i, line in enumerate(original) if line.strip() == heading)
    except StopIteration:
        raise ValueError(f"Heading '{heading}' not found in {pypi_path}")
    
    new_lines = original[:idx+1]

    new_lines.append("")
    new_lines.append("```fos")
    new_lines.append(fos_text.rstrip("\n"))
    new_lines.append("```")
    new_lines.append("")

    # Write back
    pypi_path.write_text("\n".join(new_lines), encoding="utf-8")

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