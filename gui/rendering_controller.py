from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class RenderingController(QObject):
    # ----------------------------
    # инициализация сигналов в формате
    # ... = pyqtSignal(...)
    # ----------------------------

    def __init__(self):
        super().__init__()

    # ----------------------------
    # Установка и описание слотов в формате

    # @pyqtSlot(имеющийся signal)
    # def ...(self, ...):
    #     ...

    # ----------------------------
