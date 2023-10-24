from PyQt5.QtWidgets import QWidget

from gui.rendering_controller import RenderingController


class PrimitiveWidget(QWidget):
    def __init__(self, controller: RenderingController = None):
        super().__init__()
        self.controller = controller
        self.primitive = None
        self.__set_widgets()
        self.__set_layouts()
        self.__set_connections()

    def __set_widgets(self):
        pass

    def __set_layouts(self):
        pass

    def __set_connections(self):
        pass

    def set_primitive(self, primitive):
        self.primitive = primitive


