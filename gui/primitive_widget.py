from PyQt5.QtCore import QRect, QPoint, Qt
from PyQt5.QtGui import QPainter, QCursor
from PyQt5.QtWidgets import QWidget, QMenu, QAction, QVBoxLayout, QLabel, QDialog

from core.schema_classes import Primitive
from gui.pin_widget import PinWidget
from gui.rendering_controller import RenderingController
from gui.set_name_dialog import SetNameDialog
from settings import primitive_width, primitive_height


class PrimitiveWidget(QWidget):
    def __init__(self, parent=None, controller: RenderingController = None, primitive: Primitive = None):
        super(PrimitiveWidget, self).__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.controller = controller
        self.primitive = primitive
        self.move(primitive.get_left(), primitive.get_top())
        self.setFixedWidth(primitive.get_width())
        self.setFixedHeight(primitive.get_height())
        self.setStyleSheet("border: 2px solid black; background-color: #cccccc;")

        self.pin_widgets = []

        self.__create_widgets()
        self.__create_layouts()
        self.__create_actions()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def __create_widgets(self):
        self.name_label = QLabel(self.primitive.get_name())
        self.name_label.setStyleSheet('border: 0px ')
        self.name_label.setAlignment(Qt.AlignCenter)

    def __create_layouts(self):
        common_v_layout = QVBoxLayout()
        common_v_layout.addWidget(self.name_label)
        self.setLayout(common_v_layout)



    def __create_actions(self):
        self.add_pin_action = QAction("Добавить Пин", self)
        self.add_pin_action.triggered.connect(self.add_pin)
        self.set_name_action = QAction("Изменить имя", self)
        self.set_name_action.triggered.connect(self.set_name)
        self.del_action = QAction("Удалить", self)
        self.del_action.triggered.connect(self.delete)

    def show_context_menu(self, position):
        context_menu = QMenu(self)
        context_menu.setStyleSheet("background-color: gray;")
        context_menu.addAction(self.add_pin_action)
        context_menu.addAction(self.set_name_action)
        context_menu.addAction(self.del_action)
        context_menu.exec(self.mapToGlobal(position))

    def delete(self):
        pass

    def add_pin(self):
        pass

    def set_name(self):
        set_name_dialog = SetNameDialog(self.name_label.text())
        if set_name_dialog.exec_() == QDialog.Accepted:
            self.primitive.set_name(set_name_dialog.name_edit.text())
            self.name_label.setText(self.primitive.get_name())

