
MD_PATHS = {
    "Code Example" : (
        "mkdocs/docs/examples/code_example/index.md",
        "mkdocs/docs/internal/copy_markdown/code_example.md",
    ),
    "Expected Properties" : (
        "mkdocs/docs/expected/index.md",
        "mkdocs/docs/internal/copy_markdown/expected.md",
    )
}

def copy_all():
    from pathlib import Path
    from ..._utils import ch2repo
    from .helpers import copy_md_code
    ch2repo()
    path_input = {k:(Path(src), Path(dest)) for k, (src, dest) in MD_PATHS.items()}
    for name, (src_path, dest_path) in path_input.items():
        copy_md_code(src_path, dest_path, name)