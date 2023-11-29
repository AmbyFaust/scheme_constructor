import unittest
import json
from schema_classes import Pin, Primitive, Block, PinNet, Object
from coder import converting_to_json, code_pins, code_pin_nets, code_objects, scheme_to_json


class TestSchemeToJson(unittest.TestCase):

    def setUp(self):
        self.pin1 = Pin(name="pin1", top_left=(0, 0))
        self.pin2 = Pin(name="pin2", top_left=(1, 1))

        self.pin_net1 = PinNet(name="pin_net1", pins=[self.pin1], lines=[[(0, 0), (1, 1)]])
        self.pin_net2 = PinNet(name="pin_net2", pins=[self.pin2], lines=[[(2, 2), (3, 3)]])

        self.primitive1 = Primitive(name="primitive1", pins=[self.pin1], top_left=(0, 0), width=10, height=20, link='link1')
        self.primitive2 = Primitive(name="primitive2", pins=[self.pin2], top_left=(1, 1), width=15, height=25, link='link2')

        self.object1 = Object(name="object1", object_type="block", link='link3', top_left=(0, 0), width=10, height=20)
        self.object2 = Object(name="object2", object_type="primitive", link='link4', top_left=(1, 1), width=15, height=25)

        self.block = Block(name="block1", pins=[self.pin1], objects=[self.object1, self.object2], pin_nets=[self.pin_net1, self.pin_net2], top_left=(0, 0), width=30, height=50, link='link5')

        self.schema = [self.primitive1, self.object1, self.block]

    def test_converting_to_json(self):
        data = {'key': 'value'}
        result = converting_to_json(data)
        self.assertEqual(result, json.dumps(data))

    def test_code_pins(self):
        pins = [self.pin1, self.pin2]
        result = code_pins(pins)
        expected_result = [{'name': 'pin1', 'top_left': (0, 0)}, {'name': 'pin2', 'top_left': (1, 1)}]
        self.assertEqual(result, expected_result)

    def test_code_pin_nets(self):
        pin_nets = [self.pin_net1, self.pin_net2]
        result = code_pin_nets(pin_nets)
        expected_result = [
            {'name': 'pin_net1', 'pins': [{'name': 'pin1', 'top_left': (0, 0)}], 'lines': [[(0, 0), (1, 1)]]},
            {'name': 'pin_net2', 'pins': [{'name': 'pin2', 'top_left': (1, 1)}], 'lines': [[(2, 2), (3, 3)]]}
        ]
        self.assertEqual(result, expected_result)

    def test_code_objects(self):
        objects = [self.primitive1, self.object1]
        result = code_objects(objects)
        expected_result = [
            {'type': 'primitive', 'name': 'primitive1', 'top_left': (0, 0), 'width': 10, 'height': 20, 'pins': [{'name': 'pin1', 'top_left': (0, 0)}], 'link': 'link1'},
            {'type': 'block', 'name': 'object1', 'top_left': (0, 0), 'width': 10, 'height': 20, 'pins': [{'name': 'pin1', 'top_left': (0, 0)}]}
        ]
        self.assertEqual(result, expected_result)

    def test_scheme_to_json(self):
        filename = "test_output.json"
        scheme_to_json(self.schema, filename)
