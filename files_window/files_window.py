from PyQt5.QtWidgets import QFileSystemModel, QTreeView, QVBoxLayout, QWidget, QMenu
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import QtCore
from pathlib import Path
from functools import partial
from coder_parser.parser import parse


class FilesWindow(QWidget):
    """
    Window for working with checker
    """
    login_data = pyqtSignal(object)

    def __init__(self, dir_path):
        super(FilesWindow, self).__init__()
        self.setWindowTitle('FilesWindow')
        self.setMinimumWidth(400)
        self.setMinimumHeight(400)

        self.dir_path = dir_path
        self.schema = {}

        self.model = QFileSystemModel()
        self.model.setRootPath(dir_path)

        self.tree = QTreeView()
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.openMenu)
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(dir_path))
        self.tree.setColumnWidth(0, 100)
        self.tree.setAlternatingRowColors(True)

        self.tree.expandAll()

        layout = QVBoxLayout()
        layout.addWidget(self.tree)
        self.setLayout(layout)

    def openMenu(self, position):
        mdlIdx = self.tree.indexAt(position)
        path = str(Path(self.model.filePath(mdlIdx)).name)

        right_click_menu = QMenu()
        act_add = right_click_menu.addAction(self.tr("upload schema"))
        act_add.triggered.connect(partial(self.run_parser, path))
        right_click_menu.exec_(self.sender().viewport().mapToGlobal(position))

    @QtCore.pyqtSlot()
    def run_parser(self, path: str):
        try:
            self.schema = parse(self.dir_path + path)
            self.login_data.emit(self.schema)
            print(f"Schema {self.schema}")
            self.close()
        except Exception as exc:
            print(f"Something go wrong in checker, LOG: {exc}")


