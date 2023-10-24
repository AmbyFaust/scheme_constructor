from PyQt5.QtWidgets import QWidget

from gui.rendering_controller import RenderingController


class BlockWidget(QWidget):
    def __init__(self, controller: RenderingController = None):
        super().__init__()
        self.controller = controller
        self.block = None
        self.__set_widgets()
        self.__set_layouts()
        self.__set_connections()

    def __set_widgets(self):
        pass

    def __set_layouts(self):
        pass

    def __set_connections(self):
        pass

    def set_block(self, block):
        self.block = block


