from PyQt5.QtWidgets import QMenu, QMainWindow, QMenuBar, QWidget
from PyQt5.QtWidgets import QTreeView, QVBoxLayout
from PyQt5.QtGui import QStandardItemModel, QStandardItem



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

        self.tree = QTreeView(self)
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Name', 'Type'])
        self.tree.header().setDefaultSectionSize(180)
        self.tree.setModel(self.model)
        self.tree.expandAll()

        self.setCentralWidget(self.tree)



    def get_hierarchy(self, primitives, blocks):
        """
        get hierarchy from backend to parse
        :return:
        """
        self.primitives_arr = primitives
        self.blocks_arr = blocks
        print(self.primitives_arr, self.blocks_arr)
        for i in self.primitives_arr:
            print(i.primitive.get_name())
        for i in self.blocks_arr:
            print(i.block.get_name())
            print(type(i).__name__)
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
            name = QStandardItem(base_obj.primitive.get_name())
            typ = QStandardItem(type(base_obj.primitive).__name__)
            return name, typ
        else:
            name = QStandardItem(base_obj.block.get_name())
            typ = QStandardItem(type(base_obj.block).__name__)

            inner_blocks = base_obj.block.get_inner_blocks_list()
            if len(inner_blocks) == 0:
                return name, typ
            else:
                for elem in inner_blocks:
                    inner_name, inner_typ = self.dfs(elem)
                    name.appendRow([QStandardItem(inner_name), QStandardItem(inner_typ)])
                return name, typ




