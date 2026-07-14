from PySide6.QtWidgets import QApplication, QSplashScreen
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import sys

from .window import MainWindow
from ._utils import add_parser, ASSETS

SPLASH_PCT = 30

@add_parser(
    ("copy", "c"),
    ("open_path", "o"),
    desc="CLI Entry for FoSpy App",
    args_to=MainWindow
)
def main_cli(**kwargs):
    app = QApplication(sys.argv)

    screen = app.primaryScreen()
    geo = screen.geometry()
    screen_h = geo.height()
    splash_h = (screen_h * SPLASH_PCT) // 100

    pixmap = QPixmap(ASSETS["splash"])
    scaled = pixmap.scaledToHeight(splash_h, Qt.SmoothTransformation)

    splash = QSplashScreen(scaled, Qt.WindowStaysOnTopHint)
    splash.show()
    app.processEvents()

    window = MainWindow(**kwargs)
    window.show()
    splash.finish(window)

    sys.exit(app.exec())


def main():
    main_cli()

def setup():
    from ._utils import register_dlg

    register_dlg()


if __name__ == "__main__":
    main_cli()

    