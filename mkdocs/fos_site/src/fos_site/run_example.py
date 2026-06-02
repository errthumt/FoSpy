import re
from pathlib import Path

API_MD_PATH = Path("mkdocs/docs/examples/API_example/index.md")
API_SCRIPT_PATH = Path("mkdocs/build_scripts/API_example.py")
FULL_MD_PATH = Path("mkdocs/docs/examples/API_example/full.md")

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


def extract_and_run():
    from ._utils import ch2repo
    ch2repo()

    extract_code_to_main(API_MD_PATH, API_SCRIPT_PATH, FULL_MD_PATH)

    import os
    os.chdir(API_SCRIPT_PATH.parent)

    import API_example as example

    ch2repo()
    os.chdir(API_MD_PATH.parent.parent)
    example.main()

    ch2repo()

    print("Example Code Finished!")

