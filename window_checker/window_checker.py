from PyQt5.QtWidgets import QFileSystemModel, QTreeView, QVBoxLayout, QWidget, QMenu, QMessageBox
from PyQt5.QtCore import Qt
from pathlib import Path
from functools import partial
import subprocess


class WindowChecker(QWidget):
    """
    Window for working with checker
    """
    def __init__(self, dir_path):
        super(WindowChecker, self).__init__()
        self.setWindowTitle('WindowChecker')
        self.setMinimumWidth(500)
        self.setMinimumHeight(500)

        self.dir_path = dir_path

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
        act_add = right_click_menu.addAction(self.tr("Run checker"))
        act_add.triggered.connect(partial(self.run_checker, path))
        right_click_menu.exec_(self.sender().viewport().mapToGlobal(position))

    def run_checker(self, path: str):
        try:
            args = "./stubs/Checker.exe " + self.dir_path + path
            output = subprocess.run(args, capture_output=True)
            print(f"out: {output.stdout}, \nerror: {output.stderr}")

            msg = QMessageBox()
            msg.setWindowTitle("Result")
            if output.stderr == b'':
                msg.setText(f"file name: {path},\nChecker result: OK")
            else:
                msg.setText(f"file name: {path}\n,Checker result: WRONG,\nError: {output.stderr}")
            msg.exec()

            if output.returncode != 0:
                raise Exception(output.stderr)
        except Exception as exc:
            print(f"Something go wrong in checker, LOG: {exc}")
