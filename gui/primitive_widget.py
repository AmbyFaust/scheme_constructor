from PyQt5.QtCore import QRect, QPoint, Qt
from PyQt5.QtGui import QPainter, QCursor
from PyQt5.QtWidgets import QWidget, QMenu, QAction

from core.schema_classes import Primitive
from gui.pin_widget import PinWidget
from gui.rendering_controller import RenderingController
from settings import primitive_width, primitive_height


class PrimitiveWidget(QWidget):
    def __init__(self, parent=None, controller: RenderingController = None, primitive: Primitive = None):
        super(PrimitiveWidget, self).__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.controller = controller
        self.primitive = primitive
        self.move(primitive.get_left(), primitive.get_top())
        self.setFixedWidth(primitive_width)
        self.setFixedHeight(primitive_height)
        self.setStyleSheet("border: 2px solid red;")

        self.pin_widgets = []

        self.__create_widgets()
        self.__create_layouts()
        self.__create_connections()
        self.__create_actions()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def __create_widgets(self):
        pass

    def __create_layouts(self):
        pass

    def __create_connections(self):
        pass

    def __create_actions(self):
        self.del_action = QAction("Удалить", self)
        self.del_action.triggered.connect(self.delete)
        self.add_pin_action = QAction("Добавить Пин", self)
        self.add_pin_action.triggered.connect(self.add_pin)

    def show_context_menu(self, position):
        context_menu = QMenu(self)
        context_menu.setStyleSheet("background-color: gray;")
        context_menu.addAction(self.del_action)
        context_menu.addAction(self.add_pin_action)
        context_menu.exec(self.mapToGlobal(position))

    def delete(self):
        pass

    def add_pin(self):
        pass



