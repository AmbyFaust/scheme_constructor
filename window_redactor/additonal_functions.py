def is_point_on_rectangle_boundary(rectangle_x, rectangle_y, rectangle_width, rectangle_height, point_x, point_y):
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
