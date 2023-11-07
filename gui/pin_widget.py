import math

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QColor, QCursor, QPen, QMouseEvent
from PyQt5.QtWidgets import QWidget, QAction, QMenu

from gui.wire_widget import WireWidget, Direction
from settings import pin_width, pin_height, width_wire


class PossiblePoints:
    def __init__(self, connected_widget, offset):
        self.top = []
        self.bottom = []
        self.right = []
        self.left = []
        self.all = []

        for dx in range(1, connected_widget.width() - 1):
            self.top.append(QPoint(dx, 0) - offset)
            self.bottom.append(QPoint(dx, connected_widget.height()) - offset)
        for dy in range(1, connected_widget.height() - 1):
            self.left.append(QPoint(0, dy) - offset)
            self.right.append(QPoint(connected_widget.width(), dy) - offset)
        self.all = self.top + self.bottom + self.right + self.left


class PinWidget(QWidget):
    def __init__(self, parent, connected_widget):
        super(PinWidget, self).__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.border = Qt.NoPen
        self.color = QColor()

        self.setStyleSheet("border: 1px black;")
        self.setFixedWidth(pin_width)
        self.setFixedHeight(pin_height)
        self.connected_widget = connected_widget
        self.pin_connection = None
        self.graphics_model = None
        self.wire = None

        self.dragging = False
        self.offset = QPoint(
            self.width() // 2,
            self.height() // 2
        )
        self.pin_possible_move_points = PossiblePoints(
            self.connected_widget,
            self.offset
        )

        self.__create_actions()
        self.unlock()

        self.move(
            connected_widget.x() + connected_widget.width() // 2 - self.width() // 2,
            connected_widget.y() + connected_widget.height() - self.height() // 2
        )
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        self.setMouseTracking(True)

    def destructor(self):
        self.connected_widget = None
        if self.wire:
            self.wire.delete()
        self.parent().pin_widgets.pop(self)
        self.deleteLater()

    def __create_actions(self):
        self.add_wire_action = QAction("Добавить провод", self)
        self.add_wire_action.triggered.connect(self.add_wire)
        self.set_name_action = QAction("Изменить имя", self)
        self.set_name_action.triggered.connect(self.set_name)
        self.del_action = QAction("Удалить", self)
        self.del_action.triggered.connect(self.delete)

    def show_context_menu(self, position):
        context_menu = QMenu(self)
        context_menu.setStyleSheet("background-color: gray;")
        if not self.wire:
            context_menu.addAction(self.add_wire_action)
        context_menu.addAction(self.set_name_action)
        context_menu.addAction(self.del_action)
        if not self.parent().rendered_wire:
            context_menu.exec(self.mapToGlobal(position))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(self.color)
        painter.setPen(self.border)

        # Рисуем круг в центре виджета
        rect = self.rect()
        diameter = min(rect.width(), rect.height())
        painter.drawEllipse((rect.width() - diameter) // 2, (rect.height() - diameter) // 2, diameter, diameter)

    def lock(self):
        self.border = QPen(Qt.black)
        self.border.setWidth(1)
        self.color = QColor(0, 255, 0)
        self.connected_widget.lock()
        self.update()

    def unlock(self):
        self.border = Qt.NoPen
        self.color = QColor(255, 0, 0)
        try:
            self.connected_widget.unlock()
        except Exception:
            pass
        self.update()

    def set_pin_connection(self, pin_connection):
        self.pin_connection = pin_connection

    def set_graphics_model(self, graphics_model):
        self.graphics_model = graphics_model

    def calc_distance(self, a: QPoint, b: QPoint):
        return ((a.x() - b.x())**2 + (a.y() - b.y())**2)**0.5

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            wire = self.parent().rendered_wire
            if wire:
                pos_in_conn_widget = self.pos() - self.connected_widget.pos()
                pin_direction = Direction.vertical
                delta = QPoint(width_wire // 2 + 1, 0)
                if (pos_in_conn_widget in self.pin_possible_move_points.left) \
                        or (pos_in_conn_widget in self.pin_possible_move_points.right):
                    pin_direction = Direction.horizontal
                    delta = QPoint(0, width_wire // 2 + 1)
                if self.wire or pin_direction != wire.direction:
                    return
                wire.connected_pins.append(self)
                wire.set_location(point=self.pos() + self.offset)
                pos = self.pos()
                pin_start_distance = self.calc_distance(self.pos() + self.offset, wire.start)
                pin_end_distance = self.calc_distance(self.pos() + self.offset, wire.end)
                if pin_end_distance < pin_start_distance:
                    self.move(wire.end - self.offset + delta)
                else:
                    self.move(wire.start - self.offset + delta)
                self.wire = wire
                self.parent().rendered_wire = None
                self.lock()
            else:
                QCursor.setPos(self.mapToGlobal(self.offset))
                self.dragging = True

    def mouseMoveEvent(self, event):
        if self.dragging and not self.wire:
            new_pos = self.pin_possible_move_points.all[0]
            min_distance = math.inf
            for point in self.pin_possible_move_points.all:
                distance = self.calc_distance(self.connected_widget.pos() + point, self.pos() + event.pos() - self.offset)
                if distance < min_distance:
                    new_pos = point
                    min_distance = distance
            self.move(self.connected_widget.pos() + new_pos)
        else:
            new_event = QMouseEvent(event.type(),
                                    event.pos() + self.pos(),
                                    event.screenPos(),
                                    event.button(),
                                    event.buttons(),
                                    event.modifiers())
            self.parent().mouseMoveEvent(new_event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False

    def set_name(self):
        pass

    def delete(self):
        self.connected_widget.pin_widgets.remove(self)
        self.connected_widget.unlock()
        self.destructor()

    def add_wire(self):
        pos_in_conn_widget = self.pos() - self.connected_widget.pos()
        direction = Direction.vertical
        delta = QPoint(width_wire // 2 + 1, 0)
        if (pos_in_conn_widget in self.pin_possible_move_points.left) \
                or (pos_in_conn_widget in self.pin_possible_move_points.right):
            direction = Direction.horizontal
            delta = QPoint(0, width_wire // 2 + 1)
        pos = self.pos() + self.offset - delta
        self.wire = WireWidget(self.parent(), pos, pos, direction, self)
        self.wire.lower()
        self.parent().rendered_wire = self.wire
        self.wire.show()
        self.lock()