import math
from time import sleep

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QCursor
from PyQt5.QtWidgets import QWidget, QPushButton

from core.schema_classes import Primitive, BaseGraphicsModel
from gui.block_widget import BlockWidget
from gui.pin_widget import PinWidget
from gui.primitive_widget import PrimitiveWidget
from settings import primitive_width, primitive_height, pin_width, pin_height


class RenderingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("border: 2px solid black;")  # Устанавливаем стиль с обводкой
        self.setMinimumWidth(400)
        self.setMinimumHeight(400)
        self.dragging = False
        self.primitive_offset = QPoint(
            int(primitive_width / 2),
            int(primitive_height / 2)
        )
        self.primitive_widget = None
        self.primitives_widgets = []

        self.pin_widgets = []
        self.pin_offset = QPoint(
            int(pin_width / 2),
            int(pin_height / 2)
        )
        self.pin_possible_points = []

        self.pressed_widget = None
        self.__set_widgets()

    def __set_widgets(self):
        pass

    def add_primitive(self):
        primitive = Primitive('test', [], 50, 100, 100, 50)
        primitive_widget = PrimitiveWidget(self, controller=None, primitive=primitive)
        primitive_widget.setStyleSheet("background-color: yellow;")
        primitive_widget.show()

        ################################################ tmp
        pin_widget = PinWidget(self)
        pin_widget.connected_widget = primitive_widget
        self.pin_widgets.append(pin_widget)
        primitive_widget.pin_widgets.append(pin_widget)
        x = primitive_widget.x() + int(primitive_widget.width() / 2) - int(pin_widget.width() / 2)
        y = primitive_widget.y() + primitive_widget.height() - int(pin_widget.height() / 2)
        pin_widget.move(x, y)
        pin_widget.show()
        ################################################

        self.primitives_widgets.append(primitive_widget)
        print('add primitive')

    def del_primitive(self, primitive_widget):
        self.primitives_widgets.remove(primitive_widget)
        primitive_widget.deleteLater()

    def del_pin(self, pin_widget):
        self.pin_widgets.remove(pin_widget)
        pin_widget.connected_widget.pin_widgets.remove(pin_widget)
        pin_widget.deleteLater()

    def get_pin_possible_points(self, connected_widget: PrimitiveWidget | BlockWidget):
        self.pin_possible_points.clear()

        if isinstance(self.pressed_widget, PinWidget):
            offset = self.pin_offset
        elif isinstance(self.pressed_widget, PrimitiveWidget):
            offset = self.primitive_offset

        for dx in range(connected_widget.width()):
            self.pin_possible_points.append(QPoint(
                connected_widget.x() + dx,
                connected_widget.y()
            ) - offset)
            self.pin_possible_points.append(QPoint(
                connected_widget.x() + dx,
                connected_widget.y() + connected_widget.height()
            ) - offset)
        for dy in range(connected_widget.height()):
            self.pin_possible_points.append(QPoint(
                connected_widget.x(),
                connected_widget.y() + dy
            ) - offset)
            self.pin_possible_points.append(QPoint(
                connected_widget.x() + connected_widget.width(),
                connected_widget.y() + dy
            ) - offset)

    def calc_distance(self, a: QPoint, b: QPoint):
        return ((a.x() - b.x())**2 + (a.y() - b.y())**2)**0.5

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            for widget in (self.pin_widgets + self.primitives_widgets):
                if widget.geometry().contains(event.pos()):
                    self.pressed_widget = widget
                    self.setCursor(Qt.PointingHandCursor)
                    self.setMouseTracking(True)

                    offset = QPoint()
                    if isinstance(self.pressed_widget, PinWidget):
                        offset = self.pin_offset
                        self.get_pin_possible_points(self.pressed_widget.connected_widget)
                    elif isinstance(self.pressed_widget, PrimitiveWidget):
                        offset = self.primitive_offset


                    QCursor.setPos(self.mapToGlobal(self.pressed_widget.pos() + offset))
                    self.dragging = True
                    break

    def mouseMoveEvent(self, event):
        if not self.dragging:
            return

        if isinstance(self.pressed_widget, PrimitiveWidget):
            x_possible = (
                int(self.pressed_widget.width()/2),
                self.width() - int(self.pressed_widget.width()/2)
            )
            y_possible = (
                int(self.pressed_widget.height()/2),
                self.height() - int(self.pressed_widget.height()/2)
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
            new_pos_primitive = event.pos() - QPoint(delta_x, delta_y) - self.primitive_offset
            for pin_widget in self.pressed_widget.pin_widgets:
                new_pos_pin = pin_widget.pos() + new_pos_primitive - self.pressed_widget.pos()
                pin_widget.move(new_pos_pin)
            self.pressed_widget.move(new_pos_primitive)

        elif isinstance(self.pressed_widget, PinWidget):
            new_pos_pin = self.pin_possible_points[0]
            min_distance = self.calc_distance(new_pos_pin, event.pos())

            for point in self.pin_possible_points:
                distance = self.calc_distance(point, event.pos())
                if distance < min_distance:
                    new_pos_pin = point
                    min_distance = distance
            self.pressed_widget.move(new_pos_pin)

    def mouseReleaseEvent(self, event):
        self.dragging = False
        self.unsetCursor()
        self.setMouseTracking(False)
        self.pressed_widget = None




