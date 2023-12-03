from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QColor, QMouseEvent, QCursor
from PyQt5.QtWidgets import QWidget, QAction, QMenu

from gui.direction_enum import Direction
from settings import crossroad_width, crossroad_height, width_wire, rendering_widget_width, rendering_widget_height


class CrossroadWidget(QWidget):
    def __init__(self, parent, wires: list, pos: QPoint):
        super(CrossroadWidget, self).__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setFixedWidth(crossroad_width)
        self.setFixedHeight(crossroad_height)
        self.setStyleSheet("border: 1px black;")
        self.connected_wires = wires
        self.offset = QPoint(
            self.width() // 2,
            self.height() // 2
        )
        self.move(pos)
        self.__create_actions()

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        self.dragging = False

    def __create_actions(self):
        self.add_wire_action = QAction("Добавить провод", self)
        self.add_wire_action.triggered.connect(self.add_wire)
        self.del_action = QAction("Удалить", self)
        self.del_action.triggered.connect(self.single_delete)

    def show_context_menu(self, position):
        context_menu = QMenu(self)
        context_menu.setStyleSheet("background-color: gray;")
        if len(self.connected_wires) <= 4:
            context_menu.addAction(self.add_wire_action)
        context_menu.addAction(self.del_action)
        if not self.parent().rendered_wire:
            context_menu.exec(self.mapToGlobal(position))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(0, 0, 0))
        painter.setPen(Qt.NoPen)

        # Рисуем круг в центре виджета
        rect = self.rect()
        diameter = min(rect.width(), rect.height())
        painter.drawEllipse((rect.width() - diameter) // 2, (rect.height() - diameter) // 2, diameter, diameter)

    def add_wire(self):
        count_vertical_wires = 0
        for wire_widget in self.connected_wires:
            if wire_widget.direction == Direction.vertical:
                count_vertical_wires += 1
        direction = Direction.vertical
        delta = QPoint(width_wire // 2 + 1, 0)
        if count_vertical_wires == 2:
            direction = Direction.horizontal
            delta = QPoint(0, width_wire // 2 + 1)

        pos = self.pos() + self.offset - delta
        new_wire = self.parent().add_wire(
            start=pos,
            end=pos,
            direction=direction,
            connected_pins=[],
            connected_crossroads=[self]
        )
        self.connected_wires.append(new_wire)
        new_wire.lower()
        self.parent().rendered_wire = new_wire


    def single_delete(self):
        print('single')
        if len(self.connected_wires) != 2:
            print('Не удалось совершить single_delete для crossroad_widget, проводов != 2')
            return
        if self.connected_wires[0].direction != self.connected_wires[1].direction:
            print('Не удалось совершить single_delete для crossroad_widget, разные direction')
            return

        wire1 = self.connected_wires[0]
        wire2 = self.connected_wires[1]
        wire1.connected_crossroads.remove(self)
        wire2.connected_crossroads.remove(self)

        start, end = QPoint(), QPoint
        if wire1.direction == Direction.horizontal:
            if wire1.start.x() < wire2.start.x():
                start, end = wire1.start, wire2.end
            else:
                start, end = wire2.start, wire1.end
        else:
            if wire1.start.y() < wire2.start.y():
                start, end = wire1.start, wire2.end
            else:
                start, end = wire2.start, wire1.end

        merge_wire = self.parent().add_wire(
            start=start,
            end=end,
            direction=wire1.direction,
            connected_pins=[],
            connected_crossroads=[]
        )
        merge_wire.set_location(merge_wire.end)

        for wire_widget in wire1.connected_wires:
            wire_widget.connected_wires.remove(wire1)
            wire_widget.connected_wires.append(merge_wire)
            merge_wire.connected_wires.append(wire_widget)

        for pin_widget in wire1.connected_pins:
            pin_widget.wire = merge_wire
            merge_wire.connected_pins.append(pin_widget)

        for crossroad_widget in wire1.connected_crossroads:
            crossroad_widget.connected_wires.remove(wire1)
            crossroad_widget.connected_wires.append(merge_wire)
            merge_wire.connected_crossroads.append(crossroad_widget)

        for wire_widget in wire2.connected_wires:
            wire_widget.connected_wires.remove(wire2)
            wire_widget.connected_wires.append(merge_wire)
            merge_wire.connected_wires.append(wire_widget)

        for pin_widget in wire2.connected_pins:
            pin_widget.wire = merge_wire
            merge_wire.connected_pins.append(pin_widget)

        for crossroad_widget in wire2.connected_crossroads:
            crossroad_widget.connected_wires.remove(wire2)
            crossroad_widget.connected_wires.append(merge_wire)
            merge_wire.connected_crossroads.append(crossroad_widget)

        wire1.clear()
        wire1.delete()

        wire2.clear()
        wire2.delete()

        self.connected_wires.clear()
        if self in self.parent().all_crossroad_widgets:
            self.parent().all_crossroad_widgets.pop(self)
        self.deleteLater()

    def cascade_delete(self):
        print('cascade')
        if len(self.connected_wires) == 1:
            self.connected_wires[0].connected_crossroads.remove(self)
            self.connected_wires[0].delete()
        elif len(self.connected_wires) == 2 and \
                self.connected_wires[0].direction != self.connected_wires[1].direction:
            wire1, wire2 = self.connected_wires

            wire1.connected_crossroads.remove(self)
            wire1.connected_wires.append(wire2)

            wire2.connected_crossroads.remove(self)
            wire2.connected_wires.append(wire1)
        else:
            return

        self.connected_wires.clear()
        if self in self.parent().all_crossroad_widgets:
            self.parent().all_crossroad_widgets.pop(self)
        self.deleteLater()

    def connect_wire(self, event):
        wire = self.parent().rendered_wire

        count_vertical_wires = 0
        count_horizontal_wires = 0
        for wire_widget in self.connected_wires:
            if wire_widget.direction == Direction.vertical:
                count_vertical_wires += 1
            elif wire_widget.direction == Direction.horizontal:
                count_horizontal_wires += 1

        if (wire.direction == Direction.horizontal and count_horizontal_wires < 2) \
                or (wire.direction == Direction.vertical and count_vertical_wires < 2):
            self.connected_wires.append(wire)
            wire.move_wire(self.pos() + self.offset - wire.offset)
            wire.set_location(self.pos() + self.offset)
            wire.connected_crossroads.append(self)
            self.parent().rendered_wire = None

    def mousePressEvent(self, event):
        if self.parent().rendered_wire:
            self.connect_wire(event)
            return

        if event.button() == Qt.LeftButton:
            QCursor.setPos(self.mapToGlobal(self.offset))
            if len(self.connected_wires) == 2:
                self.dragging = True
                point = self.pos() + self.offset
                for wire in self.connected_wires:
                    wire.determine_se(point)

    def mouseMoveEvent(self, event):
        if self.parent().rendered_wire:
            self.parent().mouseMoveEvent(event.pos() + self.pos())
            return

        if self.dragging:
            x_possible = (
                min(self.connected_wires[0].start.x(), self.connected_wires[1].start.x()),
                max(self.connected_wires[0].end.x(), self.connected_wires[1].end.x())
            )
            y_possible = (
                min(self.connected_wires[0].start.y(), self.connected_wires[1].start.y()),
                max(self.connected_wires[0].end.y(), self.connected_wires[1].end.y())
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


            if self.connected_wires[0].direction == Direction.horizontal:
                self.move(new_pos.x(), self.y())
            elif self.connected_wires[0].direction == Direction.vertical:
                self.move(self.x(), new_pos.y())

            point = self.pos() + self.offset

            for wire in self.connected_wires:
                wire.set_location(point=point)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
