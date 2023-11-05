import math
from time import sleep

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QCursor, QMouseEvent
from PyQt5.QtWidgets import QWidget, QPushButton

from core.schema_classes import Primitive, BaseGraphicsModel, Block
from gui.block_widget import BlockWidget
from gui.pin_widget import PinWidget
from gui.primitive_widget import PrimitiveWidget
from gui.wire_widget import Direction, WireWidget
from settings import primitive_width, primitive_height, pin_width, pin_height, block_width, block_height, \
    rendering_widget_width, rendering_widget_height, width_wire


class RenderingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("border: 2px solid black;")  # Устанавливаем стиль с обводкой
        self.setFixedWidth(rendering_widget_width)
        self.setFixedHeight(rendering_widget_height)

        self.primitives_widgets = []
        self.block_widgets = []

        self.rendered_wire = None

        self.__create_widgets()
        self.setMouseTracking(True)

    def __create_widgets(self):
        pass

    def add_primitive(self, primitive: Primitive = None):
        if not primitive:
            primitive = Primitive('primitive', [], 50, 100, 100, 50)
        primitive_widget = PrimitiveWidget(self, controller=None, primitive=primitive)
        primitive_widget.show()

        self.primitives_widgets.append(primitive_widget)

    def del_primitive(self, primitive_widget: PrimitiveWidget):
        self.primitives_widgets.remove(primitive_widget)
        primitive_widget.destructor()
        primitive_widget.deleteLater()

    def add_block(self, block: Block = None):
        if not block:
            block = Block('block', [], [], 100, 100, block_width, block_height)
        block_widget = BlockWidget(self, controller=None, block=block)
        block_widget.show()

        self.block_widgets.append(block_widget)

    def del_block(self, block_widget: BlockWidget):
        self.block_widgets.remove(block_widget)
        block_widget.destructor()
        block_widget.deleteLater()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.rendered_wire:
            self.rendered_wire.drawing = False
            delta = QPoint()
            if self.rendered_wire.start.x() > self.rendered_wire.end.x():
                delta = -QPoint(width_wire // 2 + 1, 0)
            elif self.rendered_wire.start.x() < self.rendered_wire.end.x():
                delta = -QPoint(width_wire // 2 + 1, 0)
            elif self.rendered_wire.start.y() > self.rendered_wire.end.y():
                delta = -QPoint(0, width_wire // 2 + 1)
            elif self.rendered_wire.start.y() < self.rendered_wire.end.y():
                delta = -QPoint(0, width_wire // 2 + 1)
            next_wire = WireWidget(self, event.pos() + delta, Direction.get_another(self.rendered_wire.direction))
            next_wire.stackUnder(self.rendered_wire)
            self.rendered_wire.connected_wires.append(next_wire)
            next_wire.connected_wires.append(self.rendered_wire)
            next_wire.stackUnder(self.rendered_wire)
            self.rendered_wire = next_wire
            self.rendered_wire.show()

        elif event.button() == Qt.RightButton and self.rendered_wire:
            self.rendered_wire.delete()
            self.rendered_wire = None

    def mouseMoveEvent(self, event):
        if self.rendered_wire:
            last_pos_cursor_screen = QCursor.pos()
            if self.rendered_wire.direction == Direction.horizontal:
                delta_y = event.y() - self.rendered_wire.y()
                QCursor.setPos(
                    last_pos_cursor_screen.x(),
                    last_pos_cursor_screen.y() - delta_y + width_wire // 2 + 1
                )

            elif self.rendered_wire.direction == Direction.vertical:
                delta_x = event.x() - self.rendered_wire.x()
                QCursor.setPos(
                    last_pos_cursor_screen.x() - delta_x + width_wire // 2 + 1,
                    last_pos_cursor_screen.y()
                )
            end = QPoint(event.x(), event.y())
            self.rendered_wire.set_location(end=end)

