from PyQt5.QtCore import QRect, QPoint, Qt
from PyQt5.QtGui import QPainter, QCursor
from PyQt5.QtWidgets import QWidget

from core.schema_classes import Primitive
from gui.rendering_controller import RenderingController


class PrimitiveWidget(QWidget):
    def __init__(self, parent=None, controller: RenderingController = None, primitive: Primitive = None):
        super(PrimitiveWidget, self).__init__(parent)
        self.controller = controller
        self.primitive = primitive
        self.move(primitive.get_left(), primitive.get_top())
        self.setFixedWidth(100)
        self.setFixedHeight(50)
        self.setStyleSheet("border: 2px solid red;")
        # self.x = primitive.get_left()
        # self.y = primitive.get_top()
        print(self.x(), self.y())

        self.__set_widgets()
        self.__set_layouts()
        self.__set_connections()


    def __set_widgets(self):
        pass

    def __set_layouts(self):
        pass

    def __set_connections(self):
        pass

    def move_cursor_to_center(self):
        # Вычисляем координаты центра виджета
        center_x = self.x() + self.width() // 2
        center_y = self.y() + self.height() // 2

        # Устанавливаем позицию курсора в центр виджета
        QCursor.setPos(center_x, center_y)


class TestWidget(QWidget):
    def __init__(self, parent):
        super(TestWidget, self).__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)

    def move_cursor_to_center(self):
        center_x = self.x() + self.width() // 2
        center_y = self.y() + self.height() // 2

        QCursor.setPos(center_x, center_y)
