from enum import Enum

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen, QCursor, QMouseEvent, QColor
from PyQt5.QtWidgets import QWidget, QAction, QMenu

from gui.crossroad_widget import CrossroadWidget
from gui.direction_enum import Direction
from settings import width_wire, rendering_widget_width, rendering_widget_height


class WireWidget(QWidget):
    def __init__(self, parent, start: QPoint, end: QPoint, direction: Direction,
                 connected_pins: list = [], connected_crossroads: list = []):
        super(WireWidget, self).__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("border: 0px black;")
        self.connected_wires = []
        self.direction = direction

        self.connected_pins = connected_pins
        for pin_widget in self.connected_pins:
            pin_widget.lock()

        self.connected_crossroads = connected_crossroads

        self.move(start)
        self.start = start
        self.end = end
        self.setFixedSize(width_wire, width_wire)

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
        pen = QPen(QColor(0, 0, 0, 128))
        pen.setWidth(2)
        painter.setPen(pen)
        if self.direction == Direction.horizontal:
            painter.drawLine(QPoint(0, 8), QPoint(self.width(), 8))
        elif self.direction == Direction.vertical:
            painter.drawLine(QPoint(8, 0), QPoint(8, self.height()))

    def determine_se(self, point):
        point_start_distance = self.calc_distance(point, self.start)
        point_end_distance = self.calc_distance(point, self.end)
        if point_end_distance < point_start_distance:
            self.se = True
        else:
            self.se = False

    def add_crossroad(self):
        wire1_end = QPoint()
        wire2_start = QPoint()
        if self.direction == Direction.horizontal:
            delta = self.width() // 2 + 1
            wire1_end = QPoint(self.start.x() + delta, self.end.y())
            wire2_start = QPoint(self.start.x() + delta, self.start.y())
        elif self.direction == Direction.vertical:
            delta = self.height() // 2 + 1
            wire1_end = QPoint(self.end.x(), self.start.y() + delta)
            wire2_start = QPoint(self.start.x(), self.start.y() + delta)

        wire1 = self.parent().add_wire(
            start=self.start,
            end=wire1_end,
            direction=self.direction,
            connected_pins=[],
            connected_crossroads=[]
        )
        wire1.set_location(wire1_end)
        wire1.lower()

        wire2 = self.parent().add_wire(
            start=wire2_start,
            end=self.end,
            direction=self.direction,
            connected_pins=[],
            connected_crossroads=[]
        )
        wire2.set_location(self.end)
        wire2.lower()

        for pin_widget in self.connected_pins:
            if pin_widget.geometry().contains(wire1.start):
                wire1.connected_pins.append(pin_widget)
                pin_widget.wire = wire1
            elif pin_widget.geometry().contains(wire2.end):
                wire2.connected_pins.append(pin_widget)
                pin_widget.wire = wire2

        delta = QPoint()
        if self.direction == Direction.horizontal:
            delta = QPoint(0, width_wire // 2 + 1)
        elif self.direction == Direction.vertical:
            delta = QPoint(width_wire // 2 + 1, 0)

        for crossroad_widget in self.connected_crossroads:
            crossroad_widget.connected_wires.remove(self)
            if crossroad_widget.geometry().contains(wire1.start + delta):
                wire1.connected_crossroads.append(crossroad_widget)
                crossroad_widget.connected_wires.append(wire1)
            elif crossroad_widget.geometry().contains(wire2.end - delta):
                wire2.connected_crossroads.append(crossroad_widget)
                crossroad_widget.connected_wires.append(wire2)

        if len(self.connected_crossroads) < 2:
            connect_distance = self.calc_distance(QPoint(width_wire // 2 + 1, 0), QPoint(0, width_wire // 2 + 1))
            for wire_widget in self.connected_wires:
                wire_widget.connected_wires.remove(self)

                if self.calc_distance(self.start, wire_widget.start) == connect_distance \
                        or self.calc_distance(self.start, wire_widget.end) == connect_distance:
                    wire_widget.connected_wires.append(wire1)
                    wire1.connected_wires.append(wire_widget)
                elif self.calc_distance(self.end, wire_widget.start) == connect_distance \
                        or self.calc_distance(self.end, wire_widget.end) == connect_distance:
                    wire_widget.connected_wires.append(wire2)
                    wire2.connected_wires.append(wire_widget)

        wire1.show()
        wire2.show()

        crossroad_widget = self.parent().add_crossroad(
            [wire1, wire2],
            QPoint(
                self.start.x() + self.width() // 2 + 1,
                self.start.y() + self.height() // 2 + 1
            )
        )

        crossroad_widget.move(crossroad_widget.pos() - crossroad_widget.offset)
        wire1.connected_crossroads.append(crossroad_widget)
        wire2.connected_crossroads.append(crossroad_widget)

        self.connected_wires.clear()
        self.connected_crossroads.clear()
        self.connected_pins.clear()

        self.delete()

    def delete(self):
        if self.connected_pins:
            for pin_widget in self.connected_pins:
                pin_widget.wire = None
                pin_widget.unlock()
            self.connected_pins.clear()

        for wire in self.connected_wires:
            try:
                wire.connected_wires.remove(self)
                wire.delete()
            except Exception:
                pass

        self.connected_wires.clear()

        for crossroads_widget in self.connected_crossroads:
            crossroads_widget.connected_wires.remove(self)
            crossroads_widget.cascade_delete()
        self.connected_crossroads.clear()

        if self in self.parent().all_wire_widgets:
            self.parent().all_wire_widgets.pop(self)
        self.deleteLater()

    def clear(self):
        self.connected_wires.clear()
        self.connected_pins.clear()
        self.connected_crossroads.clear()

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
            self.setFixedHeight(abs(self.end.y() - self.start.y()))

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
                    wire.determine_se(point)

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
            self.move_wire(new_pos)

    def move_wire(self, new_pos):
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







