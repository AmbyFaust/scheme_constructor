from collections import defaultdict
from typing import Tuple

from gui.direction_enum import Direction
from schema_classes.schema_classes import PinNet


def is_point_on_rectangle_boundary(rectangle_x: int, rectangle_y: int, rectangle_width: int,
                                   rectangle_height: int, point_x: int, point_y: int):
    rectangle_right = rectangle_x + rectangle_width
    rectangle_bottom = rectangle_y + rectangle_height

    on_boundary = (
        rectangle_x <= point_x <= rectangle_right and
        rectangle_y <= point_y <= rectangle_bottom or
        (
            point_x == rectangle_x or
            point_x == rectangle_right or
            point_y == rectangle_y or
            point_y == rectangle_bottom
        )
    )

    return on_boundary


def get_direction(first_wire_point: Tuple[int, int], second_wire_point: Tuple[int, int]):
    if first_wire_point[0] - second_wire_point[0] == 0:
        return Direction.vertical
    else:
        return Direction.horizontal


def get_crossroads(pin_net: PinNet):
    point_counts = defaultdict(int)

    for line in pin_net.get_lines():
        for point in line:
            point_counts[point] += 1

    crossroads = [point for point, count in point_counts.items() if count >= 2]

    return crossroads
