# from chrSupport.basicFun import dprt
from chrQtClass.qtFun import addShortcut
from functools import partial
from chrQtClass.textInputDialog import TextInputDialog
import pyperclip
from chrQtClass.actionDriver.multiTableBaseDriver import MultiTableBaseDriver
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTabWidget, QInputDialog

from chrSupport.textParseFun import word_num6text
# from chrSupport.lengthLimitedStack import LengthLimitedStack


class TabNavigator(MultiTableBaseDriver):  #
    # defaultMaxLen = 2
    # prevIndices = LengthLimitedStack(defaultMaxLen)
    prevIndex = None
    currentIndex = None

    def __init__(self, multiTableViewer):
        super().__init__(multiTableViewer)
        self.guiTableName_index = multiTableViewer.guiTableName_index
        self.tabs = multiTableViewer.tabs
        self.guiTables = multiTableViewer.guiTables

        self.inputDialog = QInputDialog()
        # self.textInputDialog.dataReadySignal.connect(self.probeFun)

        self.tabs.currentChanged.connect(self.recordCurrentIndex)
        self.currentIndex = self.multiTableViewer.currentTableIndex()

        addShortcut(multiTableViewer, 'Ctrl+g', self.gotoEntry)
        # addShortcut(multiTableViewer, 'Ctrl+Shift+g', self.gotoPrevTab)
        addShortcut(multiTableViewer, 'backspace', self.gotoPrevTab)

    def probeFun(self):
        print('probe fun called in navigator')

    def recordCurrentIndex(self):
        self.prevIndex = self.currentIndex
        self.currentIndex = self.multiTableViewer.currentTableIndex()

    def gotoPrevTab(self):
        if self.prevIndex != None:
            self.tabs.setCurrentIndex(self.prevIndex)

    def gotoEntry(self):

        text, ok = self.inputDialog.getText(self.multiTableViewer, 'navigator', 'go to')

        if ok:
            tableName, id = word_num6text(text)
        else:
            return

        try:
            tableIndex = self.guiTableName_index[tableName]
        except:
            pass
        else:
            self.tabs.setCurrentIndex(tableIndex)
            if id != None:
                destTableWidget = self.guiTables[tableIndex].widget
                destTableWidget.filterHeader.setBoxes6dict({'id': f'={id}'})


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    dbPath = r'C:\Users\thinkbanny\Dropbox\codes\220303-dbGUI\docs4debug.sqlite'
    backupLoc = r'C:\Users\thinkbanny\Dropbox\codes\220303-dbGUI\_backup'

    app = QApplication(sys.argv)
    viewer = MultiTableDbViewer(dbPath=dbPath, localLoc=backupLoc, tableNames=['aaa', 'dia'])

    viewer.show()
    #
    # widget = BookManager(dbPath, localLoc=r'C:\local_coding\~temp')
    # widget.showMaximized() # widget.show()  #
    #
    sys.exit(app.exec_())
