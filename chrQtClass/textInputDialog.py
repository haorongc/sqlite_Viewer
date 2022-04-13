# from chrFileOpClass.tableDriver import TableDriver
# from chrFileOpClass.sqlTable import SqlTable
from chrSupport.basicFun import dprt
# import os
# from expManager.expLocsKeeper import ExpLocsKeeper as locsKeeper
# from chrSupport.textParseFun import idDicts6idStr
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLineEdit
from chrQtClass.qtFun import addShortcut
from PyQt5.QtCore import pyqtSignal


class TextInputDialog(QDialog):
    dataReadySignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f'set text to change to')
        self.lineEdit = QLineEdit()
        self.setMinimumSize(600, 400)

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # assemble widgets
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.lineEdit)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

        # self.setupShortcuts()


    def setDefaultText(self, text):
        self.lineEdit.setText(text)

    def reject(self):
        dprt('cancel bulk typing')
        super().reject()

    def accept(self):
        str2change2 = self.lineEdit.text()
        dprt(str2change2)
        self.dataReadySignal.emit(str2change2)
        super().accept()

    # def setupShortcuts(self):
    #     addShortcut(self, 'Ctrl+return', self.accept)


# if __name__ == '__main__':
#     import sys
#     import cgitb
#
#     cgitb.enable(format='text')
#
#     app = QApplication(sys.argv)
#     infoDicts = [{'id': 'z1'}, {'tAdd': 11}, {'id': 'x1'}]
#     fields = ['mnem', 'tAdd', 'id', 'feature', 'context', 'method', 'journey', 'source']
#     form = InsertionDialog(fields, infoDicts)
#     form.showMaximized()  # show()  #
#     try:
#         sys.exit(app.exec_())
#     except:
#         print("Exiting")
