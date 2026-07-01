from _utils import set_sandbox_cwd
from pathlib import Path
from FoSpy._docs.properties import write_prop_md
from FoSpy import Synthesis


def main():
    set_sandbox_cwd()

    MD_PATH = Path("expected.md")

    write_prop_md(MD_PATH)

    Synthesis.print_summary()

if __name__ == "__main__":
    main()
    pass

