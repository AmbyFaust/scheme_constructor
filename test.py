import sys

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtWidgets import QApplication, QWidget

class ResizableWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 200, 200)  # Устанавливаем начальные размеры
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("border: 1px black;")
        self.start = self.pos()
        self.end = self.pos()
        self.mouse_pressed = True

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawLine(QPoint(0, 0), QPoint(self.width(), self.height()))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_pressed = True
            self.start = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_pressed = False

    def mouseMoveEvent(self, event):
        if self.mouse_pressed:
            if self.mouse_pressed:
                new_width = event.x() - self.start.x()
                new_height = event.y() - self.start.y()
                self.setFixedSize(new_width, new_height)


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 400, 400)
        self.resizable_widget = ResizableWidget()
        self.resizable_widget.setMouseTracking(True)
        self.setMouseTracking(True)
        self.resizable_widget.setParent(self)  # Делаем ResizableWidget дочерним виджетом
        self.resizable_widget.move(50, 50)

    def mouseMoveEvent(self, event):
        new_width = event.x() - self.resizable_widget.x()
        new_height = event.y() - self.resizable_widget.y()
        self.resizable_widget.setFixedSize(new_width, new_height)
        print(self.resizable_widget.size())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_widget = MainWidget()
    main_widget.show()
    sys.exit(app.exec_())
