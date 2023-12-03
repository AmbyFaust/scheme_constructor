from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QRect, QSize, QPoint
from PyQt5.QtWidgets import QListWidgetItem, QWidget
from PyQt5.QtGui import QIcon

from gui.pin_widget import PinWidget
from gui.primitive_widget import PrimitiveWidget
from gui.block_widget import BlockWidget
from schema_classes.schema_classes import Primitive, Block
from settings import pin_width, pin_height, primitive_width, primitive_height
                                            
from copy import deepcopy


class ObjectItem(QListWidgetItem):
    def __init__(self, text:str, obj:QWidget = None):
        super(ObjectItem, self).__init__(text)

        self.__data = None
        if obj:
            self.setStoredObject(obj)

    def setStoredObject(self, obj: QWidget):
        self.__data = _ObjectDublicator.clone(obj)
        padding = min(pin_width, pin_height, 0)
        self.setIcon(QIcon(self.__data.grab(QRect(QPoint(-padding//2,-padding//2), 
                                            QSize(self.__data.width() + padding, self.__data.height() + padding)))))

    def getStoredObject(self) -> QWidget:
        return _ObjectDublicator.clone(self.__data)

# создаёт начальный примитив, добавляемый в список при инициализации
def createNewPrimitiveObjectItem():
        new_primitive = Primitive("new", [], (0, 0), primitive_width, primitive_height)
        new_primitive_widget = PrimitiveWidget(None, primitive=new_primitive)
        return ObjectItem("", new_primitive_widget)


#    singledispatchmethod отказывается работать, поэтому статик
#    вспомогательный класс клонирования виджетов
#
#    !! У созданного клона родитель объекта устанавливается None !!
#    !! Родителем всех пинов является клон                       !!
#    !! Координаты пинов задаются в локальной системе координат  !!
#    !! Это важно учитывать при получении объектов               !!
class _ObjectDublicator:
    @staticmethod
    def clone(obj):
        cloned = None
        if isinstance(obj, PrimitiveWidget):
            cloned = PrimitiveWidget(None, deepcopy(obj.primitive))

        elif isinstance(obj, BlockWidget):
            cloned = BlockWidget(None, deepcopy(obj.block))

        if not cloned:
            return cloned

        for pin in obj.pin_widgets:
            pin_widget = PinWidget(cloned, pin.pin, cloned)
            pin_widget.move(pin.pos() - obj.pos())
            cloned.pin_widgets.append(pin_widget)
            pin_widget.show()
        return cloned
