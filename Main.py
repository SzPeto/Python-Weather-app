import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from app_window import AppWindow


def main():
    app = QApplication(sys.argv)
    app_window = AppWindow()
    app_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()