import re
from pathlib import Path

def extract_code_to_main(md_path, out_path):
    text = Path(md_path).read_text()

    # Capture ANY fenced code block: ```...```
    pattern = re.compile(
    r"```python\s+(.*?)```",
    re.DOTALL | re.IGNORECASE
    )


    blocks = pattern.findall(text)

    # Combine blocks with blank lines between them
    combined = "\n\n".join(blocks).rstrip()

    # Indent all lines for main()
    indented = "\n".join("    " + line if line.strip() else "" for line in combined.splitlines())

    final_script = (
        "def main():\n"
        f"{indented}\n\n"
        "if __name__ == '__main__':\n"
        "    main()\n"
    )

    Path(out_path).write_text(final_script)
    return out_path


if __name__ == "__main__":
    # extract code from the readme and write it to example.py, then run example.py
    md_path = "example/readme.md"
    out_path = "example/example.py"

    extract_code_to_main(md_path, out_path)
    from example import main
    main()

    print("Example Code Finished!")