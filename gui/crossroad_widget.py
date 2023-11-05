from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QWidget

from settings import crossroad_width, crossroad_height


class CrossroadWidget(QWidget):
    def __init__(self, parent, wires, x: int, y: int):
        super(CrossroadWidget, self).__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setFixedWidth(crossroad_width)
        self.setFixedHeight(crossroad_height)
        self.setStyleSheet("border: 1px black;")
        self.wires = wires
        self.offset = QPoint(
            self.width() // 2,
            self.height() // 2
        )
        self.move(x, y)


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(0, 0, 0))
        painter.setPen(Qt.NoPen)

        # Рисуем круг в центре виджета
        rect = self.rect()
        diameter = min(rect.width(), rect.height())
        painter.drawEllipse((rect.width() - diameter) // 2, (rect.height() - diameter) // 2, diameter, diameter)

