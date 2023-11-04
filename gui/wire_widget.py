from enum import Enum

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QWidget, QAction, QMenu

from gui.rendering_controller import RenderingController
from settings import width_wire


class Direction(Enum):
    horizontal = 0
    vertical = 1

    @classmethod
    def get_another(cls, direction):
        if direction == cls.horizontal:
            return cls.vertical
        else:
            return cls.horizontal


class WireWidget(QWidget):
    def __init__(self, parent, start: QPoint, direction: Direction = None,
                 connected_widget=None, controller: RenderingController = None):
        super(WireWidget, self).__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("border: 0px black;")
        self.controller = controller
        self.connected_wires = []
        self.direction = direction
        self.connected_widget = connected_widget
        self.move(start)
        self.setFixedSize(width_wire, width_wire)
        self.start = start
        self.end = start
        self.width_wire = width_wire
        self.drawing = True
        self.__create_actions()


        self.setMouseTracking(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def __create_actions(self):
        self.add_branching_action = QAction("Добавить ветвление", self)
        self.add_branching_action.triggered.connect(self.add_branching)
        self.del_action = QAction("Удалить", self)
        self.del_action.triggered.connect(self.delete)

    def show_context_menu(self, position):
        context_menu = QMenu(self)
        context_menu.setStyleSheet("background-color: gray;")
        context_menu.addAction(self.add_branching_action)
        context_menu.addAction(self.del_action)
        context_menu.exec(self.mapToGlobal(position))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(Qt.black)
        pen.setWidth(1)
        painter.setPen(pen)
        if self.direction == Direction.horizontal:
            painter.drawLine(QPoint(0, 8), QPoint(self.width(), 8))
        elif self.direction == Direction.vertical:
            painter.drawLine(QPoint(8, 0), QPoint(8, self.height()))

    def add_branching(self):
        pass

    def delete(self):
        pass

    def set_location(self, start: QPoint = None, end: QPoint = None):
        if not start:
            start = self.start
        if not end:
            end = self.end

        if self.direction == Direction.horizontal:
            if end.x() < self.start.x():
                self.move(end.x(), self.y())
            else:
                self.move(self.start.x(), self.y())
            self.setFixedWidth(abs(end.x() - start.x()))
            self.end = QPoint(end.x(), self.end.y())

        elif self.direction == Direction.vertical:
            if end.y() < self.start.y():
                self.move(self.x(), end.y())
            else:
                self.move(self.x(), self.start.y())
            self.setFixedHeight(abs(end.y() - start.y()))
            self.end = QPoint(self.end.x(), end.y())

    def move_wire(self, pos: QPoint):
        if self.direction == Direction.vertical:
            self.move(pos.x(), self.y())
        elif self.direction == Direction.horizontal:
            self.move(self.x(), pos.y())

    def mouseMoveEvent(self, event):
        if self.parent().rendered_wire:
            self.parent().mouseMoveEvent(event.pos() + self.pos())






