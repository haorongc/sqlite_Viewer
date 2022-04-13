from chrSqlClass.reversibleDbWorker import ReversibleDbWorker
from chrSqlClass.sqlite3Worker import Sqlite3worker
from chrSqlClass.guiSqlTable import GuiSqlTable
from chrSupport.basicFun import dateTimeStamp
from chrSupport.basicFun import dprt

import shutil, sys
from PyQt5.QtSql import QSqlDatabase
from chrQtClass.qtFun import addShortcut


class GuiDbWorker(ReversibleDbWorker):
    guiTableNames = None  # to be set by application
    guiTables = list()

    def __init__(self, dbPath, backupLoc):
        super().__init__(dbPath, backupLoc)

        # additionally create a mirror file for GUI
        self.mirrorDbPath = self.fileMover.genDerivitivePath(dbPath, newLoc=backupLoc, prefix=dateTimeStamp())
        # create and overwrite working DB for gui
        shutil.copy(dbPath, self.mirrorDbPath)
        self.mirrorDbWorker = Sqlite3worker(self.mirrorDbPath)  # no need to backup or drive GUI
        self.connectMirrorDb()

    def connectMirrorDb(self):
        self.database = QSqlDatabase.addDatabase("QSQLITE")  # SQLite version 3
        self.database.setDatabaseName(self.mirrorDbPath)

        if not self.database.open():
            print(f"Unable to open data {self.mirrorDbPath}.")
            sys.exit(1)

    def getGuiTable(self, tableName, titleField, initSortField):
        table = self.tableName_table.get(tableName, None)
        if type(table) == GuiSqlTable:
            dprt('use the guiTable generated before')
            return table
        else:
            table = GuiSqlTable(self, tableName, titleField, initSortField)
            # table.genTableWidget()
            self.tableName_table[tableName] = table
            # wont be generated more than once, use list
            self.guiTables.append(table)
            # dprt(len(self.guiTables), 'len(self.guiTables)')
            return table

    def hasEdits(self):
        for guiTable in self.guiTables:
            if guiTable.hasEdits() or guiTable.widget.cellEditorDriver.hasEdit():
                # dprt(guiTable.widget.editArchiver.editedIdSet, f'edited in table {guiTable.tableName}')
                return True
        # finished loop, have not found edits
        return False

    def saveEdits(self):
        if self.hasEdits():
            self.genUndoPoint(description='before saving edits')

            for guiTable in self.guiTables:
                guiTable.saveEdits()

    def reloadDb(self):
        # self.database.close()
        shutil.copy(self.dbPath, self.mirrorDbPath)
        # if not self.database.open():
        #     print(f"Unable to open data {self.mirrorDbPath}.")
        #     sys.exit(1)

    def refreshGuiTables(self):
        for guiTable in self.guiTables:
            guiTable.widget.model.loadData()

    def discardEdits(self):
        self.reloadDb()
        for guiTable in self.guiTables:
            guiTable.discardEdits()


    def discardEdits8refresh(self):
        self.discardEdits()
        self.refreshGuiTables()

    def undo(self, description=None):
        if self.hasEdits():
            # latest changes are from typewrite, discard those will revert all changes
            self.discardEdits8refresh()
        else:
            # latest changes from script, undo by revert to prev undo point
            self.loadPrevUndoPoint()
            self.refreshGuiTables()

    def saveEdits8refresh(self):
        self.saveEdits()
        self.refreshGuiTables()

    class Save8mod8refresh():
        def __init__(self, obj):
            self.obj = obj

        def __enter__(self):
            dbWorker = self.obj
            dbWorker.saveEdits()

        def __exit__(self, exc_type, exc_value, exc_traceback):
            self.obj.discardEdits8refresh()

if __name__ == '__main__':
    dbPath = r'C:\Users\thinkbanny\Dropbox\codes\220303-dbGUI\docs4debug.sqlite'
    backupLoc = r'C:\Users\thinkbanny\Dropbox\codes\220303-dbGUI\_backup'

    worker = GuiDbWorker(dbPath, backupLoc)

    i = 0

    with worker.ActivateConnCur(worker, commit=True):
        while 1:
            action = input('type action code, '
                           'u for undo, r for redo, '
                           'e for create new state, q for exit')
            if action == 'q':
                break
            elif action == 'u':
                worker.undo('undo')
            # elif action == 'r':
            #     worker.redo('redo')
            elif action == 'e':
                worker.genUndoPoint(f'before inserted{i}')
                worker.insert6dict('dia', {'cSel': i})
                worker.commit()
                i += 1
