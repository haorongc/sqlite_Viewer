from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTabWidget

from chrQtClass.tableWindow import TableWindow
from chrQtClass.qtFun import addShortcut
from chrSupport.dictWorker import DictWorker
from chrSqlClass.guiDbWorker import GuiDbWorker
dictWorker = DictWorker()


class MultiTableViewer(QMainWindow):  #
    def __init__(self, dbPath, guiTableNames, localLoc=None,
                 tableName_titleField=dict(),
                 tableName_initSortField=dict()):
        super().__init__()
        self.setWindowTitle(dbPath)
        self.guiTableNames = guiTableNames
        nTables = len(self.guiTableNames)

        # dbWorker is core for all db operation
        self.dbWorker = GuiDbWorker(dbPath, backupLoc=localLoc)
        self.dbWorker.guiTableNames = guiTableNames

        # multiTableDbViewer has several abstract tables that can be manipulated
        self.tableWindows = []
        self.tableName_guiWindow = dict()
        for tableName in self.guiTableNames:
            titleField = tableName_titleField.get(tableName, 'id')
            initSortField = tableName_initSortField.get(tableName, 'id')
            guiTable = self.dbWorker.getGuiTable(tableName, titleField, initSortField)
            tableWindow = TableWindow(guiTable.widget)
            self.tableWindows.append(tableWindow)
            self.tableName_guiWindow[tableName] = tableWindow

        self.guiTables = self.dbWorker.guiTables
        self.guiTableName_index = dictWorker.indexMap6list(self.guiTableNames)

        self.assembleWidgets()

        # setup drivers
        from chrQtClass.actionDriver.singleFieldBulkEditDriver import SingleFieldBulkEditDriver
        self.bulkEditDriver = SingleFieldBulkEditDriver(self)

        from chrQtClass.actionDriver.tabNavigator import TabNavigator
        self.tableNavigator = TabNavigator(self)

        self.setupMoreDrivers()

        self.setupMenus()
        self.setupShortcuts()

    def assembleWidgets(self):
        self.tabs = QTabWidget()
        for window, tableName in zip(self.tableWindows, self.guiTableNames):
            self.tabs.addTab(window, tableName)

        self.setCentralWidget(self.tabs)

    def currentTableIndex(self):
        return self.tabs.currentIndex()

    def setupMoreDrivers(self):
        pass

    def setupMenus(self):
        self.menu = self.menuBar()
        fileMenu = self.menu.addMenu('&file')
        editMenu = self.menu.addMenu('&edit')
        editMenu.addAction("undo\t &z", self.undo)

    def setupShortcuts(self):
        addShortcut(self, 'Ctrl+z', self.undo)
        addShortcut(self, 'Ctrl+s', self.save)
        addShortcut(self, 'F5', self.dbWorker.saveEdits8refresh)
        addShortcut(self, 'Shift+F5', self.dbWorker.discardEdits8refresh)

    def save(self):
        for window in self.tableWindows:
            window.submitDockEdits()
        self.dbWorker.saveEdits()

    def undo(self):
        # if there is unsaved edits, user likely want to redo the editing, no need to use redo points to overwrite
        # otherwise, the action to revert is from external command, needs redo point overwrite
        if self.dbWorker.hasEdits():
            print('undoing manual edits')
            self.dbWorker.discardEdits8refresh()
        else:
            print('undoing script generated change')
            self.dbWorker.undo()
            self.dbWorker.discardEdits8refresh()

    def probeFun(self):
        # print('probe fun by multi tab viewer')
        for table in self.tableName_guiTable.values():
            dict = table.ids6selection()
            # dict = table.oneDict6selection()
            print(dict)

    def closeEvent(self, event):
        print('requested to exit')

        if self.dbWorker.hasEdits():
            reply = QMessageBox.question(self, 'closing prompt', 'save changes?',
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Yes)

            if reply not in {QMessageBox.Yes, QMessageBox.No}:
                # chosen not to exit
                print('  chosen not to exit')
                event.ignore()
                return
            # chosen to exit
            if reply == QMessageBox.Yes:
                # chosent to save
                print('\t saving changes')
                self.dbWorker.saveEdits()

            else:
                # exit without saving
                print('\t discard changes')
        else:
            # no changes, exit without prompt
            print('no changes to content, save settings and exit')

        # properly close
        for tableWindow in self.tableWindows:
            tableWindow.close()

        self.dbWorker.deactivate()
        # send2trash(self.dbWorker.mirrorDbPath)


if __name__ == '__main__':
    from chrSqlClass.guiDbWorker import GuiDbWorker
    import os, sys

    dbLoc = r'C:\local_coding\CHR_packages\_db'
    dbPath = os.path.join(dbLoc, 'labnotes.sqlite')
    localLoc = r'C:\local_coding\~temp'

    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    viewer = MultiTableViewer(dbPath, ['s', 'p'], localLoc)

    viewer.showMaximized()

    sys.exit(app.exec_())
