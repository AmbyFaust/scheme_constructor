from enum import Enum

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QWidget

from gui.rendering_controller import RenderingController

class Direction(Enum):
    horizontal = 0
    vertical = 1

class WireWidget(QWidget):
    def __init__(self, parent, start: QPoint, direction: Direction = None,
                 connected_pin_widget=None, controller: RenderingController = None):
        super(WireWidget, self).__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("border: 0px black;")
        self.controller = controller
        self.connected_wires = []
        self.direction = direction
        self.connected_pin_widget = connected_pin_widget
        self.move(start)
        self.setFixedSize(1, 1)
        self.start = start
        self.end = start + QPoint(100,50)
        self.drawing = True
        self.reverse_x = False
        self.reverse_y = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawLine(QPoint(0, 0), QPoint(self.width(), self.height()))

    # def mousePressEvent(self, event):
    #     if event.button() == Qt.LeftButton:
    #         self.drawing = False
    #         # next_wire_widget = WireWidget(self.parent(), )
    #         # self.connected_wires.
    #         self.start_x, self.start_y = event.x(), event.y()
    #         self.end_x, self.end_y = event.x(), event.y()

    # def mouseMoveEvent(self, event):
    #     if self.drawing:
    #         if self.direction == Direction.horizontal:
    #             new_width = event.x() - self.x()
    #             if event.x() < self.start.x():
    #                 self.move(self.x() + new_width, self.y())
    #                 self.setFixedWidth(self.start.x() - self.x())
    #             else:
    #                 self.move(self.start.x(), self.y())
    #                 self.setFixedWidth(new_width)
    #         elif self.direction == Direction.vertical:
    #             new_height = event.y() - self.y()
    #             self.setFixedHeight(new_height)



