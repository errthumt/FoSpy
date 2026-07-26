import subprocess
import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)


def update(source="FoSpy", dependencies=False, executable=None, cmd_only=False):
    if executable is None:
        executable = sys.executable

    if "win" in sys.platform.lower():
        app_executable = (Path(executable).parent / "fospy-app.exe").resolve()
    else:
        app_executable = (Path(executable).parent / "fospy-app").resolve()

    # Build the pip install command
    install_cmd = f'"{executable}" -m pip install --upgrade --force-reinstall'
    if not dependencies:
        install_cmd += " --no-deps"
    elif source=="FoSpy":
        source += "[app]"
    else:
        source = f'"FoSpy[app] @ {source}"'
    install_cmd += f" {source}"

    # Full chained command
    cmd = (
        f'echo Clearing pip cache... '
        f'&& "{executable}" -m pip cache purge '
        f'&& echo( && echo Installing from: {source} '
        f'&& {install_cmd} '
        f'&& echo( && echo Restarting FoSpy... '
        f'&& "{app_executable}"'
    )

    if cmd_only:
        return cmd

    run_detached_in_new_window(cmd)

def update_dlg(window):
    dlg = UpdateFoSpyDialog(parent=window)

    if not dlg.exec():
        return

    dependencies, github, branch = dlg.get_values()

    if github:
        source = f"git+https://github.com/errthumt/FoSpy.git@{branch}"
    else:
        source = "FoSpy"

    update(source=source, dependencies=dependencies)

    window.close()


def git_available():
    import shutil
    return shutil.which("git") is not None


class UpdateFoSpyDialog(QDialog):
    def __init__(self, branches=("main", "dev"), parent=None, new=False):
        super().__init__(parent)
        self.setWindowTitle("Update FoSpy")

        root = QVBoxLayout(self)
        if not new:
            desc = QLabel(
                "Please select options for update.\n\n"
                "This app will be closed and restarted after update. If necessary, cancel this dialog and save your work before updating.\n\n"
                "This dialog can be accessed again from the Menu via:\nApp > Update FoSpy.\n\n"
                "Please note that Python's pip cache will be cleared before updating."
            )
        else:
            desc = QLabel(
                "Please select FoSpy install options.\n\n"
                "Please not that Python's pip cache will be cleared before installing."
            )

        root.addWidget(desc)

        self.rb_with_deps = QRadioButton("Update/Reinstall all dependencies.")
        self.rb_without_deps = QRadioButton("Update FoSpy only.")

        if new:
            self.rb_with_deps.setChecked(True)

        else:
            self.rb_without_deps.setChecked(True)
            # --- Update mode group ---
            mode_group = QGroupBox("Update/Reinstall Dependencies (numpy, pandas, etc)?")
            mode_layout = QVBoxLayout(mode_group)


            mode_layout.addWidget(self.rb_with_deps)
            mode_layout.addWidget(self.rb_without_deps)

            root.addWidget(mode_group)


        self.rb_pypi = QRadioButton("PyPI")
        self.rb_github = QRadioButton("GitHub")

        self.rb_pypi.setChecked(True)
        # Only show GitHub option if git is available
        if git_available():
            self.rb_github.clicked.connect(self.select_github)
            self.rb_pypi.clicked.connect(self.select_pypi)

            # --- Source group ---
            source_group = QGroupBox("Update Source")
            source_layout = QVBoxLayout(source_group)
            source_layout.addWidget(self.rb_pypi)
            source_layout.addWidget(self.rb_github)
            self.gh_label = QLabel(
                "Please note that GitHub updates may be unstable. A complete "
                "reinstall is recommended for returning from a GitHub build to "
                "a stable release.")
            self.gh_label.setVisible(False)
            root.addWidget(source_group)

        else:
            self.gh_label = QLabel("Tip: Once <a href='https://git-scm.com/'>Git</a> is installed, you can update directly from GitHub using this menu.")


        # --- Branch selection (hidden unless GitHub selected) ---
        self.branch_container = QWidget()
        branch_layout = QHBoxLayout(self.branch_container)
        branch_layout.setContentsMargins(0, 0, 0, 0)

        branch_layout.addWidget(QLabel("GitHub Branch:"))
        self.branch_combo = QComboBox()
        self.branch_combo.addItems(branches)
        branch_layout.addWidget(self.branch_combo)

        # Initially hidden unless GitHub is selected
        self.branch_container.setVisible(False)
        root.addWidget(self.branch_container)

        root.addWidget(self.gh_label)

        # --- OK / Cancel ---
        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        root.addWidget(btns)


        self.setWindowModality(Qt.ApplicationModal)
        self.raise_()
        self.activateWindow()
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        if new and not git_available():
            self.accept()

    def get_values(self):
        dependencies = self.rb_with_deps.isChecked()
        github = not self.rb_pypi.isChecked()
        branch = self.branch_combo.currentText() if github else None
        return dependencies, github, branch

    def select_github(self, *_):
        self.gh_label.setVisible(True)
        self.branch_container.setVisible(True)

    def select_pypi(self, *_):
        self.gh_label.setVisible(False)
        self.branch_container.setVisible(False)

def run_detached_in_new_window(cmd_str: str):
    """
    Executes a chained command string in a single new terminal window,
    completely detached from the calling Python process.
    """
    system = sys.platform

    if system == "win32":
        # Windows: Use CREATE_NEW_CONSOLE with cmd.exe
        subprocess.Popen(
            f'cmd.exe /k "{cmd_str}"',
            creationflags=subprocess.CREATE_NEW_CONSOLE,
            close_fds=True
        )

    elif system == "darwin":
        # macOS: Use AppleScript to open a new Terminal window and run the command
        # Escaping quotes for AppleScript
        escaped_cmd = cmd_str.replace('\\', '\\\\').replace('"', '\\"')
        applescript = f'tell application "Terminal" to do script "{escaped_cmd}"'
        
        subprocess.Popen(
            ["osascript", "-e", applescript],
            start_new_session=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    else:
        # Linux / Unix: Try common terminal emulators
        # x-terminal-emulator, gnome-terminal, konsole, or xterm
        terminals = [
            ["x-terminal-emulator", "-e", f"bash -c '{cmd_str}'"],
            ["gnome-terminal", "--", "bash", "-c", cmd_str],
            ["konsole", "-e", "bash", "-c", cmd_str],
            ["xterm", "-e", f"bash -c '{cmd_str}'"]
        ]

        launched = False
        for term_args in terminals:
            try:
                subprocess.Popen(
                    term_args,
                    start_new_session=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                launched = True
                break
            except FileNotFoundError:
                continue

        if not launched:
            raise RuntimeError("Could not find a supported terminal emulator (x-terminal-emulator, gnome-terminal, etc.).")


def _load_current():
    frozen_txt = subprocess.check_output(["pip", "freeze"], text=True)
    return _load_packages(frozen_txt)


def _load_compatible(path):
    frozen_txt = path.read_text()
    return _load_packages(frozen_txt)


def check_for_incompatible():
    from FoSpy.ui.app._utils import ASSETS
    frozen = _load_current()
    compatible = _load_compatible(ASSETS["compatible packages"])

    incompatible = set(frozen.keys()) - set(compatible.keys())
    incompatible = {name: frozen[name] for name in incompatible}
    incompatible.pop("fospy", None)

    return incompatible


def check_env(win):
    from ...config import values as cfg

    checked = cfg.APP.startup_checks.get("env", False)
    if checked:
        return

    incompatible = check_for_incompatible()
    if not incompatible:
        return

    summary_strings = [f"{name}=={ver}" for name, ver in incompatible.items()]

    if len(incompatible) > 9:
        summary_strings = summary_strings[:9]
        summary_strings.append(f"and {len(incompatible) - 9} more...")

    summary = "\n".join(summary_strings)

    confirm = win._custom_popup(
        "Additional Packages Detected",
        "It is recommended to install the FoSpy GUI in a dedicated virtual environment.\n"
        "The following packages are unexpected for FoSpy and suggest you may be using FoSpy in a shared environment:\n\n"
        f"{summary}\n\n"
        "Would you like to reinstall FoSpy in a fresh virtual environment?",
        ("Yes", True),
        ("No", False),
        ("No, and don't ask again", None),
        cancel=False
    )

    if confirm is None:
        cfg.APP.startup_checks.env = True
        cfg.APP.startup_checks.save()

    if not confirm:
        return

    import sys
    from pathlib import Path

    from PySide6.QtWidgets import QFileDialog

    from .check_update import UpdateFoSpyDialog, run_detached_in_new_window, update

    new_venv = QFileDialog.getExistingDirectory(
        win,
        "Select Folder for New FoSpy Environment", "",
        QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)

    new_venv = Path(new_venv) / ".venv_FoSpy"
    new_venv = new_venv.resolve()

    cmd = (
        'echo Setting up new virtual environment at: && '
        f'echo {new_venv} && '
        f'"{sys.executable}" -m venv "{new_venv}" && '
        'echo( && '
    )

    if "win" in sys.platform.lower():
        new_executable = new_venv / "Scripts" / "python.exe"
    else:
        new_executable = new_venv / "bin" / "python"

    new_executable = new_executable.resolve()


    update_dlg = UpdateFoSpyDialog(parent=win, new=True)

    if not update_dlg.exec():
        return

    dependencies, github, branch = update_dlg.get_values()

    if github:
        source = f"git+https://github.com/errthumt/FoSpy.git@{branch}"
    else:
        source = "FoSpy"

    cmd += update(source=source, dependencies=dependencies, executable=new_executable, cmd_only=True)

    # print(cmd)

    run_detached_in_new_window(cmd)
    win.close()
    return True


def _load_packages(frozen_txt):
    pkgs = {}
    for line in frozen_txt.splitlines():
        line = line.strip()
        if "==" in line:
            name, ver = line.split("==", 1)
            pkgs[name.lower()] = ver
    return pkgs