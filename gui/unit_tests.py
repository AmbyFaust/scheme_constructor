import unittest
from PyQt5.QtCore import QPoint
from rendering_widget import RenderingWidget
from gui.wire_widget import Direction


class TestRenderingWidgetFunctions(unittest.TestCase):
    rendering_widget = None

    def setUp(self):
        self.rendering_widget = RenderingWidget()

    def test_add_primitive(self):
        primitive_widget = self.rendering_widget.add_primitive()
        self.assertIn(primitive_widget, self.rendering_widget.primitives_widgets)

    def test_del_primitive(self):
        primitive_widget = self.rendering_widget.add_primitive()
        primitive_widget.delete()
        self.assertNotIn(primitive_widget, self.rendering_widget.primitives_widgets)

    def test_add_block(self):
        block_widget = self.rendering_widget.add_block()
        self.assertIn(block_widget, self.rendering_widget.block_widgets)

    def test_del_block(self):
        block_widget = self.rendering_widget.add_block()
        block_widget.delete()
        self.assertNotIn(block_widget, self.rendering_widget.block_widgets)

    def test_add_pin(self):
        connect_widget = self.rendering_widget.add_primitive()
        pin_widget = self.rendering_widget.add_pin(connect_widget)
        self.assertIn(pin_widget, self.rendering_widget.pin_widgets)
        self.assertIn(pin_widget, connect_widget.pin_widgets)

    def test_del_pin(self):
        connect_widget = self.rendering_widget.add_primitive()
        pin_widget = self.rendering_widget.add_pin(connect_widget)
        pin_widget.delete()
        self.assertNotIn(pin_widget, self.rendering_widget.pin_widgets)
        self.assertNotIn(pin_widget, connect_widget.pin_widgets)

    def test_add_wire(self):
        start_point = QPoint(0, 0)
        end_point = QPoint(50, 50)
        direction = Direction.horizontal
        wire_widget = self.rendering_widget.add_wire(start_point, end_point, direction, [], [])
        self.assertIn(wire_widget, self.rendering_widget.wire_widgets)

    def test_del_wire(self):
        start_point = QPoint(0, 0)
        end_point = QPoint(50, 50)
        direction = Direction.horizontal
        wire_widget = self.rendering_widget.add_wire(start_point, end_point, direction, [], [])
        wire_widget.delete()
        self.assertNotIn(wire_widget, self.rendering_widget.wire_widgets)

    def test_add_crossroad(self):
        wires = []
        pos = QPoint(50, 50)
        crossroad_widget = self.rendering_widget.add_crossroad(wires, pos)
        self.assertIn(crossroad_widget, self.rendering_widget.crossroad_widgets)

    def test_cascade_del_crossroad(self):
        wires = []
        pos = QPoint(50, 50)
        crossroad_widget = self.rendering_widget.add_crossroad(wires, pos)
        crossroad_widget.cascade_delete()
        self.assertNotIn(crossroad_widget, self.rendering_widget.crossroad_widgets)

    def test_single_del_crossroad(self):
        wires = []
        pos = QPoint(50, 50)
        crossroad_widget = self.rendering_widget.add_crossroad(wires, pos)
        crossroad_widget.single_delete()
        self.assertNotIn(crossroad_widget, self.rendering_widget.crossroad_widgets)


if __name__ == '__main__':
    unittest.main()
