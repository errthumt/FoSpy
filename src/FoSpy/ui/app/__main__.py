from PySide6.QtWidgets import QApplication
import argparse
import sys

from .window import MainWindow

def main():
    parser = argparse.ArgumentParser(description='Fospy App Launcher')

    parser.add_argument(
        "filepath",
        nargs="?",
        default=None,
        help="Path to the initial FoS-style format to load on startup."
    )

    args = parser.parse_args()

    app = QApplication(sys.argv)

    window = MainWindow(args.filepath)
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()

    