import json
from schema_classes import BaseGraphicsModel, Pin, PinNet, Primitive, Object, Block

def converting_to_json(dict, filename):
    """
    Coding dictionary to json-file
    :param dict: dictionary with entities
    return json
    """
    print(dict)
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
        pin_dictionary = {
            'name': pin.get_name(),
            'top_left': pin.get_top_left()
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
        link = obj.get_link()
        if (isinstance(obj, Block)):
            type = 'Block'
        else:
            type = 'Primitive'
        obj_dictionary = {
            'type': type,
            'name': obj.get_name(),
            'top_left': obj.get_top_left(),
            'width': obj.get_width(),
            'height': obj.get_height()
        }
        if (type == 'Block'):
            obj_dictionary['pins'] = code_pins(obj.get_pins())
        if (link != ''):
            obj_dictionary['link'] = link
        list_of_objects.append(obj_dictionary)
    return list_of_objects


def scheme_to_json(schema, filename):
    """
    Coding scheme to json-file according to special format
    :param scheme: dictionary with objects
    :param filename: name of json file to save
    :return:
    """
    list_of_blocks = ""  # лист в который будут складываться блоки в формате json
    for obj in schema:
        if (isinstance(obj, Block)):
            type = 'Block'
        elif (isinstance(obj, Primitive)):
            type = 'Primitive'
        link = obj.get_link()
        obj_description = {
            'type': type,
            'name': obj.get_name(),
            'top_left': obj.get_top_left(),
            'width': obj.get_width(),
            'height': obj.get_height()}
        if ((type == 'Block') & (link == '')):
                obj_description['objects'] = code_objects(obj.get_objects())
                obj_description['pins'] = code_pins(obj.get_pins())
                obj_description['pin_nets'] = code_pin_nets(obj.get_pin_nets())
        elif(((type == 'Block') & (link != '')) | ((type == 'Primitive') & (link != ''))):
            obj_description['link'] = link
        converting_to_json(obj_description, filename)
    return 0


