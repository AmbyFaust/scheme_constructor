from typing import List, Tuple


class BaseGraphicsModel:
    """
    Базовый класс для графических моделей. Этот класс предоставляет базовые атрибуты и методы для работы с графическими объектами.
    """
    def __init__(self, top_left: Tuple[int, int], width: int = 0, height: int = 0):
        """
        Инициализирует объект BaseGraphicsModel.

        Args:
            top_left (Tuple[int, int]): Координаты верхнего левого угла объекта.
            width (int, optional): Ширина объекта. Defaults to 0.
            height (int, optional): Высота объекта. Defaults to 0.
        """
        self._top_left = top_left
        self._width = width
        self._height = height

    def get_top_left(self) -> Tuple[int, int]:
        """
        Возвращает координаты верхнего левого угла объекта.

        Returns:
            Tuple[int, int]: Координаты верхнего левого угла.
        """
        return self._top_left

    def set_top_left(self, top_left: Tuple[int, int]):
        """
        Устанавливает новые координаты верхнего левого угла объекта.

        Args:
            top_left (Tuple[int, int]): Новые координаты верхнего левого угла.
        """
        self._top_left = top_left

    def get_width(self) -> int:
        """
        Возвращает ширину объекта.

        Returns:
            int: Ширина объекта.
        """
        return self._width

    def set_width(self, width: int):
        """
        Устанавливает новую ширину объекта.

        Args:
            width (int): Новая ширина объекта.
        """
        self._width = width

    def get_height(self) -> int:
        """
        Возвращает высоту объекта.

        Returns:
            int: Высота объекта.
        """
        return self._height

    def set_height(self, height: int):
        """
        Устанавливает новую высоту объекта.

        Args:
            height (int): Новая высота объекта.
        """
        self._height = height


class Pin(BaseGraphicsModel):
    """
    Класс, представляющий пин. Этот класс наследует атрибуты и методы от BaseGraphicsModel.
    """
    def __init__(self, name: str, top_left: Tuple[int, int]):
        """
        Инициализирует объект Pin.

        Args:
            name (str): Имя пина.
            top_left (Tuple[int, int]): Координаты верхнего левого угла пина.
        """
        super().__init__(top_left)
        self._name = name

    def get_name(self) -> str:
        """
        Возвращает имя пина.

        Returns:
            str: Имя пина.
        """
        return self._name

    def set_name(self, name: str):
        """
        Устанавливает новое имя пина.

        Args:
            name (str): Новое имя пина.
        """
        self._name = name


class PinNet:
    """
    Класс, представляющий соединение пинов.
    """
    def __init__(self, name: str, pins: List[Pin], lines: List[List[Tuple[int, int]]]):
        """
        Инициализирует объект PinNet.

        Args:
            name (str): Имя соединения пинов.
            pins (List[Pin]): Список пинов, входящих в соединение.
            lines (List[List[Tuple[int, int]]]): Список линий, представляющих соединение.
        """
        self._name = name
        self._pins = pins
        self._lines = lines

    def get_name(self) -> str:
        """
        Возвращает имя соединения пинов.

        Returns:
            str: Имя соединения пинов.
        """
        return self._name

    def set_name(self, name: str):
        """
        Устанавливает новое имя соединения пинов.

        Args:
            name (str): Новое имя соединения пинов.
        """
        self._name = name

    def get_pins(self) -> List[Pin]:
        """
        Возвращает список пинов, входящих в соединение.

        Returns:
            List[Pin]: Список пинов.
        """
        return self._pins

    def set_pins(self, pins: List[Pin]):
        """
        Устанавливает новый список пинов, входящих в соединение.

        Args:
            pins (List[Pin]): Новый список пинов.
        """
        self._pins = pins

    def get_lines(self) -> List[List[Tuple[int, int]]]:
        """
        Возвращает список линий, представляющих соединение пинов.

        Returns:
            List[List[Tuple[int, int]]]: Список линий.
        """
        return self._lines

    def set_lines(self, lines: List[List[Tuple[int, int]]]):
        """
        Устанавливает новый список линий, представляющих соединение пинов.

        Args:
            lines (List[List[Tuple[int, int]]]): Новый список линий.
        """
        self._lines = lines


class Primitive(BaseGraphicsModel):
    """
    Класс, представляющий примитив. Этот класс также наследует атрибуты и методы от BaseGraphicsModel.
    """
    def __init__(self, name: str, pins: List[Pin], top_left: Tuple[int, int], width: int, height: int, link: str = ''):
        """
        Инициализирует объект Primitive.

        Args:
            name (str): Имя примитива.
            pins (List[Pin]): Список пинов, входящих в примитив.
            top_left (Tuple[int, int]): Координаты верхнего левого угла примитива.
            width (int): Ширина примитива.
            height (int): Высота примитива.
            link (str, optional): Ссылка на примитив. Defaults to ''.
        """
        super().__init__(top_left, width, height)
        self._name = name
        self._pins = pins
        self._link = link

    def get_name(self) -> str:
        """
        Возвращает имя примитива.

        Returns:
            str: Имя примитива.
        """
        return self._name

    def set_name(self, name: str):
        """
        Устанавливает новое имя примитива.

        Args:
            name (str): Новое имя примитива.
        """
        self._name = name

    def get_pins(self) -> List[Pin]:
        """
        Возвращает список пинов, входящих в примитив.

        Returns:
            List[Pin]: Список пинов.
        """
        return self._pins

    def set_pins(self, pins: List[Pin]):
        """
        Устанавливает новый список пинов, входящих в примитив.

        Args:
            pins (List[Pin]): Новый список пинов.
        """
        self._pins = pins

    def get_link(self) -> str:
        """
        Возвращает ссылку на примитив.

        Returns:
            str: Ссылка на примитив.
        """
        return self._link

    def set_link(self, link: str):
        """
        Устанавливает новую ссылку на примитив.

        Args:
            link (str): Новая ссылка на примитив.
        """
        self._link = link


class Object(BaseGraphicsModel):
    """
    Класс, представляющий объект схемы. Этот класс также наследует атрибуты и методы от BaseGraphicsModel.
    """
    def __init__(self, name: str, object_type: str, link: str, top_left: Tuple[int, int], width: int, height: int):
        """
        Инициализирует объект Object.

        Args:
            name (str): Имя объекта схемы.
            object_type (str): Тип объекта (например, "primitive" или "block").
            link (str): Ссылка на объект.
            top_left (Tuple[int, int]): Координаты верхнего левого угла объекта.
            width (int): Ширина объекта.
            height (int): Высота объекта.
        """
        super().__init__(top_left, width, height)
        self._name = name
        self._object_type = object_type
        self._link = link

    def get_name(self) -> str:
        """
        Возвращает имя объекта схемы.

        Returns:
            str: Имя объекта схемы.
        """
        return self._name

    def set_name(self, name: str):
        """
        Устанавливает новое имя объекта схемы.

        Args:
            name (str): Новое имя объекта схемы.
        """
        self._name = name

    def get_object_type(self) -> str:
        """
        Возвращает тип объекта схемы.

        Returns:
            str: Тип объекта (например, "primitive" или "block").
        """
        return self._object_type

    def set_object_type(self, object_type: str):
        """
        Устанавливает новый тип объекта схемы.

        Args:
            object_type (str): Новый тип объекта (например, "primitive" или "block").
        """
        self._object_type = object_type

    def get_link(self) -> str:
        """
        Возвращает ссылку на объект.

        Returns:
            str: Ссылка на объект.
        """
        return self._link

    def set_link(self, link: str):
        """
        Устанавливает новую ссылку на объект.

        Args:
            link (str): Новая ссылка на объект.
        """
        self._link = link


class Block(BaseGraphicsModel):
    """
    Класс, представляющий блок-схемы. Этот класс также наследует атрибуты и методы от BaseGraphicsModel.
    """
    def __init__(self, name: str, pins: List[Pin], objects: List[Object], pin_nets: List[PinNet],
                 top_left: Tuple[int, int], width: int, height: int, link: str = ''):
        """
        Инициализирует блок-схемы.

        Args:
            name (str): Имя блок-схемы.
            pins (List[Pin]): Список пинов, принадлежащих блок-схеме.
            objects (List[Object]): Список объектов, входящих в состав блок-схемы.
            pin_nets (List[PinNet]): Список соединений пинов.
            top_left (Tuple[int, int]): Координаты верхнего левого угла блок-схемы.
            width (int): Ширина блок-схемы.
            height (int): Высота блок-схемы.
            link (str): Ссылка на блок-схему (по умолчанию пустая строка).
        """
        super().__init__(top_left, width, height)
        self._name = name
        self._pins = pins
        self._objects = objects
        self._pin_nets = pin_nets
        self._link = link

    def get_name(self) -> str:
        """
        Возвращает имя блок-схемы.

        Returns:
            str: Имя блок-схемы.
        """
        return self._name

    def set_name(self, name: str):
        """
        Устанавливает новое имя блок-схемы.

        Args:
            name (str): Новое имя блок-схемы.
        """
        self._name = name

    def get_pins(self) -> List[Pin]:
        """
        Возвращает список пинов, принадлежащих блок-схеме.

        Returns:
            List[Pin]: Список пинов.
        """
        return self._pins

    def set_pins(self, pins: List[Pin]):
        """
        Устанавливает новый список пинов, принадлежащих блок-схеме.

        Args:
            pins (List[Pin]): Новый список пинов.
        """
        self._pins = pins

    def get_objects(self) -> List[Object]:
        """
        Возвращает список объектов, входящих в состав блок-схемы.

        Returns:
            List[Object]: Список объектов.
        """
        return self._objects

    def set_objects(self, objects: List[Object]):
        """
        Устанавливает новый список объектов, входящих в состав блок-схемы.

        Args:
            objects (List[Object]): Новый список объектов.
        """
        self._objects = objects

    def get_pin_nets(self) -> List[PinNet]:
        """
        Возвращает список соединений пинов.

        Returns:
            List[PinNet]: Список соединений пинов.
        """
        return self._pin_nets

    def set_pin_nets(self, pin_nets: List[PinNet]):
        """
        Устанавливает новый список соединений пинов.

        Args:
            pin_nets (List[PinNet]): Новый список соединений пинов.
        """
        self._pin_nets = pin_nets
