import math
from time import sleep

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QCursor
from PyQt5.QtWidgets import QWidget, QPushButton

from core.schema_classes import Primitive, BaseGraphicsModel, Block
from gui.block_widget import BlockWidget
from gui.pin_widget import PinWidget
from gui.primitive_widget import PrimitiveWidget
from settings import primitive_width, primitive_height, pin_width, pin_height, block_width, block_height, \
    rendering_widget_width, rendering_widget_height


class RenderingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("border: 2px solid black;")  # Устанавливаем стиль с обводкой
        self.setFixedWidth(rendering_widget_width)
        self.setFixedHeight(rendering_widget_height)

        self.primitives_widgets = []
        self.block_widgets = []

        self.__create_widgets()

    def __create_widgets(self):
        pass

    def add_primitive(self):
        primitive = Primitive('primitive', [], 50, 100, 100, 50)
        primitive_widget = PrimitiveWidget(self, controller=None, primitive=primitive)
        primitive_widget.setStyleSheet("background-color: yellow;")
        primitive_widget.show()

        self.primitives_widgets.append(primitive_widget)
        print('add primitive')

    def del_primitive(self, primitive_widget: PrimitiveWidget):
        self.primitives_widgets.remove(primitive_widget)
        primitive_widget.destructor()
        primitive_widget.deleteLater()




    def add_block(self):
        block = Block('block', [], [], 100, 100, block_width, block_height)
        block_widget = BlockWidget(self, controller=None, block=block)
        block_widget.show()

        self.block_widgets.append(block_widget)
        print('add block')




