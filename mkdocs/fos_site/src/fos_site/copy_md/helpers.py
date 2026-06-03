from pathlib import Path
import os

def copy_md_code(src_path:Path, dest_path:Path, site_name:str):
    """Copy a markdown document as a fenced code block in a new file."""
    src_text = src_path.read_text()
    dest_text = (
        f"# {site_name}: Raw Code\n\n"
        f"There is a copy button in the top right of the code block.\n\n"
        f"[Click here to go to the rendered version]({os.path.relpath(src_path, dest_path.parent)})\n\n"
        f"````markdown\n"
        f"{src_text}\n"
        f"````\n"
    )

    dest_path.write_text(dest_text)