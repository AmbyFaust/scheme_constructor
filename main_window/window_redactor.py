from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMenu, QMainWindow, QMenuBar

from gui.rendering_widget import RenderingWidget
from hierarchy_window import HierarchyWindow


class WindowRedactor(QMainWindow):
    """
    Window for working with Redactor
    """
    def __init__(self):
        super(WindowRedactor, self).__init__()
        self.setWindowTitle('WindowNetlist')
        self.setMinimumWidth(1000)
        self.setMinimumHeight(500)
        self.menuBar = None

        self.work_zone = None
        self.primitive_panel = None
        self.hierarchy_window = None

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

        self.work_zone = RenderingWidget()
        self.panel_primitive = QtWidgets.QWidget()
        self.hierarchy_window = HierarchyWindow()

        lay = QtWidgets.QGridLayout(central_widget)

        for w, (r, c) in zip(
                (self.work_zone, self.primitive_panel),
                ((0, 0), (0, 1)),
        ):
            lay.addWidget(w, r, c)

        for c in range(2):
            lay.setColumnStretch(c, 1)

        lay = QtWidgets.QVBoxLayout(self.work_zone)
        lay.addWidget(QtWidgets.QWidget())

        lay = QtWidgets.QVBoxLayout(self.panel_primitive)
        lay.addWidget(QtWidgets.QListWidget())

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

        hierarchy = QMenu("&Hierarchy", self)
        self.menuBar.addMenu(hierarchy)

        hierarchy.addAction('open', self.clicked_open_hierarchy)
        hierarchy.addAction('reload', self.clicked_reload_hierarchy)

    @QtCore.pyqtSlot()
    def clicked_open_hierarchy(self):
        """
        open hierarchy window
        :return:
        """
        action = self.sender()
        print("Pressed button", action.text())
        self.hierarchy_window.show()

    @QtCore.pyqtSlot()
    def clicked_reload_hierarchy(self):
        """
        reload hierarchy after update
        :return:
        """
        action = self.sender()
        print("Pressed button", action.text())

    @QtCore.pyqtSlot()
    def clicked_open(self):
        """
        open one of redactor project
        :return:
        """
        action = self.sender()
        print("Pressed button", action.text())

    @QtCore.pyqtSlot()
    def clicked_close(self):
        """
        close current redactor project
        :return:
        """
        action = self.sender()
        print("Pressed button", action.text())
