import json
from schema_classes.schema_classes import BaseGraphicsModel, Pin, PinNet, Primitive, Object, Block

def converting_to_json(dict, filename):
    """
    Coding dictionary to json-file
    :param dict: dictionary with entities
    return json
    """
    with open(filename, 'w') as outfile:
        json.dump(dict, outfile)

def code_pins(pins):
    """
    Coding pins to list of json objects
    :param pins: entities of class Pin
    :return: list of json objects
    """
    list_of_pins = []
    for pin in pins:
        top_left = pin.get_top_left()
        pin_dictionary = {
            'name': pin.get_name(),
            'top': top_left[0],
            'left': top_left[1]
        }
        list_of_pins.append(pin_dictionary)
    return list_of_pins


def code_pin_nets(pin_nets):
    """
    Coding main scheme to json-object according to special format
    :param pin_net: entity of Pin_connections
    :return: list of json objects

    """
    list_of_pin_nets = []
    for pn in pin_nets:
        pin_nets_dictionary = {
            'name': pn.get_name(),
            'pins': code_pins(pn.get_pins()),
            'lines': pn.get_lines()
        }
        list_of_pin_nets.append(pin_nets_dictionary)
    return list_of_pin_nets


def code_objects(objects):
    """
    Coding objects to list of json objects
    :param list of objects: entities of class Primitive and Block
    :return: list of json objects
    """
    list_of_objects = []
    for obj in objects:
        if (isinstance(obj, Block)):
            type = 'block'
        else:
            type = 'primitive'
        top_left = obj.get_top_left()
        obj_dictionary = {
            'type': type,
            'name': obj.get_name(),
            'link': obj.get_link(),
            'top': top_left[0],
            'left': top_left[1],
            'width': obj.get_width(),
            'height': obj.get_height(),
        }
        list_of_objects.append(obj_dictionary)
    return list_of_objects


def scheme_to_json(schema, filename):
    """
    Coding scheme to json-file according to special format
    :param scheme: dictionary with {name: object}
    :param filename: name of json file to save
    :return:
    """
    list_of_blocks = []
    for obj in schema.keys():
        if (isinstance(schema[obj], Block)):
            type = 'block'
        elif (isinstance(schema[obj], Primitive)):
            type = 'primitive'
        top_left = schema[obj].get_top_left()
        obj_description = {
            'type': type,
            'name': schema[obj].get_name(),
            'top': top_left[0],
            'left': top_left[1],
            'width': schema[obj].get_width(),
            'height': schema[obj].get_height(),
            'pins': code_pins(schema[obj].get_pins())}
        if (type == 'block'):
            obj_description['objects'] = code_objects(schema[obj].get_objects())
            obj_description['pin_nets'] = code_pin_nets(schema[obj].get_pin_nets())
        list_of_blocks.append(obj_description)
    converting_to_json(list_of_blocks, filename)
    return 0

