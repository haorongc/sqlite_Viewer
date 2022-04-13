# from chrFileOpClass.tableDriver import TableDriver
# from chrFileOpClass.sqlTable import SqlTable
from chrSupport.basicFun import dprt
# import os
# from expManager.expLocsKeeper import ExpLocsKeeper as locsKeeper
# from chrSupport.textParseFun import idDicts6idStr
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout
from chrQtClass.qtFun import addShortcut
from PyQt5.QtCore import pyqtSignal


class FormInputDialog(QDialog):
    dataReadySignal = pyqtSignal(list)

    def __init__(self, destTableName, insertionForm):
        super().__init__()
        self.setWindowTitle(f'insert to {destTableName}')
        self.form = insertionForm
        self.setMinimumSize(800, 600)

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # assemble widgets
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.form)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

        # self.setupShortcuts()



    def reject(self):
        dprt('cancel importing')
        super().reject()

    def accept(self):
        dicts2insert = self.form.dicts6allRows()
        dprt(dicts2insert)
        self.dataReadySignal.emit(dicts2insert)
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
