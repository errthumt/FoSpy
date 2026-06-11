from pathlib import Path

CODE_MD_PATH = Path("mkdocs/docs/examples/code_example/index.md")
CODE_SCRIPT_PATH = Path("mkdocs/fos_site/src/fos_site/run_example/extracted.py")
FULL_MD_PATH = Path("mkdocs/docs/examples/code_example/full.md")


def extract_and_run(figures=True):
    from .helpers import extract_code_to_main
    from .._utils import ch2repo
    import os
    ch2repo()

    extract_code_to_main(CODE_MD_PATH, CODE_SCRIPT_PATH, FULL_MD_PATH, figures=figures)

    from .extracted import main

    os.chdir("mkdocs/docs/examples")
    main()

    ch2repo()

    print("Example Code Finished!")

