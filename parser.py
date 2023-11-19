from schema_classes import Pin, PinNet, Primitive, Block, Object
from utils import json_to_dict
from typing import List, Tuple


def parse(filename):
    data = json_to_dict(filename)

    main_found = False
    items = []

    try:
        for el in data:
            if parse_type(el) == 'block':
                items.append(parse_block(el))
                main_found = main_found or (parse_name(el) == 'main')
            elif parse_type(el) == 'primitive':
                items.append(parse_primitive(el))
        if not main_found:
            raise RuntimeError('Block with name \"main\" not found.')
    except KeyError as ke:
        raise KeyError(f'Key {ke} was expected but not found.')

    return items


def parse_primitive(primitive_dict) -> Primitive:
    return Primitive(
        name=parse_name(primitive_dict),
        pins=parse_pins(primitive_dict),
        top_left=parse_top_left(primitive_dict),
        width=parse_width(primitive_dict),
        height=parse_height(primitive_dict)
    )


def parse_block(block_dict) -> Block:
    return Block(
        name=parse_name(block_dict),
        pins=parse_pins(block_dict),
        objects=parse_objects(block_dict),
        pin_nets=parse_pin_nets(block_dict),
        top_left=parse_top_left(block_dict),
        width=parse_width(block_dict),
        height=parse_height(block_dict)
    )


def parse_object(object_dict) -> Object:
    return Object(
        name=parse_name(object_dict),
        object_type=parse_type(object_dict),
        link=parse_link(object_dict),
        top_left=parse_top_left(object_dict),
        width=parse_width(object_dict),
        height=parse_height(object_dict)
    )


def parse_objects(objects_dict) -> List[Object]:
    return [parse_object(object_dict) for object_dict in objects_dict['objects']]


def parse_pin(pin_dict) -> Pin:
    return Pin(name=parse_name(pin_dict), top_left=parse_top_left(pin_dict))


def parse_pins(pins_dict) -> List[Pin]:
    return [parse_pin(pin_dict) for pin_dict in pins_dict['pins']]


def parse_pin_net(pin_net_dict) -> PinNet:
    return PinNet(name=parse_name(pin_net_dict), pins=parse_pins(pin_net_dict), lines=parse_lines(pin_net_dict))


def parse_pin_nets(pin_nets_dict) -> List[PinNet]:
    return [parse_pin_net(pin_net_dict) for pin_net_dict in pin_nets_dict['pin_nets']]


def parse_top_left(top_left_dict) -> tuple:
    return tuple([top_left_dict['top'], top_left_dict['left']])


def parse_name(name_dict) -> str:
    return name_dict['name']


def parse_width(width_dict) -> int:
    return width_dict['width']


def parse_height(height_dict) -> int:
    return height_dict['height']


def parse_link(link_dict) -> str:
    return link_dict['link']


def parse_type(type_dict) -> str:
    return type_dict['type']


def parse_lines(lines_dict) -> List[List[Tuple[int, int]]]:
    return [
        [tuple(lines_dict['lines'][i][0]),
         tuple(lines_dict['lines'][i][0])]
        for i in range(len(lines_dict['lines']))
    ]
