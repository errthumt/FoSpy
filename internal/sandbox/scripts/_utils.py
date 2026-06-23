def set_sandbox_cwd():
    import os
    from pathlib import Path
    sandbox = Path(os.path.dirname(os.path.abspath(__file__))) / ".."

    os.chdir(sandbox)