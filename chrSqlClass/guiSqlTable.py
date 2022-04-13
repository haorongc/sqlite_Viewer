import cgitb

cgitb.enable(format='text')

from chrSqlClass.sqlTable import SqlTable
from chrQtClass.tableWidget8sub.sqlTableWidget import SqlTableWidget
from chrSupport.dictWorker import DictWorker

dictWorker = DictWorker()


class GuiSqlTable(SqlTable):
    initSortField = None
    titleField = None
    widget = None

    def __init__(self, guiDbWorker, tableName, titleField, initSortField):
        super().__init__(guiDbWorker, tableName)

        self.widget = SqlTableWidget(self, titleField, initSortField)

    def setInitSortField(self, field):
        self.initSortField = field

    def setTitleField(self, field):
        self.titleField = field

    def oneValue6selection(self):
        return self.widget.selectionDriver.oneValue6selection()

    def oneId6selection(self):
        return self.widget.selectionDriver.oneId6selection()

    def oneField6selection(self):
        return self.widget.selectionDriver.oneField6selection()

    def ids6selection(self):
        return self.widget.selectionDriver.ids6selection()

    def oneDict6selection(self, fields2request=None):
        return self.widget.selectionDriver.oneDict6selection(fields2request)

    def hasEdits(self):
        if len(self.widget.editArchiver.editedIdSet) > 0:
            return True
        else:
            return False

    def discardEdits(self):
        self.widget.editArchiver.clearEditLog()

    def saveEdits(self):
        self.widget.cellEditorDriver.save2cell()
        self.widget.editArchiver.archiveEdits()


if __name__ == '__main__':
    from chrSqlClass.guiDbWorker import GuiDbWorker
    # from chrSqlClass.guiSqlTable import GuiSqlTable
    # from chrSqlClass.guiDbWorker import GuiDbWorker
    import os, sys

    dbLoc = r'C:\local_coding\CHR_packages\_db'
    dbPath = os.path.join(dbLoc, 'docs.sqlite')
    localLoc = r'C:\local_coding\~temp'

    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    worker = GuiDbWorker(dbPath, localLoc)
    worker.activate()

    table = worker.getGuiTable('lec')
    # table.setInitSortField('id')
    table.setInitSortField('tMod')
    table.setTitleField('id')

    table2 = worker.getGuiTable('lec')
    table2.genTableWidget()

    # resultDicts = table2.dicts6searchDict(None, {'place': 'bats', 'who': 'Emi Lutz'})
    # for resultDict in resultDicts:
    #     print(resultDict)

    # table.widget.showMaximized()

    sys.exit(app.exec_())
