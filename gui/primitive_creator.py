import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMenu, QMainWindow, QWidget, QPushButton, QMenuBar, QMessageBox
from gui.rendering_widget import RenderingWidget
from PyQt5.QtCore import pyqtSignal

class PrimitiveCreator(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(400)
        self.setMinimumHeight(400)
        self.work_zone = PrimitiveRenderingWidget()
        self.work_zone.add_primitive()
        self.work_zone.show()

    



class PrimitiveRenderingWidget(RenderingWidget):
    def __init__(self):
        super().__init__()
        self.add_pin_action.setVisible(False)
        self.save_button = QPushButton(self, text="Save Primitive")
        self.save_button.setStyleSheet('QPushButton {background-color: #FFFFFF;}')
        self.save_button.move(10, 350)
        self.save_button.setFixedWidth(150)
        self.save_button.show()
        self.save_button.clicked.connect(self.save_primitive)

    def add_primitive(self):
        self.prim_wid = super().add_primitive()
        self.prim_wid.del_action.setVisible(False)
        self.save_button.raise_()

    def add_pin(self, connect_widget):
        pin = super().add_pin(connect_widget)
        pin.add_wire_action.setVisible(False)
        self.save_button.raise_()

    def save_primitive(self):
        if self.prim_wid.name_label.text() == 'primitive':
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Название примитива должно быть отлично от Primitive")
            msg.exec()
        else:
            self.objSaveRequested.emit(self.prim_wid)
            self.close()

    objSaveRequested = pyqtSignal(QWidget)