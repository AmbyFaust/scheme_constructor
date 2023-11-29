from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QCursor, QMouseEvent
from PyQt5.QtWidgets import QWidget

from core.schema_classes import Primitive, Block
from gui.block_widget import BlockWidget
from gui.crossroad_widget import CrossroadWidget
from gui.pin_widget import PinWidget
from gui.primitive_widget import PrimitiveWidget
from gui.wire_widget import Direction, WireWidget
from settings import block_width, block_height, rendering_widget_width, rendering_widget_height, width_wire


class RenderingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("border: 2px solid black;")  # Устанавливаем стиль с обводкой
        self.setFixedWidth(rendering_widget_width)
        self.setFixedHeight(rendering_widget_height)

        self.primitives_widgets = {}
        self.block_widgets = {}
        self.pin_widgets = {}
        self.wire_widgets = {}
        self.crossroad_widgets = {}

        self.rendered_wire = None

        self.setMouseTracking(True)

    def add_primitive(self, primitive: Primitive = None):
        if not primitive:
            primitive = Primitive('primitive', [], (50, 100), 100, 50)
        primitive_widget = PrimitiveWidget(self, primitive)
        primitive_widget.show()
        self.primitives_widgets[primitive_widget] = True
        return primitive_widget

    def add_block(self, block: Block = None):
        if not block:
            block = Block('block', [], [], [], (100, 100), block_width, block_height)
        block_widget = BlockWidget(self, block)
        block_widget.show()
        self.block_widgets[block_widget] = True
        return block_widget

    def add_pin(self, connect_widget):
        pin_widget = PinWidget(self, connect_widget)
        connect_widget.pin_widgets.append(pin_widget)
        pin_widget.show()
        self.pin_widgets[pin_widget] = True
        return pin_widget

    def add_wire(self, start: QPoint, end: QPoint, direction: Direction,
                 connected_pins: list, connected_crossroads: list):
        wire_widget = WireWidget(self, start, end, direction, connected_pins, connected_crossroads)
        self.wire_widgets[wire_widget] = True
        wire_widget.lower()
        wire_widget.show()
        return wire_widget

    def add_crossroad(self, wires: list, pos: QPoint):
        crossroad_widget = CrossroadWidget(self, wires, pos)
        self.crossroad_widgets[crossroad_widget] = True
        crossroad_widget.show()
        return crossroad_widget

    def mousePressEvent(self, event):
        print('--------')
        print('primitives:', len(self.primitives_widgets))
        print('blocks:', len(self.block_widgets))
        print('pins:', len(self.pin_widgets))
        print('wires:', len(self.wire_widgets))
        print('crossroads:', len(self.crossroad_widgets))
        if event.button() == Qt.LeftButton and self.rendered_wire:
            for pin_widget in self.pin_widgets:
                if pin_widget.geometry().contains(event.pos()):
                    new_event = QMouseEvent(event.type(),
                                            event.pos() - pin_widget.pos(),
                                            event.screenPos(),
                                            event.button(),
                                            event.buttons(),
                                            event.modifiers())
                    pin_widget.mousePressEvent(new_event)
                    return


            self.rendered_wire.drawing = False
            delta = QPoint()

            if self.rendered_wire.direction == Direction.horizontal:
                delta = QPoint(width_wire // 2 + 1, 0)
            elif self.rendered_wire.direction == Direction.vertical:
                delta = QPoint(0, width_wire // 2 + 1)
            pos = event.pos() - delta
            next_wire = self.add_wire(
                start=pos,
                end=pos,
                direction=Direction.get_another(self.rendered_wire.direction),
                connected_pins=[],
                connected_crossroads=[]
            )
            self.rendered_wire.connected_wires.append(next_wire)
            next_wire.connected_wires.append(self.rendered_wire)
            self.rendered_wire = next_wire

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
            point = QPoint(event.x(), event.y())
            self.rendered_wire.set_location(point=point)

