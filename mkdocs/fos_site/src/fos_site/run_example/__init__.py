from pathlib import Path

API_MD_PATH = Path("mkdocs/docs/examples/API_example/index.md")
API_SCRIPT_PATH = Path("mkdocs/build_scripts/API_example.py")
FULL_MD_PATH = Path("mkdocs/docs/examples/API_example/full.md")


def extract_and_run(figures=True):
    from .helpers import extract_code_to_main
    from .._utils import ch2repo
    ch2repo()

    extract_code_to_main(API_MD_PATH, API_SCRIPT_PATH, FULL_MD_PATH, figures=figures)

    import os
    os.chdir(API_SCRIPT_PATH.parent)

    import API_example as example

    ch2repo()
    os.chdir(API_MD_PATH.parent.parent)
    example.main()

    ch2repo()

    print("Example Code Finished!")

