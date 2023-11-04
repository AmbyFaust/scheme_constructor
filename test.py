import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 200, 200)
        self.has_border = True  # Флаг для отслеживания наличия обводки

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.has_border:
            pen = QPen(Qt.black)  # Создаем перо с желаемой обводкой
            pen.setWidth(2)  # Устанавливаем толщину обводки
            painter.setPen(pen)  # Устанавливаем обводку
        else:
            painter.setPen(Qt.NoPen)  # Убираем обводку

        painter.drawRect(10, 10, 180, 180)  # Рисуем прямоугольник

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_widget = MyWidget()
    my_widget.show()
    sys.exit(app.exec_())
