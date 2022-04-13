from PyQt5.QtWidgets import (QWidget, QPushButton, QGridLayout)
from PyQt5.QtCore import pyqtSignal
from chrQtClass.tableWidget8sub.filterLineEdit import FilterLineEdit
from chrSupport import basicFun as mbf


class FilterHeaderWidget(QWidget):
    # buttonClicked = pyqtSignal(int)
    filterTermChanged = pyqtSignal()
    sortButtonStyles = {'normal': "Text-align:left",
                        'descend': "Text-align:left; font: bold; text-decoration: underline",
                        'ascend': "Text-align:left; font: bold"
                        }
    nRows = 2  # 2 rows by default

    def __init__(self, tableWidget):
        super().__init__()
        self.allFields = tableWidget.allFields
        self.nFields = tableWidget.nFields
        self.field_index = tableWidget.field_index

        self.setupWidgets()

    def setTitleCol(self, titleCol):
        self.titleCol = titleCol

    def setColumnHidden(self, c, wantHidden):
        if wantHidden:
            self.sortButtons[c].hide()
            for r in range(self.nRows):
                self.filterRows[r][c].hide()
        else:
            self.sortButtons[c].show()
            for r in range(self.nRows):
                self.filterRows[r][c].show()

    def show8selectTitleBox(self):
        self.show()
        lineEditor = self.filterRows[0][self.titleCol]
        lineEditor.setFocus()
        lineEditor.selectAll()

    def setupWidgets(self):
        filterGridBox = QGridLayout()
        filterGridBox.setSpacing(0)
        self.sortButtons = []
        self.filterRows = []

        for c in range(self.nFields):
            sortButton = QPushButton(self.allFields[c])
            sortButton.setMinimumSize(30, 20)
            sortButton.setStyleSheet(self.sortButtonStyles['normal'])
            self.sortButtons.append(sortButton)
            filterGridBox.addWidget(sortButton, 0, c)
            # _ = partial(self.buttonClicked.emit, c)
            # self.sortButtons[c].clicked.connect(_)

        for r in range(self.nRows):
            filterRow = []
            for c, field in enumerate(self.allFields):
                filterEdit = FilterLineEdit(field)
                filterGridBox.addWidget(filterEdit, r + 1, c)
                # filterEditor.setMinimumSize(30,20)v
                filterRow.append(filterEdit)
            self.filterRows.append(filterRow)

        self.filterEdits = []
        for filterRow in self.filterRows:
            self.filterEdits += filterRow

        filterGridBox.setColumnStretch(self.nFields, 1)
        self.setLayout(filterGridBox)

    # self.header.sectionResized.connect(self.sizingFilterBoxes)
    def applyWidths(self, widths):
        for col, width in enumerate(widths):
            if col == None:
                print(f'trying to set width of a noneexisting column')
                return

            self.sortButtons[col].setFixedWidth(width)
            for r in range(self.nRows):
                self.filterRows[r][col].setFixedWidth(width)

    # def setColumnWidth(self, col, width):
    #     if col == None:
    #         print(f'trying to set width of a noneexisting column')
    #         return
    #
    #     self.sortButtons[col].setFixedWidth(width)
    #     for r in range(self.nRows):
    #         self.filterRows[r][col].setFixedWidth(width)

    def setBoxes6dict(self, searchDict):
        self.clearAllBoxes()
        for field, key in searchDict.items():
            col = self.field_index[field]
            text = str(key)
            self.filterRows[0][col].setText(text)

    def setColumnLocked(self, col, wantLocked):
        if wantLocked:
            filterBoxstyle = "background: #ECECEC"  # #FAFAFA
        else:
            filterBoxstyle = "background: transparent"
        for row in range(self.nRows):
            self.filterRows[row][col].setStyleSheet(filterBoxstyle)

    def clearAllBoxes(self):
        for filterEdit in self.filterEdits:
            filterEdit.clear()

    # def toggleVisibility(self):
    #     if self.filterRow.isHidden():
    #         self.filterRow.show()
    #     else:
    #         self.filterRow.hide()
