# ------------------------------- Класс соединения пинов ---------------------------------------
class PinConnection:
    def __init__(self, name: str, pin_1: str, pin_2: str):
        self.__name = name
        self.__pin_1 = pin_1
        self.__pin_2 = pin_2

    def get_name(self) -> str:
        return self.__name

    def set_name(self, name: str):
        self.__name = name

    def get_pin_1(self) -> str:
        return self.__pin_1

    def set_pin_1(self, pin_1: str):
        self.__pin_1 = pin_1

    def get_pin_2(self) -> str:
        return self.__pin_2

    def set_pin_2(self, pin_2: str):
        self.__pin_2 = pin_2


# ------------------------------- Класс, отвечающий за графическое представление -------------------------------
class BaseGraphicsModel:
    def __init__(self, top: int, left: int, width: int, height: int):
        self.__top = top
        self.__left = left
        self.__width = width
        self.__height = height

    def get_top(self) -> int:
        return self.__top

    def set_top(self, top: int):
        self.__top = top

    def get_left(self) -> int:
        return self.__left

    def set_left(self, left: int):
        self.__left = left

    def get_width(self) -> int:
        return self.__width

    def set_width(self, width: int):
        self.__width = width

    def get_height(self) -> int:
        return self.__height

    def set_height(self, height: int):
        self.__height = height


# ---------------------------------------- Класс примитива ----------------------------------------
class Primitive(BaseGraphicsModel):
    def __init__(self, name: str, pins: [str], top: int, left: int, width: int, height: int):
        super().__init__(top, left, width, height)
        self.__name = name
        self.__pins = pins

    def get_name(self) -> str:
        return self.__name

    def set_name(self, name: str):
        self.__name = name

    def get_pins(self) -> [str]:
        return self.__pins

    def set_pins(self, pins: [str]):
        self.__pins = pins


# ----------------- Класс блока (в том числе класс основной схемы - блок с именем "main") -----------------
class Block(BaseGraphicsModel):
    def __init__(self, name: str, pins: [str], pin_connection: [PinConnection],
                 top: int, left: int, width: int, height: int):
        super().__init__(top, left, width, height)
        self.__name = name
        self.__pins = pins
        self.__pin_connection = pin_connection
        self.__inner_blocks_list = []    # здесь будет храниться лист с внутренними блоками и примитивами
        self.__inner_connections_list = []  # здесь будет храниться лист со связями блока
        self.__init_inner_blocks_and_connections()

    # функция (сейчас заглушка) для инициализации внутренних блоков и связей
    def __init_inner_blocks_and_connections(self):
        pass

    def get_name(self) -> str:
        return self.__name

    def set_name(self, name: str):
        self.__name = name

    def get_pins(self) -> [str]:
        return self.__pins

    def set_pins(self, pins: [str]):
        self.__pins = pins

    def get_pin_connection(self) -> [PinConnection]:
        return self.__pin_connection

    def set_pin_connection(self, pin_connection: [PinConnection]):
        self.__pin_connection = pin_connection

    def get_inner_connections_list(self) -> list:
        return self.__inner_connections_list

    def set_inner_connections_list(self, inner_connections_list: list):
        self.__inner_connections_list = inner_connections_list

    def get_inner_blocks_list(self) -> list:
        return self.__inner_blocks_list

    def set_inner_block_list(self, inner_blocks_list: list):
        self.__inner_blocks_list = inner_blocks_list
