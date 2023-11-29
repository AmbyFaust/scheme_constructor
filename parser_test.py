import unittest
import os
from parser import *
from utils import *


class TestJsonParsing(unittest.TestCase):

    def setUp(self):
        self.valid_json_filename = "valid_data.json"
        self.invalid_json_filename = "invalid_data.json"

        # Creating a valid JSON file
        valid_data = [
            {
                "type": "primitive",
                "name": "valid_primitive",
                "top_left": [0, 0],
                "width": 10,
                "height": 20,
                "pins": [{"name": "pin1", "top_left": [1, 1]}]
            },
            {
                "type": "block",
                "name": "main",
                "top_left": [0, 0],
                "width": 30,
                "height": 50,
                "pins": [{"name": "pin2", "top_left": [2, 2]}],
                "objects": [
                    {
                        "type": "primitive",
                        "name": "valid_inner_primitive",
                        "link": "valid_primitive",
                        "top_left": [0, 0],
                        "width": 15,
                        "height": 25,
                        "pins": [{"name": "pin3", "top_left": [3, 3]}]
                    }
                ],
                "pin_nets": [
                    {"name": "pin_net1", "pins": {"pins": ["pin2"]}, "lines": [[(0, 0), (1, 1)]]}
                ]
            }
        ]

        with open(self.valid_json_filename, 'w') as f:
            json.dump(valid_data, f)

        # Creating an invalid JSON file
        invalid_data = [
            {"type": "invalid_type", "name": "invalid_entity", "top_left": [0, 0], "width": 10, "height": 20}
        ]

        with open(self.invalid_json_filename, 'w') as f:
            json.dump(invalid_data, f)

    def tearDown(self):
        # Clean up created files
        os.remove(self.valid_json_filename)
        os.remove(self.invalid_json_filename)

    def test_json_to_dict_valid(self):
        result = json_to_dict(self.valid_json_filename)
        self.assertEqual(len(result), 2)

    def test_dict_to_json(self):
        data = {"key": "value"}
        dict_to_json(data, "output.json")

        with open("output.json", 'r') as f:
            content = f.read()
            self.assertEqual(content, '{"key": "value"}')

    def test_is_name_valid(self):
        self.assertTrue(is_name_valid("valid_name"))
        self.assertFalse(is_name_valid("invalid name"))
        self.assertFalse(is_name_valid("123name"))
        self.assertFalse(is_name_valid("name.with.dots", dots_allowed=1))

    def test_is_type_valid(self):
        self.assertTrue(is_type_valid("block"))
        self.assertTrue(is_type_valid("primitive"))
        self.assertFalse(is_type_valid("invalid_type"))

    def test_is_number_valid(self):
        self.assertTrue(is_number_valid(42))
        self.assertTrue(is_number_valid(0))
        self.assertFalse(is_number_valid("invalid"))

    def test_parse(self):
        result = parse(self.valid_json_filename)
        self.assertEqual(len(result), 2)
        self.assertTrue(all(isinstance(entity, (Primitive, Block)) for entity in result))

    def test_parse_primitive(self):
        data = {"type": "primitive", "name": "valid_primitive", "top_left": [0, 0], "width": 10, "height": 20, "pins": [{"name": "pin1", "top_left": [1, 1]}]}
        result = parse_primitive(data)
        self.assertIsInstance(result, Primitive)

    def test_parse_block(self):
        data = {"type": "block", "name": "valid_block", "top_left": [0, 0], "width": 30, "height": 50, "pins": [{"name": "pin2", "top_left": [2, 2]}], "objects": [{"type": "primitive", "name": "valid_inner_primitive", "link": "valid_primitive", "top_left": [1, 1], "width": 15, "height": 25, "pins": [{"name": "pin3", "top_left": [3, 3]}]}], "pin_nets": [{"name": "pin_net1", "pins": {"pins": ["pin2"]}, "lines": [[(0, 0), (1, 1)]]}]}
        result = parse_block(data)
        self.assertIsInstance(result, Block)

    def test_parse_object(self):
        data = {"type": "primitive", "name": "valid_primitive", "link": "valid_primitive", "top_left": [0, 0], "width": 10, "height": 20}
        result = parse_object(data)
        self.assertIsInstance(result, Object)

    def test_parse_objects(self):
        data = {"objects": [{"type": "primitive", "name": "valid_primitive", "link": "valid_primitive", "top_left": [0, 0], "width": 10, "height": 20}]}
        result = parse_objects(data)
        self.assertTrue(all(isinstance(obj, Object) for obj in result))

    def test_parse_pin(self):
        data = {"name": "valid_pin", "top_left": [1, 1]}
        result = parse_pin(data)
        self.assertIsInstance(result, Pin)

    def test_parse_pins(self):
        data = {"pins": [{"name": "valid_pin", "top_left": [1, 1]}]}
        result = parse_pins(data)
        self.assertTrue(all(isinstance(pin, Pin) for pin in result))

    def test_parse_pin_net(self):
        data = {"name": "valid_pin_net", "pins": {"pins": ["valid_pin"]}, "lines": [[(0, 0), (1, 1)]]}
        result = parse_pin_net(data)
        self.assertIsInstance(result, PinNet)

    def test_parse_pin_nets(self):
        data = {"pin_nets": [{"name": "valid_pin_net", "pins": {"pins": ["valid_pin"]}, "lines": [[(0, 0), (1, 1)]]}]}
        result = parse_pin_nets(data)
        self.assertTrue(all(isinstance(pin_net, PinNet) for pin_net in result))

    def test_parse_top_left(self):
        data = {"top_left": [0, 0]}
        result = parse_top_left(data)
        self.assertEqual(result, (0, 0))

    def test_parse_name(self):
        data = {"name": "valid_name"}
        result = parse_name(data)
        self.assertEqual(result, "valid_name")

    def test_parse_width(self):
        data = {"width": 10}
        result = parse_width(data)
        self.assertEqual(result, 10)

    def test_parse_height(self):
        data = {"height": 20}
        result = parse_height(data)
        self.assertEqual(result, 20)

    def test_parse_link(self):
        data = {"link": "valid_link"}
        result = parse_link(data)
        self.assertEqual(result, "valid_link")

    def test_parse_type(self):
        data = {"type": "block"}
        result = parse_type(data)
        self.assertEqual(result, "block")

    def test_parse_lines(self):
        data = {"lines": [[(0, 0), (1, 1)]]}
        result = parse_lines(data)
        self.assertEqual(result, [[(0, 0), (1, 1)]])


if __name__ == '__main__':
    unittest.main()
