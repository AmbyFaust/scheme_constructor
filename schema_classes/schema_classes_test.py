import unittest
from schema_classes import *


class TestGraphicsModels(unittest.TestCase):

    def test_base_graphics_model(self):
        model = BaseGraphicsModel((0, 0), 10, 20)
        self.assertEqual(model.get_top_left(), (0, 0))
        model.set_top_left((1, 1))
        self.assertEqual(model.get_top_left(), (1, 1))
        self.assertEqual(model.get_width(), 10)
        model.set_width(15)
        self.assertEqual(model.get_width(), 15)
        self.assertEqual(model.get_height(), 20)
        model.set_height(25)
        self.assertEqual(model.get_height(), 25)

    def test_pin(self):
        pin = Pin("pin1", (0, 0))
        self.assertEqual(pin.get_name(), "pin1")
        pin.set_name("pin2")
        self.assertEqual(pin.get_name(), "pin2")
        self.assertEqual(pin.get_top_left(), (0, 0))
        pin.set_top_left((1, 1))
        self.assertEqual(pin.get_top_left(), (1, 1))

    def test_pin_net(self):
        pin1 = Pin("pin1", (0, 0))
        pin2 = Pin("pin2", (1, 1))
        pin_net = PinNet("pin_net", [pin1, pin2], [[(0, 0), (1, 1)]])
        self.assertEqual(pin_net.get_name(), "pin_net")
        pin_net.set_name("new_pin_net")
        self.assertEqual(pin_net.get_name(), "new_pin_net")
        self.assertEqual(pin_net.get_pins(), [pin1, pin2])
        new_pins = [Pin("pin3", (2, 2)), Pin("pin4", (3, 3))]
        pin_net.set_pins(new_pins)
        self.assertEqual(pin_net.get_pins(), new_pins)
        self.assertEqual(pin_net.get_lines(), [[(0, 0), (1, 1)]])
        new_lines = [[(2, 2), (3, 3)], [(4, 4), (5, 5)]]
        pin_net.set_lines(new_lines)
        self.assertEqual(pin_net.get_lines(), new_lines)

    def test_primitive(self):
        pin1 = Pin("pin1", (0, 0))
        pin2 = Pin("pin2", (1, 1))
        pins = [pin1, pin2]
        primitive = Primitive("primitive", pins, (0, 0), 10, 20, link="link1")
        self.assertEqual(primitive.get_name(), "primitive")
        primitive.set_name("new_primitive")
        self.assertEqual(primitive.get_name(), "new_primitive")
        self.assertEqual(primitive.get_pins(), pins)
        new_pins = [Pin("pin3", (2, 2)), Pin("pin4", (3, 3))]
        primitive.set_pins(new_pins)
        self.assertEqual(primitive.get_pins(), new_pins)
        self.assertEqual(primitive.get_link(), "link1")
        primitive.set_link("link2")
        self.assertEqual(primitive.get_link(), "link2")

    def test_object(self):
        obj = Object("object1", "primitive", "link1", (0, 0), 10, 20)
        self.assertEqual(obj.get_name(), "object1")
        obj.set_name("new_object")
        self.assertEqual(obj.get_name(), "new_object")
        self.assertEqual(obj.get_object_type(), "primitive")
        obj.set_object_type("block")
        self.assertEqual(obj.get_object_type(), "block")
        self.assertEqual(obj.get_link(), "link1")
        obj.set_link("link2")
        self.assertEqual(obj.get_link(), "link2")

    def test_block(self):
        pin1 = Pin("pin1", (0, 0))
        pin2 = Pin("pin2", (1, 1))
        pins = [pin1, pin2]
        obj1 = Object("object1", "primitive", "link1", (2, 2), 10, 20)
        obj2 = Object("object2", "block", "link2", (3, 3), 15, 25)
        objects = [obj1, obj2]
        pin_net1 = PinNet("pin_net1", [pin1, pin2], [[(0, 0), (1, 1)]])
        pin_net2 = PinNet("pin_net2", [pin2], [[(1, 1), (2, 2)]])
        pin_nets = [pin_net1, pin_net2]
        block = Block("block1", pins, objects, pin_nets, (0, 0), 30, 40, link="link1")
        self.assertEqual(block.get_name(), "block1")
        block.set_name("new_block")
        self.assertEqual(block.get_name(), "new_block")
        self.assertEqual(block.get_pins(), pins)
        new_pins = [Pin("pin3", (2, 2)), Pin("pin4", (3, 3))]
        block.set_pins(new_pins)
        self.assertEqual(block.get_pins(), new_pins)
        self.assertEqual(block.get_objects(), objects)
        new_objects = [Object("object3", "primitive", "link3", (4, 4), 20, 30)]
        block.set_objects(new_objects)
        self.assertEqual(block.get_objects(), new_objects)
        self.assertEqual(block.get_pin_nets(), pin_nets)
        new_pin_nets = [PinNet("pin_net3", [pin2], [[(1, 1), (2, 2)]])]
        block.set_pin_nets(new_pin_nets)
        self.assertEqual(block.get_pin_nets(), new_pin_nets)
        self.assertEqual(block.get_link(), "link1")
        block.set_link("link2")
        self.assertEqual(block.get_link(), "link2")


if __name__ == '__main__':
    unittest.main()
