from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMenu, QMainWindow, QMenuBar

from gui.rendering_window import RenderingWindow
from gui.rendering_widget import RenderingWidget
from gui.object_panel import ObjectPanel
from hierarchy_window import hierarchy_window
from files_window.files_window import FilesWindow


class WindowRedactor(QMainWindow):
    """
    Window for working with Redactor
    """
    def __init__(self, dir_path):
        super(WindowRedactor, self).__init__()
        self.setWindowTitle('WindowNetlist')
        self.setMinimumWidth(1000)
        self.setMinimumHeight(500)
        self.menuBar = None

        self.dir_path = dir_path
        self.schema = None

        self.work_zone = None
        self.object_panel = None
        self.hierarchy_window = None
        self.files_window = FilesWindow(self.dir_path)

        self.__createMenuBar()
        self.__createMainWidgets()

    def __createMainWidgets(self):
        """
        creating Widgets for work zone and primitive panel
        creating Window for hierarchy
        :return:
        """

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        self.work_zone = RenderingWindow()
        self.object_panel = ObjectPanel()
        self.hierarchy_window = hierarchy_window.HierarchyWindow()

        lay = QtWidgets.QGridLayout(central_widget)

        for w, (r, c) in zip(
                (self.work_zone, self.object_panel, self.hierarchy_window),
                ((0, 0), (0, 1), (0, 2)),
        ):
            lay.addWidget(w, r, c)

        for c in range(3):
            lay.setColumnStretch(c, 1)

        self.object_panel.objAddRequested.connect(self.work_zone.rendering_widget.add_object_from_panel)
        self.object_panel.show()

        # lay = QtWidgets.QVBoxLayout(self.work_zone)
        # lay.addWidget(QtWidgets.QWidget())
        #
        # lay = QtWidgets.QVBoxLayout(self.panel_primitive)
        # lay.addWidget(QtWidgets.QListWidget())
        #
        # lay = QtWidgets.QVBoxLayout(self.hierarchy_window)
        # lay.addWidget(QtWidgets.QMainWindow())

    def __createMenuBar(self):
        """
        creating menu bar for working with files and hierarchy window
        :return:
        """
        self.menuBar = QMenuBar(self)
        self.setMenuBar(self.menuBar)

        fileMenu = QMenu("&File", self)
        self.menuBar.addMenu(fileMenu)

        fileMenu.addAction('open', self.clicked_open)
        fileMenu.addAction('close', self.clicked_close)

        clear = QMenu("&Clear", self)
        self.menuBar.addMenu(clear)
        clear.addAction('reload', self.clicked_clear)

        # hierarchy = QMenu("&Hierarchy", self)
        # self.menuBar.addMenu(hierarchy)
        # hierarchy.addAction('reload', self.clicked_reload_hierarchy)

        self.files_window.login_data[dict].connect(self.clicked_reload_hierarchy)

    def clicked_reload_hierarchy(self, objects: dict):
        """
        reload hierarchy after update
        :return:
        """
        # action = self.sender()
        # print("Pressed button", action.text())
        # primitives_widgets = self.work_zone.rendering_widget.primitives_widgets
        # block_widgets = self.work_zone.rendering_widget.block_widgets
        # self.hierarchy_window.get_hierarchy(primitives_widgets, block_widgets)

        self.schema = objects
        self.hierarchy_window.get_hierarchy(self.schema)


    @QtCore.pyqtSlot()
    def clicked_clear(self):
        """
        clear work zone
        :return:
        """
        action = self.sender()
        print("Pressed button", action.text())

        for wire_widg in list(self.work_zone.rendering_widget.all_wire_widgets):
            wire_widg.delete()
        for prim_widg in list(self.work_zone.rendering_widget.all_primitive_widgets):
            prim_widg.delete()
        for block_widg in list(self.work_zone.rendering_widget.all_block_widgets):
            block_widg.delete()
        for pin_widg in list(self.work_zone.rendering_widget.all_pin_widgets):
            pin_widg.delete()
        for cross_widg in list(self.work_zone.rendering_widget.all_crossroad_widgets):
            cross_widg.cascade_delete()

        self.work_zone.rendering_widget.pin_widgets = []

        self.work_zone.rendering_widget.rendered_wire = None
        self.work_zone.rendering_widget.update()


    @QtCore.pyqtSlot()
    def clicked_open(self):
        """
        open one of redactor project
        :return:
        """
        self.files_window.show()

    @QtCore.pyqtSlot()
    def clicked_close(self):
        """
        close current redactor project
        :return:
        """
        action = self.sender()
        print("Pressed button", action.text())
