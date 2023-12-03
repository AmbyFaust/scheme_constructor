from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QListWidget, QWidget, QAction, QMenu

from gui.object_item import ObjectItem, PrimitiveWidget, BlockWidget, createNewPrimitiveObjectItem

from gui.primitive_creator import PrimitiveCreator

class ObjectPanel(QListWidget):
    def __init__(self):
        super(ObjectPanel, self).__init__()
        self.setIconSize(QtCore.QSize(200, 200))
        self.setWordWrap(True)
        self.setSelectionMode(QListWidget.SingleSelection)
        self.setAutoScroll(False)
        self.setSpacing(5)

        # Добавление в группу примитивов пустого примитива
        self.__addNewLabel("Primitives")
        new_prim_element = createNewPrimitiveObjectItem()
        new_prim_element.setWhatsThis("uneditable")

        self.addItem(new_prim_element)

        # Кешируем объект для быстрого доступа к нему +
        # создаем метку группы блоков
        self.__block_label_item = self.__addNewLabel("Blocks")

        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.__showContextMenu)
        self.itemDoubleClicked.connect(self.handleDoubleClick)

    def __addNewLabel(self, label: str):
        item = ObjectItem(label)
        item.setFlags(QtCore.Qt.NoItemFlags)
        item.setTextAlignment(QtCore.Qt.AlignHCenter)
        item.setWhatsThis("label")
        self.addItem(item)
        return item

    def handleDoubleClick(self, item):
        if item.whatsThis() == "uneditable":
            self.window = PrimitiveCreator(self)
            self.window.work_zone.objSaveRequested.connect(self.registerObject)
            #self.window.show()
        else:
            self.objAddRequested.emit(item.getStoredObject())

    def removeItem(self):
        selected_items = self.selectedItems()
        for item in selected_items:
            if item.whatsThis() == "uneditable":
                continue
            self.takeItem(self.row(item))
            self.objDeleted.emit(item.getStoredObject())

    def editItem(self):
        selected_items = self.selectedItems()
        for item in selected_items:
            if item.whatsThis() == "uneditable":
                continue
            self.objEditRequested.emit(item.getStoredObject())

    def __showContextMenu(self, pos):
        menu = QMenu()

        edit_action = QAction("Edit", menu)
        edit_action.triggered.connect(self.editItem)
        menu.addAction(edit_action)

        remove_action = QAction("Remove", menu)
        remove_action.triggered.connect(self.removeItem)
        menu.addAction(remove_action)

        menu.exec_(self.mapToGlobal(pos))

    #### signals

    objAddRequested = pyqtSignal(object)

    objDeleted = pyqtSignal(object)

    objEditRequested = pyqtSignal(object)
    
    #### slots

    @QtCore.pyqtSlot(QWidget)
    def registerObject(self, obj):
        new_el = ObjectItem("", obj)
        for ind in range(self.count()):
            item = self.item(ind)
            if item.whatsThis() == "":
                checking = item.getStoredObject()
                if checking.name_label.text() == obj.name_label.text():
                    item.setStoredObject(obj)
                    return
        if isinstance(obj, BlockWidget):
            self.addItem(new_el)
        elif isinstance(obj, PrimitiveWidget):
            ind = self.indexFromItem(self.__block_label_item).row()
            self.insertItem(ind, new_el)

