from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QWidget

from gui.rendering_controller import RenderingController
from settings import pin_width, pin_height


class PinWidget(QWidget):
    def __init__(self, parent=None, controller: RenderingController = None):
        super().__init__()
        super(PinWidget, self).__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("border: 0px solid black;")
        self.setFixedWidth(pin_width)
        self.setFixedHeight(pin_height)
        self.controller = controller
        self.connected_widget = None
        self.pin_connection = None
        self.graphics_model = None
        self.__set_widgets()
        self.__set_layouts()
        self.__set_connections()

    def __set_widgets(self):
        pass

    def __set_layouts(self):
        pass

    def __set_connections(self):
        pass

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # Включаем сглаживание
        painter.setBrush(QColor(255, 0, 0))  # Задаем цвет круга (красный)
        painter.setPen(Qt.NoPen)  # Убираем обводку

        # Рисуем круг в центре виджета
        rect = self.rect()
        diameter = min(rect.width(), rect.height())
        painter.drawEllipse((rect.width() - diameter) // 2, (rect.height() - diameter) // 2, diameter, diameter)

    def set_pin_connection(self, pin_connection):
        self.pin_connection = pin_connection

    def set_graphics_model(self, graphics_model):
        self.graphics_model = graphics_model
