from PySide6.QtWidgets import QApplication
import sys

from .window import MainWindow
from ._utils import add_parser

@add_parser(
    ("copy", "c"),
    ("open_path", "o"),
    desc="CLI Entry for FoSpy App",
    args_to=MainWindow
)
def main_cli(**kwargs):
    app = QApplication(sys.argv)

    window = MainWindow(**kwargs)
    window.show()

    sys.exit(app.exec())


def main():
    main_cli()

def setup():
    from ._utils import register_dlg

    register_dlg()


if __name__ == "__main__":
    main_cli()

    