from parser import *
from utils import *
from coder import *

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

with open("file.json", 'w') as f:
    json.dump(valid_data, f)

dict = parse("file.json")
print(dict['main'].get_objects())

scheme_to_json(dict, 'file2.json')