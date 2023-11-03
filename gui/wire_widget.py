from enum import Enum

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QWidget

from gui.pin_widget import PinWidget
from gui.rendering_controller import RenderingController

class Direction(Enum):
    horizontal = 0
    vertical = 1

class WireWidget(QWidget):
    def __init__(self, parent=None, controller: RenderingController = None,
                 direction: Direction = None, start: QPoint = None, connected_pin_widget: PinWidget = None):
        super(WireWidget, self).__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.controller = controller
        self.wire1 = None
        self.wire2 = None
        self.direction = direction
        self.connected_pin_widget = connected_pin_widget
        self.start = start
        self.end = QPoint()

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawLine(self.start, self.end)


