import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 400, 400)

    def paintEvent(self, event):
        painter = QPainter(self)

        # Создаем перо с кастомными параметрами
        pen = QPen(Qt.black)
        pen.setWidth(1)  # Ширина линии
        pen.setCapStyle(Qt.RoundCap)  # Устанавливаем стиль концов линии (круглые точки)
        pen.setCustomDashOffset(1)  # Смещение точек

        painter.setPen(pen)
        painter.drawLine(50, 50, 350, 50)  # Рисуем линию с точками на концах


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_widget = MyWidget()
    my_widget.show()
    sys.exit(app.exec_())
