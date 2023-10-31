from PyQt5.QtWidgets import QMainWindow, QPushButton


class WindowChecker(QMainWindow):
    """
    Window for working with checker
    """
    def __init__(self):
        super(WindowChecker, self).__init__()
        self.setWindowTitle('WindowChecker')
        self.setMinimumWidth(500)
        self.setMinimumHeight(500)

        self.button = QPushButton(self)
        self.button.setText('Run checker')
        self.button.clicked.connect(self.run_button)

    def run_button(self):
        """
        To run checker
        :return:
        """
        pass