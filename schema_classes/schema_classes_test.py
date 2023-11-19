import unittest

from schema_classes.schema_classes import BaseGraphicsModel, Pin, PinNet, Primitive, Object, Block


class TestBaseGraphicsModel(unittest.TestCase):

    def test_base_graphics_model(self):
        base_model = BaseGraphicsModel(top_left=(0, 0), width=10, height=20)
        self.assertEqual(base_model.get_top_left(), (0, 0))
        self.assertEqual(base_model.get_width(), 10)
        self.assertEqual(base_model.get_height(), 20)

        base_model.set_top_left((1, 1))
        base_model.set_width(15)
        base_model.set_height(25)
        self.assertEqual(base_model.get_top_left(), (1, 1))
        self.assertEqual(base_model.get_width(), 15)
        self.assertEqual(base_model.get_height(), 25)


class TestPin(unittest.TestCase):

    def test_pin(self):
        pin = Pin(name="test_pin", top_left=(0, 0))
        self.assertEqual(pin.get_name(), "test_pin")
        self.assertEqual(pin.get_top_left(), (0, 0))

        pin.set_name("new_name")
        pin.set_top_left((1, 1))
        self.assertEqual(pin.get_name(), "new_name")
        self.assertEqual(pin.get_top_left(), (1, 1))


class TestPinNet(unittest.TestCase):

    def test_pin_net(self):
        pin1 = Pin(name="pin1", top_left=(0, 0))
        pin2 = Pin(name="pin2", top_left=(1, 1))
        pins = [pin1, pin2]

        lines = [[(0, 0), (1, 1)]]
        pin_net = PinNet(name="test_pin_net", pins=pins, lines=lines)

        self.assertEqual(pin_net.get_name(), "test_pin_net")
        self.assertEqual(pin_net.get_pins(), pins)
        self.assertEqual(pin_net.get_lines(), lines)

        pin_net.set_name("new_pin_net")
        new_pin = Pin(name="new_pin", top_left=(2, 2))
        new_pins = [new_pin]
        new_lines = [[(2, 2)]]
        pin_net.set_pins(new_pins)
        pin_net.set_lines(new_lines)

        self.assertEqual(pin_net.get_name(), "new_pin_net")
        self.assertEqual(pin_net.get_pins(), new_pins)
        self.assertEqual(pin_net.get_lines(), new_lines)


class TestPrimitive(unittest.TestCase):

    def test_primitive(self):
        pin = Pin(name="test_pin", top_left=(0, 0))
        primitive = Primitive(name="test_primitive", pins=[pin], top_left=(0, 0), width=10, height=20, link='')

        self.assertEqual(primitive.get_name(), "test_primitive")
        self.assertEqual(primitive.get_pins(), [pin])
        self.assertEqual(primitive.get_link(), '')

        primitive.set_name("new_primitive")
        new_pin = Pin(name="new_pin", top_left=(1, 1))
        new_pins = [new_pin]
        primitive.set_pins(new_pins)
        primitive.set_link("new_link")

        self.assertEqual(primitive.get_name(), "new_primitive")
        self.assertEqual(primitive.get_pins(), new_pins)
        self.assertEqual(primitive.get_link(), "new_link")


class TestObject(unittest.TestCase):

    def test_object(self):
        obj = Object(name="test_object", object_type="primitive", link="object_link", top_left=(0, 0), width=10,
                     height=20)

        self.assertEqual(obj.get_name(), "test_object")
        self.assertEqual(obj.get_object_type(), "primitive")
        self.assertEqual(obj.get_link(), "object_link")

        obj.set_name("new_object")
        obj.set_object_type("block")
        obj.set_link("new_object_link")

        self.assertEqual(obj.get_name(), "new_object")
        self.assertEqual(obj.get_object_type(), "block")
        self.assertEqual(obj.get_link(), "new_object_link")


class TestBlock(unittest.TestCase):

    def test_block(self):
        pin = Pin(name="test_pin", top_left=(0, 0))
        obj = Object(name="test_object", object_type="primitive", link="object_link", top_left=(0, 0), width=10,
                     height=20)
        pin_net = PinNet(name="test_pin_net", pins=[pin], lines=[[(0, 0), (1, 1)]])

        block = Block(name="test_block", pins=[pin], objects=[obj], pin_nets=[pin_net], top_left=(0, 0), width=10,
                      height=20, link='block_link')

        self.assertEqual(block.get_name(), "test_block")
        self.assertEqual(block.get_pins(), [pin])
        self.assertEqual(block.get_objects(), [obj])
        self.assertEqual(block.get_pin_nets(), [pin_net])
        self.assertEqual(block.get_link(), "block_link")

        block.set_name("new_block")
        new_pin = Pin(name="new_pin", top_left=(1, 1))
        new_obj = Object(name="new_object", object_type="block", link="new_object_link", top_left=(1, 1), width=15,
                         height=25)
        new_pin_net = PinNet(name="new_pin_net", pins=[new_pin], lines=[[(1, 1), (2, 2)]])

        block.set_pins([new_pin])
        block.set_objects([new_obj])
        block.set_pin_nets([new_pin_net])
        block.set_link("new_block_link")

        self.assertEqual(block.get_name(), "new_block")
        self.assertEqual(block.get_pins(), [new_pin])
        self.assertEqual(block.get_objects(), [new_obj])
        self.assertEqual(block.get_pin_nets(), [new_pin_net])
        self.assertEqual(block.get_link(), "new_block_link")


if __name__ == '__main__':
    unittest.main()
