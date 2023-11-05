from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QCursor, QMouseEvent
from PyQt5.QtWidgets import QWidget, QAction, QMenu, QLabel, QVBoxLayout, QDialog

from core.schema_classes import Block
from gui.pin_widget import PinWidget
from gui.rendering_controller import RenderingController
from gui.set_name_dialog import SetNameDialog
from settings import rendering_widget_width, rendering_widget_height


class BlockWidget(QWidget):
    def __init__(self, parent=None, controller: RenderingController = None, block: Block = None):
        super(BlockWidget, self).__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.controller = controller
        self.block = block
        self.move(block.get_left(), block.get_top())
        self.setFixedWidth(block.get_width())
        self.setFixedHeight(block.get_height())

        self.pin_widgets = []

        self.dragging = False
        self.offset = QPoint(
            self.width() // 2,
            self.height() // 2
        )

        self.__create_widgets()
        self.__create_layouts()
        self.__create_actions()
        self.unlock()

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def destructor(self):
        for pin_widget in self.pin_widgets:
            pin_widget.destructor()
        self.pin_widgets.clear()

    def __create_widgets(self):
        self.name_label = QLabel(self.block.get_name())
        self.name_label.setStyleSheet('border: 0px ')
        self.name_label.setAlignment(Qt.AlignCenter)

    def __create_layouts(self):
        common_v_layout = QVBoxLayout()
        common_v_layout.addWidget(self.name_label)
        self.setLayout(common_v_layout)

    def __create_actions(self):
        self.add_pin_action = QAction("Добавить Пин", self)
        self.add_pin_action.triggered.connect(self.add_pin)
        self.set_name_action = QAction("Изменить имя", self)
        self.set_name_action.triggered.connect(self.set_name)
        self.del_action = QAction("Удалить", self)
        self.del_action.triggered.connect(self.delete)

    def show_context_menu(self, position):
        context_menu = QMenu(self)
        context_menu.setStyleSheet("background-color: gray;")
        context_menu.addAction(self.add_pin_action)
        context_menu.addAction(self.set_name_action)
        context_menu.addAction(self.del_action)
        context_menu.exec(self.mapToGlobal(position))

    def lock(self):
        self.setStyleSheet("border: 2px solid black; background-color: #42aaff;")

    def unlock(self):
        for pin in self.pin_widgets:
            if pin.wire:
                return
        self.setStyleSheet("border: 0px solid black; background-color: #42aaff;")

    def delete(self):
        self.parent().del_block(self)

    def add_pin(self):
        pin_widget = PinWidget(self.parent(), self)
        self.pin_widgets.append(pin_widget)
        pin_widget.show()

    def set_name(self):
        set_name_dialog = SetNameDialog(self.name_label.text())
        if set_name_dialog.exec_() == QDialog.Accepted:
            self.block.set_name(set_name_dialog.name_edit.text())
            self.name_label.setText(self.block.get_name())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and not self.parent().rendered_wire:
            for pin_widget in self.pin_widgets:
                if pin_widget.wire:
                    return
            QCursor.setPos(self.mapToGlobal(self.offset))
            self.dragging = True

    def mouseMoveEvent(self, event):
        if self.dragging:
            x_possible = (
                self.width() // 2,
                rendering_widget_width - self.width() // 2
            )
            y_possible = (
                self.height() // 2,
                rendering_widget_height - self.height() // 2
            )
            pos = self.pos() + event.pos()
            cursor_x = pos.x()
            cursor_y = pos.y()
            delta_x = 0
            delta_y = 0
            last_pos_cursor_screen = QCursor.pos()
            if cursor_x < x_possible[0]:
                delta_x = cursor_x - x_possible[0]
            elif cursor_x > x_possible[1]:
                delta_x = cursor_x - x_possible[1]
            if cursor_y < y_possible[0]:
                delta_y = cursor_y - y_possible[0]
            elif cursor_y > y_possible[1]:
                delta_y = cursor_y - y_possible[1]
            QCursor.setPos(
                last_pos_cursor_screen.x() - delta_x,
                last_pos_cursor_screen.y() - delta_y
            )
            new_pos = pos - QPoint(delta_x, delta_y) - self.offset
            for pin_widget in self.pin_widgets:
                new_pos_pin = pin_widget.pos() + new_pos - self.pos()
                pin_widget.move(new_pos_pin)
            self.move(new_pos)
        else:
            new_event = QMouseEvent(event.type(),
                                    event.pos() + self.pos(),
                                    event.screenPos(),
                                    event.button(),
                                    event.buttons(),
                                    event.modifiers())
            self.parent().mouseMoveEvent(new_event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False




