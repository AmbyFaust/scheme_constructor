from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QCursor
from PyQt5.QtWidgets import QWidget

from core.schema_classes import Primitive, BaseGraphicsModel
from gui.primitive_widget import PrimitiveWidget, TestWidget


class RenderingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("border: 2px solid black;")  # Устанавливаем стиль с обводкой
        self.__set_widgets()
        self.dragging = False
        self.offset = None

    def __set_widgets(self):
        primitive = Primitive('test', [], 50, 50, 100, 50)
        # self.primitive_widget = PrimitiveWidget(self, controller=None, primitive=primitive)
        self.primitive_widget = TestWidget(self)
        self.primitive_widget.setGeometry(50, 100, 100, 50)
        self.primitive_widget.setStyleSheet("background-color: yellow;")  # Задаем цвет фона внутреннего виджета

    def move_center_pressed_widget_to_cursor(self, pressed_widget, cursor_x, cursor_y):
        x = self.x() + pressed_widget.x() + pressed_widget.width() // 2
        y = self.y() + pressed_widget.y() + pressed_widget.height() // 2
        print(x, y)
        QCursor.setPos(x, y)

    def mousePressEvent(self, event):
        if self.primitive_widget.geometry().contains(event.pos()):
            self.setCursor(Qt.PointingHandCursor)
            self.dragging = True
            self.setMouseTracking(True)
            center_widget_pos = QPoint(
                int(self.primitive_widget.width()/2),
                int(self.primitive_widget.height()/2))
            self.primitive_widget.move(event.pos() - center_widget_pos)
            self.offset = event.pos() - self.primitive_widget.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            x_possible = (
                int(self.primitive_widget.width()/2) + 11,
                self.width() - int(self.primitive_widget.width()/2) - 11
            )
            y_possible = (
                int(self.primitive_widget.height() / 2) + 11,
                self.height() - int(self.primitive_widget.height()/2) - 11
            )
            cursor_x = event.x()
            cursor_y = event.y()
            delta_x = 0
            delta_y = 0
            last_pos_cursor_screen = QCursor.pos()
            if cursor_x < x_possible[0]:
                delta_x = cursor_x - x_possible[0]
            elif cursor_x > x_possible[1]:
                delta_x = cursor_x - x_possible[1]
            if cursor_y < y_possible[0]:
                delta_y = cursor_y - y_possible[0]
            elif cursor_y > y_possible[1]:
                delta_y = cursor_y - y_possible[1]
            QCursor.setPos(
                last_pos_cursor_screen.x() - delta_x,
                last_pos_cursor_screen.y() - delta_y
            )
            new_pos = event.pos() - QPoint(delta_x, delta_y) - self.offset
            self.primitive_widget.move(new_pos)

    def mouseReleaseEvent(self, event):
        self.dragging = False
        self.unsetCursor()
        self.setMouseTracking(False)

