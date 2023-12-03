from PyQt5.QtWidgets import QMainWindow


class HierarchyWindow(QMainWindow):
    """
    Window for present hierarchy of primitives and blocks
    """
    def __init__(self):
        super(HierarchyWindow, self).__init__()
        self.setWindowTitle('Hierarchy Window')
        self.setMinimumWidth(500)
        self.setMinimumHeight(500)
        self.hierarchy_arr = []

    def get_hierarchy(self):
        """
        get hierarchy from backend to parse
        :return:
        """
        pass

    def visualize_hierarchy(self):
        """
        visualise hierarchy on HierarchyWindow
        :return:
        """
        pass
