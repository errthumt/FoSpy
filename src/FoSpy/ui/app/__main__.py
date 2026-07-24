try:  # noqa: N999
    from ._utils import add_parser
    from .window import MainWindow
except Exception:  # noqa: BLE001
    def add_parser(*args, **kwargs):
        def decorator(func):
            return func
        return decorator
    
    MainWindow = None

SPLASH_PCT = 30

@add_parser(
    ("copy", "c"),
    ("open_path", "o"),
    desc="CLI Entry for FoSpy App",
    args_to=MainWindow
)
def main_cli(**kwargs):
    from . import _import_gate
    _import_gate()
    import sys

    from PySide6.QtCore import Qt
    from PySide6.QtGui import QPixmap
    from PySide6.QtWidgets import QApplication, QSplashScreen

    from ...config import values as cfg
    from ._utils import ASSETS, register_dlg
    from .check_update import check_env
    from .window import MainWindow

    app = QApplication(sys.argv)

    screen = app.primaryScreen()
    geo = screen.geometry()
    screen_h = geo.height()
    splash_h = (screen_h * SPLASH_PCT) // 100

    pixmap = QPixmap(ASSETS["splash"])
    scaled = pixmap.scaledToHeight(splash_h, Qt.SmoothTransformation)

    splash = QSplashScreen(scaled, Qt.WindowStaysOnTopHint)
    if cfg.get("APP.splash", True):
        splash.show()

    try:
        app.processEvents()

        window = MainWindow(**kwargs)
        window.show()
    except Exception:
        splash.hide()
        raise
    
    splash.finish(window)

    if check_env(window) is None:
        register_dlg()

    sys.exit(app.exec())


def main():
    main_cli()

def setup():
    from ._utils import register_dlg

    register_dlg()


if __name__ == "__main__":
    main_cli()

    