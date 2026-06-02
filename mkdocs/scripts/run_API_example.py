import re
from pathlib import Path

BASE = Path(__file__).resolve().parent # mkdocs/scripts/
DOCS = BASE.parent / "docs" / "examples" / "API_example"

def extract_code_to_main(md_path, out_path, out_md_path):
    text = Path(md_path).read_text()

    pattern = re.compile(r"```python\s+(.*?)```", re.DOTALL | re.IGNORECASE)
    blocks = pattern.findall(text)
    combined = "\n\n".join(blocks).rstrip()
    indented = "\n".join("    " + line if line.strip() else "" for line in combined.splitlines())

    final_script = (
        "def main():\n"
        f"{indented}\n\n"
        "if __name__ == '__main__':\n"
        "    main()\n"
    )

    md_script = (
        "# Full Example Script\n\n"
        "Uninterrupted code extracted from the [API example walkthrough](./index.md).\n\n"
        "```python\n"
        f"{final_script}"
        "```"
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(final_script)
    out_md_path.parent.mkdir(parents=True, exist_ok=True)
    out_md_path.write_text(md_script)
    return out_path


def main():
    md_path = DOCS / "index.md"
    out_path = BASE / "API_example.py"
    out_md_path = DOCS / "full.md"

    extract_code_to_main(md_path, out_path, out_md_path)

    import os
    os.chdir(DOCS.parent)

    # Import dynamically
    import API_example as example
    example.main()

    print("Example Code Finished!")

if __name__ == "__main__":
    main()
