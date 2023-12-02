from schema_classes import BaseGraphicsModel, Pin, PinNet, Primitive, Object, Block
from utils import json_to_dict, is_name_valid, is_type_valid, is_number_valid
from typing import List, Tuple


def parse(filename):
    data = json_to_dict(filename)

    main_found = False
    items = dict()

    for el in data:
        if parse_name(el) in items.keys():
            raise RuntimeError('Block (or Primitive) with name \"{}\" already exists.'.format(parse_name(el)))

        if parse_type(el) == 'block':
            block = parse_block(el)
            items[parse_name(el)] = block
            main_found = main_found or (parse_name(el) == 'main')

        elif parse_type(el) == 'primitive':
            primitive = parse_primitive(el)
            items[parse_name(el)] = primitive

    if not main_found:
        raise RuntimeError('Block with name \"main\" not found.')

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


def parse_pin_by_name(name) -> Pin:
    return Pin(name=name, top_left=(0, 0))


def parse_pins_by_names(pin_names_dict) -> List[Pin]:
    return [parse_pin_by_name(name) for name in pin_names_dict['pins']]


def parse_pin_net(pin_net_dict) -> PinNet:
    return PinNet(name=parse_name(pin_net_dict), pins=parse_pins_by_names(pin_net_dict), lines=parse_lines(pin_net_dict))


def parse_pin_nets(pin_nets_dict) -> List[PinNet]:
    return [parse_pin_net(pin_net_dict) for pin_net_dict in pin_nets_dict['pin_nets']]


def parse_top_left(top_left_dict) -> tuple:
    tl = top_left_dict['top_left']
    if len(tl) == 2 and is_number_valid(tl[0]) and is_number_valid(tl[1]):
        return tuple([tl[0], tl[1]])
    raise RuntimeError(f'Top or left can not be parsed.')


def parse_name(name_dict) -> str:
    if is_name_valid(name_dict['name']):
        return name_dict['name']
    raise RuntimeError(f'Name can not be parsed.')


def parse_width(width_dict) -> int:
    if is_number_valid(width_dict['width']):
        return width_dict['width']
    raise RuntimeError(f'Width can not be parsed.')


def parse_height(height_dict) -> int:
    if is_number_valid(height_dict['height']):
        return height_dict['height']
    raise RuntimeError(f'Height can not be parsed.')


def parse_link(link_dict) -> str:
    if is_name_valid(link_dict['link'], 0):
        return link_dict['link']
    raise RuntimeError(f'Link can not be parsed.')


def parse_type(type_dict) -> str:
    if is_type_valid(type_dict['type']):
        return type_dict['type']
    raise RuntimeError(f'Type can not be parsed.')


def parse_lines(lines_dict) -> List[List[Tuple[int, int]]]:
    res = []
    for line in lines_dict['lines']:
        res_line = []
        if len(line) != 2:
            raise RuntimeError(f'Line must be represented by 2 points, {len(line)} were given.')
        for point in line:
            if len(point) != 2:
                raise RuntimeError(f'Point must be represented by 2 numbers, {len(point)} were given.')
            if is_number_valid(point[0]) and is_number_valid(point[1]):
                res_line.append(tuple([point[0], point[1]]))
            else:
                raise RuntimeError(f'Top or left can not be parsed.')
        res.append(res_line)

    return res
