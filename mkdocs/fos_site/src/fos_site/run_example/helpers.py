import re
from pathlib import Path

def _extract_code(md_path, figures=True):
    text = Path(md_path).read_text()

    pattern = re.compile(r"```python\s+(.*?)```", re.DOTALL | re.IGNORECASE)
    blocks = pattern.findall(text)
    combined = "\n".join(blocks).rstrip()

    if not figures:
        lines = combined.splitlines()
        modified_lines = []
        for line in lines:
            try:
                if modified_lines[-1].strip().startswith("# optional: figure"):
                    modified_lines.append("# " + line)
                else:
                    modified_lines.append(line)
            except IndexError:
                modified_lines.append(line)

        combined = "\n".join(modified_lines)
    indented = "\n".join("    " + line if line.strip() else "" for line in combined.splitlines())
    return indented


def extract_code_to_main(md_path, out_path, out_md_path, figures=True):
    indented = _extract_code(md_path, figures)

    final_script = (
        "def main():\n"
        f"{indented}\n\n"
        "if __name__ == '__main__':\n"
        "    main()\n"
    )

    md_script = (
        "# Full Example Script\n\n"
        "Uninterrupted code extracted from the [code example](./index.md).\n\n"
        "```python\n"
        f"{final_script}"
        "```"
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(final_script)
    out_md_path.parent.mkdir(parents=True, exist_ok=True)
    out_md_path.write_text(md_script)
    return out_path

def extract_code_to_test(md_path, test_path, figures=False):
    indented = _extract_code(md_path, figures)

    final_script = (
        "def test_example(example_dir):\n"
        "    import os\n"
        "    os.chdir(example_dir)\n"
        f"{indented}\n\n"
    )

    test_path.parent.mkdir(parents=True, exist_ok=True)
    test_path.write_text(final_script)
    return test_path

def copy_start_fos(from_path, to_path):
    from_path.parent.mkdir(parents=True, exist_ok=True)
    to_path.parent.mkdir(parents=True, exist_ok=True)
    to_path.write_text(from_path.read_text())