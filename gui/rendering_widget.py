import random

from PyQt5.QtCore import Qt, QPoint, pyqtSlot
from PyQt5.QtGui import QCursor, QMouseEvent
from PyQt5.QtWidgets import QWidget, QMenu, QAction

from schema_classes.schema_classes import Primitive, Block, Pin
from gui.block_widget import BlockWidget
from gui.crossroad_widget import CrossroadWidget
from gui.pin_widget import PinWidget
from gui.primitive_widget import PrimitiveWidget
from gui.wire_widget import Direction, WireWidget
from settings import block_width, block_height, rendering_widget_width, rendering_widget_height, width_wire, pin_width, \
    pin_height, primitive_width, primitive_height


class RenderingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("border: 2px solid black;")  # Устанавливаем стиль с обводкой
        self.setFixedWidth(rendering_widget_width)
        self.setFixedHeight(rendering_widget_height)

        self.all_primitive_widgets = {}
        self.all_block_widgets = {}
        self.all_pin_widgets = {}
        self.all_wire_widgets = {}
        self.all_crossroad_widgets = {}

        self.pin_widgets = []

        self.rendered_wire = None

        self.__create_actions()

        # self.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.customContextMenuRequested.connect(self.show_context_menu)

        self.setMouseTracking(True)

    def __create_actions(self):
        self.add_pin_action = QAction("Добавить внешний Пин", self)
        self.add_pin_action.triggered.connect(self.add_external_pin)

    def show_context_menu(self, position):
        context_menu = QMenu(self)
        context_menu.setStyleSheet("background-color: gray;")
        context_menu.addAction(self.add_pin_action)
        if not self.rendered_wire:
            context_menu.exec(self.mapToGlobal(position))

    def get_pin_names(self):
        return [pin_.pin.get_name() for pin_ in self.all_pin_widgets]

    def get_primitive_names(self):
        return [prim_.primitive.get_name() for prim_ in self.all_primitive_widgets]

    def get_block_names(self):
        return [block_.block.get_name() for block_ in self.all_block_widgets]

    def gen_name(self, name, existed_names):
        name = name + str(random.randrange(10))
        while name in existed_names:
            name = name + str(random.randrange(10))
        return name
    def add_external_pin(self):
        self.add_pin(self)

    @pyqtSlot(object)
    def add_object_from_panel(self, object_wid):
        if object_wid:
            object_wid.setParent(self)
            object_wid.move(50, 50)
            object_wid.show()
            for pin in object_wid.pin_widgets:
                pin.setParent(self)
                pin.move(object_wid.pos() + pin.pos() + QPoint(object_wid.width(), 0))
                pin.show()
                self.all_pin_widgets[pin] = True
            if isinstance(object_wid, PrimitiveWidget):
                self.all_primitive_widgets[object_wid] = True
            elif isinstance(object_wid, BlockWidget):
                self.all_block_widgets[object_wid] = True
    def add_primitive(self, primitive: Primitive = None, pins: list[Pin] = None):
        if not primitive:
            primitive = Primitive(
                self.gen_name('primitive', self.get_primitive_names()), [], (0, 100), primitive_width, primitive_height
            )
        primitive_widget = PrimitiveWidget(self, primitive, pins)
        primitive_widget.show()
        self.all_primitive_widgets[primitive_widget] = True
        return primitive_widget

    def add_block(self, block: Block = None, pins: list[Pin] = None):
        if not block:
            block = Block(
                self.gen_name('block', self.get_block_names()), [], [], [], (0, 0), block_width, block_height
            )
        block_widget = BlockWidget(self, block, pins)
        block_widget.show()
        self.all_block_widgets[block_widget] = True
        return block_widget

    def add_pin(self, connect_widget, pin: Pin = None):
        print(f"Pin widgets: {self.pin_widgets}")
        for pin_ in self.all_pin_widgets:
            print(f"Pin: {pin_.pin.get_name()}")

        for prim_ in self.all_primitive_widgets:
            for pin_ in prim_.pin_widgets:
                print(f"Pins from Primitives: {pin_.pin.get_name()}")

        for wire_ in self.all_wire_widgets:
            for pin_ in wire_.connected_pins:
                print(f"Pins from Wires: {pin_.pin.get_name()}")

        if not pin:
            top_left = (
                connect_widget.y() + connect_widget.height() - pin_height // 2,
                connect_widget.x() + connect_widget.width() // 2 - pin_width // 2,
            )
            print(f"Type of base obj, to what want add Pin {type(connect_widget)}")
            pin = Pin('', top_left)

            if not connect_widget == self:
                pin.set_name(self.gen_name(connect_widget.primitive.get_name()+'.', self.get_pin_names()))

        if connect_widget == self:
            top_left = pin.get_top_left()
            top_left = (
                top_left[0] - connect_widget.y() - pin_width // 2,
                top_left[1] - connect_widget.x()
            )
            pin.set_top_left(top_left)
            pin.set_name(self.gen_name('ext', self.get_pin_names()))

        pin_widget = PinWidget(self, pin, connect_widget)
        connect_widget.pin_widgets.append(pin_widget)
        pin_widget.show()
        self.all_pin_widgets[pin_widget] = True
        return pin_widget

    def add_wire(self, start: QPoint, end: QPoint, direction: Direction,
                 connected_pins: list, connected_crossroads: list):
        wire_widget = WireWidget(self, start, end, direction, connected_pins, connected_crossroads)
        self.all_wire_widgets[wire_widget] = True
        wire_widget.lower()
        wire_widget.show()
        return wire_widget

    def add_crossroad(self, wires: list, pos: QPoint):
        crossroad_widget = CrossroadWidget(self, wires, pos)
        self.all_crossroad_widgets[crossroad_widget] = True
        crossroad_widget.show()
        return crossroad_widget

    def mousePressEvent(self, event):
        print('--------')
        print('primitives:', len(self.all_primitive_widgets))
        print('blocks:', len(self.all_block_widgets))
        print('pins:', len(self.all_pin_widgets))
        print('wires:', len(self.all_wire_widgets))
        print('crossroads:', len(self.all_crossroad_widgets))
        if event.button() == Qt.LeftButton and self.rendered_wire:
            for pin_widget in self.all_pin_widgets:
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

        elif event.button() == Qt.RightButton and not self.rendered_wire:
            self.show_context_menu(event.pos())

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


