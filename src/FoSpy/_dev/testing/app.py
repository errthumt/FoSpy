import subprocess
import sys
def run():
    from ...ui import available, app
    try:
        app._import_gate()
        subprocess.check_call(
            [sys.executable, "-m", "FoSpy.ui.app"],
        )
        return True
    except available.UINotAvailable:
        if input("Do you want to install additional dependencies for the GUI app? (y/n) ").lower() == "y":
            return install_dependencies()
        
        return True
    except (SystemExit, Exception):
        from PySide6.QtWidgets import QApplication
        app = QApplication.instance()
        if app is not None:
            app.quit()
            app.deleteLater()

        return True


def install_dependencies():
    print("\nPLEASE NOTE: For changes to take effect, you must exit the testing suite and wait for packages to install before restarting.")
    input("Press any key to continue...")
    subprocess.Popen(
        [sys.executable, "-m", "pip", "install", "-e", ".[DEV-TEST, app]"],
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
    )

    return False

    