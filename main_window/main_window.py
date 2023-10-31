import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMenu, QMainWindow, QWidget, QPushButton, QMenuBar

from window_checker import WindowChecker
from window_redactor import WindowRedactor


class MainWindow(QMainWindow):
    """
    Main window to chose between checker and redactor
    """
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('MainWindow')
        self.setMinimumWidth(400)
        self.setMinimumHeight(200)

        self.redactor = WindowRedactor()
        self.checker = WindowChecker()

        self.button_redactor = QPushButton(self, text="Open Redactor")
        self.button_redactor.move(50, 100)
        self.button_redactor.setFixedWidth(100)
        self.button_redactor.clicked.connect(self.run_redactor)

        self.button_checker = QPushButton(self, text="Open Checker")
        self.button_checker.move(200, 100)
        self.button_checker.setFixedWidth(100)
        self.button_checker.clicked.connect(self.run_checker)

    def run_redactor(self):
        """
        To open Redactor window
        :return:
        """
        self.redactor.show()

    def run_checker(self):
        """
        To open Checker window
        :return:
        """
        self.checker.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())