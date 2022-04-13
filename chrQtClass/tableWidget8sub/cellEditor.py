from chrQtClass.textEdit import TextEdit
from PyQt5.QtCore import pyqtSignal


class CellEditor(TextEdit):
    activation = pyqtSignal()
    deactivation = pyqtSignal()

    def show(self):
        super().show()
        self.activation.emit()

    def hide(self):
        super().hide()
        self.deactivation.emit()




