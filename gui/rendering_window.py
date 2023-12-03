from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout

from gui.rendering_widget import RenderingWidget


class RenderingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.__set_widgets()
        self.__set_layouts()
        self.__set_connections()

    def __set_widgets(self):
        self.rendering_widget = RenderingWidget()
        self.add_primitive_button = QPushButton('Save as Block')
        self.add_block_button = QPushButton('Clear')

    def __set_layouts(self):
        common_v_layout = QVBoxLayout()
        tools_h_layout = QHBoxLayout()
        common_v_layout.addLayout(tools_h_layout)
        common_v_layout.addWidget(self.rendering_widget)
        tools_h_layout.addWidget(self.add_primitive_button)
        tools_h_layout.addWidget(self.add_block_button)
        self.setLayout(common_v_layout)

    def __set_connections(self):
        self.add_primitive_button.clicked.connect(self.rendering_widget.add_primitive)
        self.add_block_button.clicked.connect(self.rendering_widget.add_block)


