from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QWidget, QAction, QMenu

from gui.direction_enum import Direction
from settings import crossroad_width, crossroad_height, width_wire


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
            connected_pins=wire1.connected_pins + wire2.connected_pins,
            connected_crossroads=wire1.connected_crossroads + wire2.connected_crossroads
        )
        merge_wire.set_location(merge_wire.end)

        for wire_widget in wire1.connected_wires:
            wire_widget.connected_wires.remove(wire1)
            wire_widget.connected_wires.append(merge_wire)
            merge_wire.connected_wires.append(wire_widget)

        for wire_widget in wire2.connected_wires:
            wire_widget.connected_wires.remove(wire2)
            wire_widget.connected_wires.append(merge_wire)
            merge_wire.connected_wires.append(wire_widget)

        wire1.connected_wires.clear()
        wire1.connected_pins.clear()
        wire1.connected_crossroads.clear()
        wire1.delete()

        wire2.connected_wires.clear()
        wire2.connected_pins.clear()
        wire2.connected_crossroads.clear()
        wire2.delete()

        self.connected_wires.clear()
        self.deleteLater()

    def cascade_delete(self):
        if len(self.connected_wires) == 1:
            self.connected_wires[0].connected_crossroads.remove(self)
            self.connected_wires[0].delete()
        elif len(self.connected_wires) == 2:
            wire1, wire2 = self.connected_wires
            wire1.connected_crossroads.remove(self)
            wire1.connected_wires.append(wire2)

            wire2.connected_crossroads.remove(self)
            wire2.connected_wires.append(wire1)
        elif len(self.connected_wires) == 3:
            return

        self.connected_wires.clear()
        self.deleteLater()
