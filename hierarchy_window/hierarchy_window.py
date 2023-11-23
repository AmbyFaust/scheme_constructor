from PyQt5.QtWidgets import QMenu, QMainWindow, QAction, QMenuBar, QWidget
from PyQt5.QtWidgets import QTreeView, QVBoxLayout
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor
from PyQt5 import QtCore
from functools import partial


class StandardItem(QStandardItem):
    def __init__(self, obj):
        super().__init__()

        self.name = obj.get_name()
        self.type = type(obj).__name__
        self.obj = obj

        colors = {"Block": QColor(255, 0, 0), "Primitive": QColor(0, 0, 255)}

        #self.setEditable(False)
        self.setForeground(colors[self.type])
        self.setText(self.name)

class HierarchyWindow(QMainWindow):
    """
    Window for present hierarchy of primitives and blocks
    """
    def __init__(self):
        super(HierarchyWindow, self).__init__()
        self.setWindowTitle('Hierarchy Window')
        self.setMinimumWidth(300)
        self.setMinimumHeight(500)
        self.primitives_arr = []
        self.blocks_arr = []

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Name', "Type"])

        self.tree = QTreeView()
        self.tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.openMenu)
        self.tree.setModel(self.model)

        self.tree.setHeaderHidden(True)
        self.tree.header().setDefaultSectionSize(180)
        self.tree.expandAll()

        self.setCentralWidget(self.tree)

    def openMenu(self, position):
        mdlIdx = self.tree.indexAt(position)
        right_click_menu = QMenu()
        act_add = right_click_menu.addAction(self.tr("visualize"))
        act_add.triggered.connect(partial(self.visualize, self.model.item(mdlIdx.row())))
        right_click_menu.exec_(self.sender().viewport().mapToGlobal(position))

    def visualize(self, stand_item: StandardItem):
        print(stand_item.obj)

    def get_hierarchy(self, primitives, blocks):
        """
        get hierarchy from backend to parse
        :return:
        """
        self.primitives_arr = primitives
        self.blocks_arr = blocks
        print(self.primitives_arr, self.blocks_arr)
        self.visualize_hierarchy()

    def visualize_hierarchy(self, root=None):
        """
        visualise hierarchy on HierarchyWindow
        :return:
        """

        self.model.setRowCount(0)
        if root is None:
            root = self.model.invisibleRootItem()

        for prim in self.primitives_arr:
            name, typ = self.__dfs(prim)
            root.appendRow([name, typ])

        for block in self.blocks_arr:
            name, typ = self.__dfs(block)
            root.appendRow([name, typ])

    def __dfs(self, base_obj):
        if type(base_obj).__name__ == "PrimitiveWidget":
            name = StandardItem(base_obj.primitive)
            typ = QStandardItem(type(base_obj.primitive).__name__)
            return name, typ

        elif type(base_obj).__name__ == "Primitive":
            name = StandardItem(base_obj)
            typ = QStandardItem(type(base_obj).__name__)
            return name, typ

        elif type(base_obj).__name__ == "BlockWidget":
            name = StandardItem(base_obj.block)
            typ = QStandardItem(type(base_obj.block).__name__)

            inner_blocks = base_obj.block.get_inner_blocks_list()
            if len(inner_blocks) == 0:
                return name, typ
            else:
                for elem in inner_blocks:
                    inner_name, inner_typ = self.__dfs(elem)
                    name.appendRow([inner_name, inner_typ])
                return name, typ

        elif type(base_obj).__name__ == "Block":
            name = StandardItem(base_obj)
            typ = QStandardItem(type(base_obj).__name__)

            inner_blocks = base_obj.get_inner_blocks_list()
            if len(inner_blocks) == 0:
                return name, typ
            else:
                for elem in inner_blocks:
                    inner_name, inner_typ = self.__dfs(elem)
                    name.appendRow([inner_name, inner_typ])
                return name, typ

    # def __dfs(self, base_obj):
    #     if type(base_obj).__name__ == "PrimitiveWidget":
    #         name = QStandardItem(base_obj.primitive.get_name())
    #         typ = QStandardItem(type(base_obj.primitive).__name__)
    #         return name, typ
    #
    #     elif type(base_obj).__name__ == "Primitive":
    #         name = QStandardItem(base_obj.get_name())
    #         typ = QStandardItem(type(base_obj).__name__)
    #         return name, typ
    #
    #     elif type(base_obj).__name__ == "BlockWidget":
    #         name = QStandardItem(base_obj.block.get_name())
    #         typ = QStandardItem(type(base_obj.block).__name__)
    #
    #         inner_blocks = base_obj.block.get_inner_blocks_list()
    #         if len(inner_blocks) == 0:
    #             return name, typ
    #         else:
    #             for elem in inner_blocks:
    #                 inner_name, inner_typ = self.__dfs(elem)
    #                 name.appendRow([inner_name, inner_typ])
    #             return name, typ
    #
    #     elif type(base_obj).__name__ == "Block":
    #         name = QStandardItem(base_obj.get_name())
    #         typ = QStandardItem(type(base_obj).__name__)
    #
    #         inner_blocks = base_obj.get_inner_blocks_list()
    #         if len(inner_blocks) == 0:
    #             return name, typ
    #         else:
    #             for elem in inner_blocks:
    #                 inner_name, inner_typ = self.__dfs(elem)
    #                 name.appendRow([inner_name, inner_typ])
    #             return name, typ




