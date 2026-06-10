from pathlib import Path

EXAMPLE_DIR = Path("mkdocs/docs/examples")
SYN_DIR = EXAMPLE_DIR / "synthesis"
TPL_DIR = EXAMPLE_DIR / "templates"

PYPI_RM = EXAMPLE_DIR / "../../../PyPI/readme.md"

# Files to include at the top of each index
SYN_INIT_FILES = [
    ("Initial Synthesis (FOS)", SYN_DIR / "start_synthesis.fos"),
    ("Initial Synthesis (JSON)", SYN_DIR / "start_synthesis.json"),
]

TPL_INIT_FILES = [
    ("Initial Templates (FOS)", TPL_DIR / "start_templates.fos"),
]


def generate_fos_pages():
    from .helpers import generate_index, copy_fos_to_PyPI
    from .._utils import ch2repo
    ch2repo()
    generate_index(
        SYN_DIR,
        "Synthesis Examples",
        SYN_INIT_FILES,
        SYN_DIR,
    )

    generate_index(
        TPL_DIR,
        "Template Examples",
        TPL_INIT_FILES,
        TPL_DIR,
    )

    print("All example pages generated successfully.")

    print("Copying truncated example FOS to PyPI readme...")

    copy_fos_to_PyPI(fos_path=SYN_INIT_FILES[0][1], pypi_path=PYPI_RM)

    print("FOS copied to PyPI readme successfully.")





