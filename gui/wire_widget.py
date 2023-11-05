from enum import Enum

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen, QCursor, QMouseEvent
from PyQt5.QtWidgets import QWidget, QAction, QMenu

from gui.rendering_controller import RenderingController
from settings import width_wire, rendering_widget_width, rendering_widget_height


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
                 connected_pin=None, controller: RenderingController = None):
        super(WireWidget, self).__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("border: 0px black;")
        self.controller = controller
        self.connected_wires = []
        self.direction = direction
        self.connected_pins = []
        if connected_pin:
            self.connected_pins.append(connected_pin)
        self.move(start)
        self.setFixedSize(width_wire, width_wire)
        self.start = start
        self.end = start

        self.drawing = True
        self.offset = QPoint(
            self.width() // 2 + 1,
            self.height() // 2 + 1
        )
        self.dragging = False
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
        if self.connected_pins:
            print(self.connected_pins)
            for pin_widget in self.connected_pins:
                pin_widget.wire = None
                pin_widget.unlock()
            self.connected_pins.clear()

        for wire in self.connected_wires:
            wire.connected_wires.remove(self)
            wire.delete()
        self.deleteLater()

    def set_location(self, start: QPoint = None, end: QPoint = None):
        if not start:
            start = self.start
        if not end:
            end = self.end

        if self.direction == Direction.horizontal:
            if end.x() < self.start.x():
                self.move(end.x(), self.y())
            else:
                self.move(start.x(), self.y())
            self.setFixedWidth(abs(end.x() - start.x()))

            self.end = QPoint(end.x(), self.end.y())

        elif self.direction == Direction.vertical:
            if end.y() < self.start.y():
                self.move(self.x(), end.y())
            else:
                self.move(self.x(), start.y())
            self.setFixedHeight(abs(end.y() - start.y()))
            self.end = QPoint(self.end.x(), end.y())

        self.start = start

        self.offset = QPoint(
            self.width() // 2 + 1,
            self.height() // 2 + 1
        )

    def mousePressEvent(self, event):
        if self.parent().rendered_wire:
            new_event = QMouseEvent(event.type(),
                                    event.pos() + self.pos(),
                                    event.screenPos(),
                                    event.button(),
                                    event.buttons(),
                                    event.modifiers())
            self.parent().mousePressEvent(new_event)
            return

        if event.button() == Qt.LeftButton:
            QCursor.setPos(self.mapToGlobal(self.offset))
            self.dragging = True

    def mouseMoveEvent(self, event):
        if self.parent().rendered_wire:
            self.parent().mouseMoveEvent(event.pos() + self.pos())
            return

        if self.dragging:
            x_possible = (
                self.width() // 2 + 1,
                rendering_widget_width - self.width() // 2 + 1
            )
            y_possible = (
                self.height() // 2 + 1,
                rendering_widget_height - self.height() // 2 + 1
            )
            pos = self.pos() + event.pos()
            cursor_x = pos.x()
            cursor_y = pos.y()
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
            new_pos = pos - QPoint(delta_x, delta_y) - self.offset
            if not self.connected_pins:
                if self.direction == Direction.vertical:
                    self.move(new_pos.x(), self.y())
                elif self.direction == Direction.horizontal:
                    self.move(self.x(), new_pos.y())

            if not self.connected_pins:
                    self.connected_wires[0].set_location(end=self.pos() + self.offset)
                    self.connected_wires[1].set_location(start=self.pos() + self.offset)


    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False







