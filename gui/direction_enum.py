from enum import Enum


class Direction(Enum):
    horizontal = 0
    vertical = 1

    @classmethod
    def get_another(cls, direction):
        if direction == cls.horizontal:
            return cls.vertical
        else:
            return cls.horizontal