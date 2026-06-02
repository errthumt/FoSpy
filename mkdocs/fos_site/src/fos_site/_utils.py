def ch2repo():
    import subprocess, os
    repo_root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
    os.chdir(repo_root)