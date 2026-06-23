import pytest

@pytest.fixture(scope="module")
def example_dir(tmp_path_factory):
    from pathlib import Path
    import os

    current = Path(os.path.abspath(__file__)).parent

    copy_files = (
        ("start_synthesis.fos", "synthesis"),
        ("start_templates.fos", "templates"),
        ("PY618_Ba8-Cu12-Zn12-As29,8.cif", "templates"),
    )

    temp_dir = tmp_path_factory.mktemp("example_dir")

    for from_file, to_dir in copy_files:
        from_path = current / from_file

        to_path = temp_dir / to_dir / from_file

        to_path.parent.mkdir(parents=True, exist_ok=True)

        to_path.write_text(from_path.read_text())

    return temp_dir