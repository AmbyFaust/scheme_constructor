from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5 import QtCore
from gui.rendering_widget import RenderingWidget


class RenderingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.__set_widgets()
        self.__set_layouts()
        self.__set_connections()

    def __set_widgets(self):
        self.rendering_widget = RenderingWidget()
        self.rendering_widget.setParent(self)
        self.save_as_block_button = QPushButton('Save as Block')
        self.clear_button = QPushButton('Clear')

    def __set_layouts(self):
        common_v_layout = QVBoxLayout()
        tools_h_layout = QHBoxLayout()
        tools_h_layout.addWidget(self.save_as_block_button)
        tools_h_layout.addWidget(self.clear_button)
        common_v_layout.addLayout(tools_h_layout)
        common_v_layout.addWidget(self.rendering_widget)
        self.setLayout(common_v_layout)

    def __set_connections(self):
        self.clear_button.clicked.connect(self.clear)
        self.rendering_widget.clear_area.connect(self.clear)

    @QtCore.pyqtSlot()
    def clear(self):
        """
        clear work zone
        :return:
        """

        for wire_widg in list(self.rendering_widget.all_wire_widgets):
            wire_widg.delete()
        for prim_widg in list(self.rendering_widget.all_primitive_widgets):
            prim_widg.delete()
        for block_widg in list(self.rendering_widget.all_block_widgets):
            block_widg.delete()
        for pin_widg in list(self.rendering_widget.all_pin_widgets):
            pin_widg.delete()
        for cross_widg in list(self.rendering_widget.all_crossroad_widgets):
            cross_widg.cascade_delete()

        self.rendering_widget.pin_widgets = []

        self.rendering_widget.rendered_wire = None
        self.rendering_widget.update()
