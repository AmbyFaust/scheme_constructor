from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QDialog, QWidget, QLineEdit, QPushButton, QVBoxLayout, QFormLayout, QHBoxLayout


class SetNameDialog(QDialog):
    def __init__(self, cur_name: str, title_name='Изменение имени', place_holder="Введите имя"):
        super().__init__()
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle(title_name)
        self.cur_name = cur_name
        self.place_holder = place_holder
        self.setMinimumSize(500, 0)
        self.__create_widgets()
        self.__create_layouts()
        self.__create_connections()

    def __create_widgets(self):
        self.name_edit = QLineEdit(self.cur_name)
        self.name_edit.setPlaceholderText(self.place_holder);

        self.accept_btn = QPushButton('Принять')
        self.cancel_btn = QPushButton('Отмена')

    def __create_layouts(self):
        common_v_layout = QVBoxLayout()
        name_form_layout = QFormLayout()
        name_form_layout.addRow('Имя:', self.name_edit)
        button_h_layout = QHBoxLayout()
        button_h_layout.addWidget(self.accept_btn)
        button_h_layout.addWidget(self.cancel_btn)
        common_v_layout.addLayout(name_form_layout)
        common_v_layout.addLayout(button_h_layout)
        self.setLayout(common_v_layout)

    def __create_connections(self):
        self.cancel_btn.clicked.connect(self.reject)
        self.accept_btn.clicked.connect(self.accept)

