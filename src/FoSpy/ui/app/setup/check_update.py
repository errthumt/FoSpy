import subprocess
import sys
from pathlib import Path


def update(source="FoSpy", dependencies=False, executable=None, cmd_only=False):
    if executable is None:
        executable = sys.executable

    if "win" in sys.platform.lower():
        version_override = "set SETUPTOOLS_SCM_PRETEND_VERSION=0.0.1.dev00+000000 && "
        app_executable = (Path(executable).parent / "fospy-app.exe").resolve()
    else:
        version_override = "SETUPTOOLS_SCM_PRETEND_VERSION=0.0.1.dev00+000000 && "
        app_executable = (Path(executable).parent / "fospy-app").resolve()

    # Build the pip install command
    install_cmd = f'"{executable}" -m pip install --upgrade --force-reinstall'
    if not dependencies:
        install_cmd += " --no-deps"
    else:
        pass#source += "[app]"
    install_cmd += f" {source}"

    if source != "FoSpy":
        install_cmd = version_override + install_cmd

    # Full chained command
    cmd = (
        f'"{executable}" -m pip cache purge'
        f' && {install_cmd}'
        f' && "{app_executable}"'
    )

    if cmd_only:
        return cmd

    subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        shell=True,
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )


def update_from_github(branch="main", dependencies=False, executable=None, cmd_only=False):
    url = f'"https://github.com/errthumt/FoSpy/archive/refs/heads/{branch}.zip"'

    return update(source=url, dependencies=dependencies, executable=executable, cmd_only=cmd_only)

def update_dlg(window, github=False):
    update_func = update_from_github if github else update

    options = {
        "Update Dependencies?": {
            "Yes": True,
            "No": False
        }
    }
    description = (
        "Please select options for update.\n\n"
        "Your Python pip cache will be cleared before update. "
        "If updating dependencies, all required packages will be reinstalled, "
        "even if they do not require updates.\n\n"
        "Otherwise, only FoSpy will be updated."
    )

    if github:
        options["GitHub Branch"] = [
            "main",
            "dev"
        ]

        description += ("\n\n"
            "Warning: Updates from the GitHub may be unstable. Some unstable updates may require a complete reinstall.")

    results = window._get_text_inputs(
        "Update FoSpy", description, **options
    )

    if not results:
        return

    confirm = window._custom_popup(
        "Confirm FoSpy Update",
        "Are you sure you want to update FoSpy? This will restart "
        "the application and you will lose any unsaved work.",
        cancel=True
    )

    if not confirm:
        return

    kwargs = {
        "dependencies": results["Update Dependencies?"],
        "branch": results.get("GitHub Branch", None)
    }

    update_func(**kwargs)

    window.close()


