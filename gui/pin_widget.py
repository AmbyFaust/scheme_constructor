from PyQt5.QtWidgets import QWidget

from gui.rendering_controller import RenderingController


class PinWidget(QWidget):
    def __init__(self, controller: RenderingController = None):
        super().__init__()
        self.controller = controller
        self.pin_connection = None
        self.graphics_model = None
        self.__set_widgets()
        self.__set_layouts()
        self.__set_connections()

    def __set_widgets(self):
        pass

    def __set_layouts(self):
        pass

    def __set_connections(self):
        pass

    def set_pin_connection(self, pin_connection):
        self.pin_connection = pin_connection

    def set_graphics_model(self, graphics_model):
        self.graphics_model = graphics_model
