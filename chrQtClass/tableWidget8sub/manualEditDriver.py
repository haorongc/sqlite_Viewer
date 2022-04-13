from PyQt5.QtCore import Qt
import pyperclip
from chrQtClass.qtFun import addShortcut
from chrSupport.basicFun import dprt

class ManualEditDriver():
    def __init__(self, tableWidget):
        self.tableWidget = tableWidget
        self.tableView = tableWidget.tableView
        self.selectionDriver = tableWidget.selectionDriver
        self.model = tableWidget.model
        self.widths = tableWidget.configDriver.widths
        self.flagsEditLock = tableWidget.configDriver.flagsEditLock

        self.nFields = tableWidget.nFields
        self.copiedTexts = list()
        self.allText = pyperclip.paste()

        # def connectShortcuts(self):
        addShortcut(self.tableView, 'Ctrl+c', self.copySelectedCells)
        addShortcut(self.tableView, 'Ctrl+x', self.cutSelectedCells)
        addShortcut(self.tableView, 'Ctrl+v', self.paste2SelectedCells)
        addShortcut(self.tableView, 'Delete', self.clearSelectedCells)

    def copySelectedCells(self):
        dprt('copying')
        indices = self.tableView.selectedIndexes()
        self.copiedTexts.clear()
        for index in indices:
            text = self.selectionDriver.data6modelIndex(index)  # how about hidden columns?
            text = str(text)
            self.copiedTexts.append(text)
        # send to system clipboard for interfacing with other apps
        self.allText = '\t'.join(self.copiedTexts)
        pyperclip.copy(self.allText)

    def paste2SelectedCells(self):
        selectedIndices = self.tableView.selectedIndexes()
        startIndex = selectedIndices[-1]
        systemClipBoardText = pyperclip.paste()
        if len(selectedIndices) == 1:  # somehow can only paste into one row any way
            if systemClipBoardText != self.allText:
                # copied from somewhere else, paste only into selected cell
                self.model.setData(startIndex, systemClipBoardText)
            else:
                # I copied from within GUI, set trailing cells by self.copiedTexts
                r = startIndex.row()
                c = startIndex.column()

                # get trailing unhidden cols
                cols2paste = list()
                while c < self.nFields:
                    if self.widths[c]:  # don't count hidden columns
                        cols2paste.append(c)
                    c += 1
                # paste into cells. wont exceed bondary
                for c, text in zip(cols2paste, self.copiedTexts):
                    if self.flagsEditLock[c] == False:
                        index = self.model.index(r, c)
                        self.model.setData(index, text)

    def clearSelectedCells(self):
        indices = self.tableView.selectedIndexes()
        for index in indices:
            col = index.column()
            if self.widths[col] and self.flagsEditLock[col]==False:
                self.model.setData(index, None, role=Qt.EditRole)

    def cutSelectedCells(self):
        self.copySelectedCells()
        self.clearSelectedCells()

    def probeFun(self):
        print('probe called')
