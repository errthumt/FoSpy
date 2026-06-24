from pathlib import Path

CODE_MD_PATH = Path("mkdocs/docs/examples/code_example/index.md")
CODE_SCRIPT_PATH = Path("mkdocs/fos_site/src/fos_site/run_example/extracted.py")
FULL_MD_PATH = Path("mkdocs/docs/examples/code_example/full.md")
TEST_PATH = Path("tests/FoSpy/code_example/conftest.py")

TEST_STARTS = [(Path(from_path), Path(to_path)) for from_path, to_path in [
    ("mkdocs/docs/examples/synthesis/start_synthesis.fos", "tests/FoSpy/code_example/start_synthesis.fos"),
    ("mkdocs/docs/examples/templates/start_templates.fos", "tests/FoSpy/code_example/start_templates.fos"),
    ("mkdocs/docs/examples/templates/PY618_Ba8-Cu12-Zn12-As29,8.cif", "tests/FoSpy/code_example/PY618_Ba8-Cu12-Zn12-As29,8.cif"),
]]


def extract_and_run(figures=True):
    from .helpers import extract_code_to_main, extract_code_to_test, copy_start_fos
    from .._utils import ch2repo
    import os
    ch2repo()

    extract_code_to_main(CODE_MD_PATH, CODE_SCRIPT_PATH, FULL_MD_PATH, figures=figures)
    extract_code_to_test(CODE_MD_PATH, TEST_PATH)

    for from_path, to_path in TEST_STARTS:
        copy_start_fos(from_path, to_path)

    from .extracted import main

    os.chdir("mkdocs/docs/examples")
    main()

    ch2repo()

    print("Example Code Finished!")

