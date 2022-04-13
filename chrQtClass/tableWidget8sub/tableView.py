from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QTableView, QItemDelegate)
from PyQt5.QtGui import QPalette
from chrQtClass.tableWidget8sub.readOnlyDelegate import ReadOnlyDelegate
from chrQtClass.tableWidget8sub.cellDelegate import CellDelegate

class TableView(QTableView):  #
    headerClicked = pyqtSignal(int)
    widthChanged = pyqtSignal(int)
    # request2hideColumn = pyqtSignal()
    request2showAll = pyqtSignal()
    delegates = None

    def __init__(self, tableWidget):
        super().__init__()
        # self.widget = tableWidget
        self.setModel(tableWidget.model)
        self.delegates = [None] * tableWidget.nFields
        self.setSelectionMode(QTableView.ExtendedSelection)
        self.setSelectionBehavior(QTableView.SelectItems)  # SelectRows
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)

        self.verticalHeader().hide()

        palette = QPalette()
        palette.setColor(QPalette.Inactive, QPalette.Highlight,
                         palette.color(QPalette.Active, QPalette.Highlight))
        self.setPalette(palette)

    def setColumnLocked(self, col, wantLocked):
        if wantLocked:
            delegate = ReadOnlyDelegate()
        else:
            delegate = QItemDelegate()
        self.delegates[col] = delegate  # drop old delegate?
        self.setItemDelegateForColumn(col, delegate)

    def applyWidths(self, widths):
        for i, width in enumerate(widths):
            self.setColumnWidth(i, width)


    def probeFun(self):
        print('probe called')


