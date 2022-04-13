# from chrSupport.basicFun import dprt
from PyQt5.QtWidgets import (QWidget, QVBoxLayout)
from chrSupport.dictWorker import DictWorker
from chrQtClass.qtFun import addShortcut

dictWorker = DictWorker()


class SqlTableWidget(QWidget):  #

    def __init__(self, sqlTable, titleField, initSortField):
        super().__init__()

        self.tableName = sqlTable.tableName
        self.sqlTable = sqlTable
        self.dbWorker = sqlTable.dbWorker

        self.allFields = sqlTable.allFields
        self.nFields = len(self.allFields)
        self.field_index = dictWorker.indexMap6list(self.allFields)

        self.idCol = self.field_index['id']

        # core widget
        from chrQtClass.tableWidget8sub.sqlTableModel import SqlTableModel
        self.model = SqlTableModel()
        self.model.setTable(self.tableName)
        self.model.loadData()

        from chrQtClass.tableWidget8sub.tableView import TableView
        self.tableView = TableView(self)

        from chrQtClass.tableWidget8sub.filterHeaderWidget import FilterHeaderWidget
        self.filterHeader = FilterHeaderWidget(self)

        self.setTitleField(titleField)
        self.setInitSortField(initSortField)
        self.setupDrivers()

        self.assembleWidgets()

    def setTitleField(self, titleField):
        self.titleField = titleField
        self.titleCol = self.field_index.get(self.titleField, None)
        self.filterHeader.setTitleCol(self.titleCol)

    def setInitSortField(self, initSortField):
        self.initSortCol = self.field_index.get(initSortField, None)

    def setupDrivers(self):
        from chrQtClass.tableWidget8sub.filterDriver import FilterDriver
        self.filterDriver = FilterDriver(self)

        from chrQtClass.tableWidget8sub.selectionDriver import SelectionDriver
        self.selectionDriver = SelectionDriver(self)

        from chrQtClass.tableWidget8sub.configDriver import ConfigDriver
        self.configDriver = ConfigDriver(self)  # load config, apply width and editLock

        from chrQtClass.tableWidget8sub.sortDriver import SortDriver
        self.sortDriver = SortDriver(self)

        from chrQtClass.tableWidget8sub.manualEditDriver import ManualEditDriver
        self.manualEditDriver = ManualEditDriver(self)

        from chrQtClass.tableWidget8sub.editArchiver import EditArchiver
        self.editArchiver = EditArchiver(self)

        from chrQtClass.tableWidget8sub.cellEditorDriver import CellEditorDriver
        self.cellEditorDriver = CellEditorDriver(self)

    def oneField6selection(self):
        return self.selectionDriver.oneField6selection()

    def assembleWidgets(self):
        mainVBOX = QVBoxLayout()
        mainVBOX.setSpacing(0)
        self.setLayout(mainVBOX)
        self.setMinimumSize(450, 300)

        mainVBOX.addWidget(self.filterHeader)
        mainVBOX.addWidget(self.tableView)

    def probeFun(self):
        print('table widget probe fun')
        self.editArchiver.archiveEdits()

    def closeEvent(self, event):
        self.configDriver.saveConfig2file()
        # print('save guiTable config to file')


if __name__ == '__main__':
    from chrSqlClass.guiDbWorker import GuiDbWorker
    from chrSqlClass.guiSqlTable import GuiSqlTable
    import os, sys

    dbLoc = r'C:\local_coding\CHR_packages\_db'
    dbPath = os.path.join(dbLoc, 'docs.sqlite')
    localLoc = r'C:\local_coding\~temp'

    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    worker = GuiDbWorker(dbPath, localLoc)

    table = GuiSqlTable(worker, 'lec')
    table.genTableWidget()
    table.widget.showMaximized()
    table.widget.cellEditor.show()

    sys.exit(app.exec_())
