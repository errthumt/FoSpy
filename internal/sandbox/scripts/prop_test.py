from _utils import set_sandbox_cwd
from pathlib import Path
from FoSpy._docs.properties import write_prop_md


def main():
    set_sandbox_cwd()

    MD_PATH = Path("expected.md")

    write_prop_md(MD_PATH)

if __name__ == "__main__":
    main()

