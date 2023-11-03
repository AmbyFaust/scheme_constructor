import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt

class DrawingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 400, 400)
        self.drawing = False
        self.start_x, self.start_y = 0, 0
        self.end_x, self.end_y = 0, 0

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawLine(self.start_x, self.start_y, self.end_x, self.end_y)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.start_x, self.start_y = event.x(), event.y()
            self.end_x, self.end_y = event.x(), event.y()

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) and self.drawing:
            self.end_x, self.end_y = event.x(), event.y()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False
            self.end_x, self.end_y = event.x(), event.y()
            self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    drawing_app = DrawingWidget()
    drawing_app.show()
    sys.exit(app.exec_())
