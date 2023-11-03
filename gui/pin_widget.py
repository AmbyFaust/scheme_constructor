import math

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QColor, QCursor
from PyQt5.QtWidgets import QWidget, QAction

from gui.rendering_controller import RenderingController
from settings import pin_width, pin_height


class PinWidget(QWidget):
    def __init__(self, parent, connected_widget, controller: RenderingController = None):
        super(PinWidget, self).__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("border: 1px black;")
        self.setFixedWidth(pin_width)
        self.setFixedHeight(pin_height)
        self.controller = controller
        self.connected_widget = connected_widget
        self.pin_connection = None
        self.graphics_model = None
        self.wire = None

        self.dragging = False
        self.offset = QPoint(
            int(self.width() / 2),
            int(self.height() / 2)
        )
        self.pin_possible_move_points = self.get_pin_possible_points()

        self.__set_widgets()
        self.__set_layouts()
        self.__set_connections()

        self.move(
            connected_widget.x() + int(connected_widget.width() / 2) - int(self.width() / 2),
            connected_widget.y() + connected_widget.height() - int(self.height() / 2)
        )
        # self.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.customContextMenuRequested.connect(self.show_context_menu)

    def destructor(self):
        self.connected_widget = None

    def __set_widgets(self):
        pass

    def __set_layouts(self):
        pass

    def __set_connections(self):
        pass

    def __create_actions(self):
        self.add_pin_action = QAction("Добавить Пин", self)
        self.add_pin_action.triggered.connect(self.add_pin)
        self.set_name_action = QAction("Изменить имя", self)
        self.set_name_action.triggered.connect(self.set_name)
        self.del_action = QAction("Удалить", self)
        self.del_action.triggered.connect(self.delete)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(255, 0, 0))
        # painter.setPen(Qt.NoPen)  # Убираем обводку

        # Рисуем круг в центре виджета
        rect = self.rect()
        diameter = min(rect.width(), rect.height())
        painter.drawEllipse((rect.width() - diameter) // 2, (rect.height() - diameter) // 2, diameter, diameter)

    def set_pin_connection(self, pin_connection):
        self.pin_connection = pin_connection

    def set_graphics_model(self, graphics_model):
        self.graphics_model = graphics_model

    def calc_distance(self, a: QPoint, b: QPoint):
        return ((a.x() - b.x())**2 + (a.y() - b.y())**2)**0.5

    def get_pin_possible_points(self):
        possible_points = []

        for dx in range(self.connected_widget.width()):
            possible_points.append(QPoint(dx, 0) - self.offset)
            possible_points.append(QPoint(dx, self.connected_widget.height()) - self.offset)
        for dy in range(self.connected_widget.height()):
            possible_points.append(QPoint(0, dy) - self.offset)
            possible_points.append(QPoint(self.connected_widget.width(), dy) - self.offset)

        return possible_points

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            QCursor.setPos(self.mapToGlobal(self.offset))
            self.dragging = True

    def mouseMoveEvent(self, event):
        new_pos = self.pin_possible_move_points[0]
        min_distance = math.inf
        for point in self.pin_possible_move_points:
            distance = self.calc_distance(self.connected_widget.pos() + point, self.pos() + event.pos())
            if distance < min_distance:
                new_pos = point
                min_distance = distance
        self.move(self.connected_widget.pos() + new_pos)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False

    def __del__(self):
        print('уняня')
