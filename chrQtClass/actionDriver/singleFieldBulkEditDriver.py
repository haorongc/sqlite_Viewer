# from chrSupport.basicFun import dprt
from chrQtClass.qtFun import addShortcut
from functools import partial
from chrQtClass.textInputDialog import TextInputDialog
import pyperclip
from chrQtClass.actionDriver.multiTableBaseDriver import MultiTableBaseDriver


class SingleFieldBulkEditDriver(MultiTableBaseDriver):  #
    backupNote = ''

    def __init__(self, multiTableViewer):
        super().__init__(multiTableViewer)

        self.textInputDialog = TextInputDialog()
        self.textInputDialog.dataReadySignal.connect(self.execFieldValueSet)

        for guiTable in multiTableViewer.guiTables:
            tableView = guiTable.widget.tableView
            addShortcut(tableView, 'Ctrl+Shift+v', self.bulkPaste)
            addShortcut(tableView, 'alt+t', self.bulkTypeWrite)
            addShortcut(tableView, 'Shift+Delete', self.bulkClearCell)

    def probeFun(self):
        print('probe fun called in bulk editor')


    def bulkPaste(self):
        self.findCallingTable()
        self.backupNote = f'before bulk paste in {self.callingTableName}'

        text = pyperclip.paste()
        self.execFieldValueSet(text)

    def bulkClearCell(self):
        self.findCallingTable()
        self.backupNote = f'before bulk clear in {self.callingTableName}'

        self.execFieldValueSet(None)

    def bulkTypeWrite(self):
        self.findCallingTable()
        self.backupNote = f'before bulk type in {self.callingTableName}'

        defaultText = self.callingTable.oneValue6selection()
        defaultText = str(defaultText)
        self.textInputDialog.setDefaultText(defaultText)
        self.textInputDialog.show()

    def execFieldValueSet(self, str2change2):
        # create undopoint for before saving type
        self.dbWorker.genUndoPoint(self.backupNote)

        with self.dbWorker.Save8mod8refresh(self.dbWorker):
            ids = self.callingTable.ids6selection()
            field = self.callingTable.oneField6selection()
            for id in ids:
                self.callingTable.update6dictPair({field: str2change2}, {'id': id})
            self.dbWorker.commit()


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
