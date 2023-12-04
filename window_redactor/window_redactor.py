import re

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMenu, QMainWindow, QMenuBar, QDialog, QMessageBox

from gui.object_panel import ObjectPanel
from gui.rendering_window import RenderingWindow
from gui.rendering_widget import RenderingWidget
from hierarchy_window import hierarchy_window
from files_window.files_window import FilesWindow
from schema_classes.schema_classes import Block, Primitive
from coder_parser.coder import scheme_to_json
from gui.set_name_dialog import SetNameDialog


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

        self.schema_uploader = None

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
        self.work_zone.rendering_widget.objSaveRequested.connect(self.object_panel.registerObject)
        self.object_panel.show()

        # lay = QtWidgets.QVBoxLayout(self.work_zone)
        # lay.addWidget(QtWidgets.QWidget())
        #
        # lay = QtWidgets.QVBoxLayout(self.panel_primitive)
        # lay.addWidget(QtWidgets.QListWidget())
        #
        # lay = QtWidgets.QVBoxLayout(self.hierarchy_window)
        # lay.addWidget(QtWidgets.QMainWindow())

        self.hierarchy_window.visualize_item.connect(self.upload_schema_object)

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
        fileMenu.addAction('save to json', self.clicked_save_json)

        clear = QMenu("&Clear", self)
        self.menuBar.addMenu(clear)
        clear.addAction('reload', self.clicked_clear)

        # hierarchy = QMenu("&Hierarchy", self)
        # self.menuBar.addMenu(hierarchy)
        # hierarchy.addAction('reload', self.clicked_reload_hierarchy)

        self.files_window.login_data[dict].connect(self.clicked_reload)

    def clicked_reload(self, objects: dict):
        """
        reload after update
        :return:
        """
        # action = self.sender()
        # print("Pressed button", action.text())
        # primitives_widgets = self.work_zone.rendering_widget.primitives_widgets
        # block_widgets = self.work_zone.rendering_widget.block_widgets
        # self.hierarchy_window.get_hierarchy(primitives_widgets, block_widgets)

        self.schema = objects
        print(f"window red: {self.schema}")
        self.upload_schema_object('main')
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
    def clicked_save_json(self):
        """
        close current redactor project
        :return:
        """
        action = self.sender()
        set_name_dialog = SetNameDialog(cur_name="", title_name="Сохранение схемы", place_holder="имя файла должно заканчиваться на .json")
        if set_name_dialog.exec_() == QDialog.Accepted:
            print(set_name_dialog.name_edit.text()[-5:])
            msg = QMessageBox()
            if re.match("[A-Za-z0-9]+\.json$", set_name_dialog.name_edit.text()):
                exc = None
                try:
                    scheme_to_json(schema=self.schema, filename=self.dir_path+set_name_dialog.name_edit.text())
                except Exception as exc_:
                    exc = exc_
                    print(f"Something go wrong in coder, LOG: {exc}")
                if not (exc is None):
                    msg.setWindowTitle("Error in coder")
                    msg.setText(f"error: {exc}")
                else:
                    msg.setWindowTitle("Saved")
                    msg.setText(f"schema saved: {set_name_dialog.name_edit.text()}")
            else:
                msg.setWindowTitle("Error")
                msg.setText("Incorrect file name")
            msg.exec()

        print("Pressed button", action.text())

    @QtCore.pyqtSlot(str)
    def upload_schema_object(self, key_name):
        if key_name in self.schema:
            if isinstance(self.schema[key_name], Block):
                self.work_zone.rendering_widget.parse_block(self.schema[key_name])
            if isinstance(self.schema[key_name], Primitive):
                self.work_zone.rendering_widget.add_primitive(self.schema[key_name])
