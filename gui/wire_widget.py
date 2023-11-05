from enum import Enum

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen, QCursor, QMouseEvent
from PyQt5.QtWidgets import QWidget, QAction, QMenu

from gui.crossroad_widget import CrossroadWidget
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

        self.connected_crossroads = []
        self.move(start)
        self.setFixedSize(width_wire, width_wire)
        self.start = start
        self.end = start

        self.drawing = True
        self.offset = QPoint(
            self.width() // 2 + 1,
            self.height() // 2 + 1
        )
        self.se = True
        self.dragging = False
        self.__create_actions()
        self.setMouseTracking(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def __create_actions(self):
        self.add_crossroad_action = QAction("Добавить ветвление", self)
        self.add_crossroad_action.triggered.connect(self.add_crossroad)
        self.del_action = QAction("Удалить", self)
        self.del_action.triggered.connect(self.delete)

    def show_context_menu(self, position):
        center = QPoint(self.width() // 2 + 1, self.height() // 2 + 1)
        QCursor.setPos(self.mapToGlobal(center))
        context_menu = QMenu(self)
        context_menu.setStyleSheet("background-color: gray;")
        context_menu.addAction(self.add_crossroad_action)
        context_menu.addAction(self.del_action)
        if not self.parent().rendered_wire:
            context_menu.exec(self.mapToGlobal(center))

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

    def add_crossroad(self):
        center = QPoint(self.width() // 2 + 1, self.height() // 2 + 1)
        # self.move(
        #     wire.x() + wire.width() // 2 + 1 - self.offset.x(),
        #     wire.y() + wire.height() // 2 + 1 - self.offset.y()
        # )
        if self.start.x() > self.end.x() or self.start.y() > self.end.y():
            pass
        else:
            pin_widget = None
            if self.connected_pins:
                pin_widget = self.connected_pins[-1]

            start = QPoint()
            if self.direction == Direction.horizontal:
                start = QPoint(self.start.x() + self.width() // 2 + 1, self.start.y())
            elif self.direction == Direction.vertical:
                stat = QPoint(self.start.x(), self.start.y() + self.height() // 2 + 1)
            new_wire = WireWidget(self.parent(), start, self.direction, pin_widget)
            new_wire.set_location(point=self.end)
            try:
                self.connected_wires[1].connected_wires[0] = new_wire
                self.connected_wires[1] = new_wire
            except Exception:
                pass
            try:
                self.connected_pins[-1].wire = new_wire
                self.connected_pins.pop(-1)
            except Exception:
                pass
            print(1)
            print(self.start + center)

            new_wire.show()
            self.set_location(point=self.start)



        # crossroad = CrossroadWidget(self.parent(), self)
        # self.connected_crossroads.append(crossroad)
        # crossroad.show()

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

    def calc_distance(self, a: QPoint, b: QPoint):
        return ((a.x() - b.x())**2 + (a.y() - b.y())**2)**0.5

    def set_location(self, point: QPoint):
        if not point:
            point = self.end

        if self.direction == Direction.horizontal:
            if point.x() <= self.start.x() <= self.end.x():
                if self.se:
                    self.end = self.start
                self.se = False
                self.start = QPoint(point.x(), self.start.y())
            elif self.start.x() <= point.x() <= self.end.x():
                if self.se:
                    self.end = QPoint(point.x(), self.end.y())
                else:
                    self.start = QPoint(point.x(), self.start.y())
            elif self.start.x() <= self.end.x() <= point.x():
                if not self.se:
                    self.start = self.end
                self.se = True
                self.end = QPoint(point.x(), self.end.y())
            self.setFixedWidth(abs(self.end.x() - self.start.x()))
        elif self.direction == Direction.vertical:
            if point.y() <= self.start.y() <= self.end.y():
                if self.se:
                    self.end = self.start
                self.se = False
                self.start = QPoint(self.start.x(), point.y())
            elif self.start.y() <= point.y() <= self.end.y():
                if self.se:
                    self.end = QPoint(self.end.x(), point.y())
                else:
                    self.start = QPoint(self.start.x(), point.y())
            elif self.start.y() <= self.end.y() <= point.y():
                if not self.se:
                    self.start = self.end
                self.se = True
                self.end = QPoint(self.end.x(), point.y())
            self.setFixedHeight(max(1, abs(self.end.y() - self.start.y())))

        self.move(self.start)

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
            if not self.connected_pins and not self.connected_crossroads:
                point = self.pos() + self.offset
                for wire in self.connected_wires:
                    point_start_distance = self.calc_distance(point, wire.start)
                    point_end_distance = self.calc_distance(point, wire.end)
                    if point_end_distance < point_start_distance:
                        wire.se = True
                    else:
                        wire.se = False
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

            if not self.connected_pins and not self.connected_crossroads:
                if self.direction == Direction.vertical:
                    self.start = QPoint(new_pos.x(), self.start.y())
                    self.end = QPoint(new_pos.x(), self.end.y())
                    self.move(new_pos.x(), self.y())
                elif self.direction == Direction.horizontal:
                    self.start = QPoint(self.start.x(), new_pos.y())
                    self.end = QPoint(self.end.x(), new_pos.y())
                    self.move(self.x(), new_pos.y())

                point = self.pos() + self.offset

                for wire in self.connected_wires:
                    wire.set_location(point=point)



    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False







