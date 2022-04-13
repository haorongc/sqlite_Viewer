from PyQt5.QtWidgets import (QMainWindow)
from PyQt5.QtCore import Qt

from chrQtClass.qtFun import addShortcut
from PyQt5.QtWidgets import QDockWidget


class TableWindow(QMainWindow):
    def __init__(self, tableWidget):
        super().__init__()
        self.tableWidget = tableWidget
        self.tableName = tableWidget.tableName
        self.setWindowTitle(self.tableName)

        self.dockedEditor = QDockWidget()
        self.dockedEditor.setWidget(tableWidget.cellEditor)
        tableWidget.cellEditor.activation.connect(self.dockedEditor.show)
        tableWidget.cellEditor.deactivation.connect(self.dockedEditor.hide)
        self.dockedEditorDriver = tableWidget.cellEditorDriver

        self.assembleWidgets()
        self.setupShortCuts()

    def assembleWidgets(self):
        self.setCentralWidget(self.tableWidget)

        self.addDockWidget(Qt.BottomDockWidgetArea, self.dockedEditor)
        self.dockedEditor.hide()

    def chooseDockArea(self, choiceStr):
        if choiceStr == 'right':
            self.addDockWidget(Qt.RightDockWidgetArea, self.dockedEditor)
        else:
            # bottom by default
            self.addDockWidget(Qt.BottomDockWidgetArea, self.dockedEditor)


    def showDock(self):
        self.dockedEditorDriver.activate8show()

    def hideUnhideDock(self):
        if self.dockedEditor.isHidden():
            self.dockedEditorDriver.activate8show()
        else:
            self.dockedEditorDriver.deactivate8hide()

    def deactivate8hideDockEditor(self):
        print('deactivate and hide')
        self.dockedEditor.hide()
        self.dockedEditorDriver.deactivate8hide()

    def activate8showDockEditor(self):
        print('activate and show')
        self.dockedEditor.show()
        self.dockedEditorDriver.activate8show()

    def setupShortCuts(self):
        addShortcut(self, 'Ctrl+k', self.hideUnhideDock)
        addShortcut(self, 'Ctrl+Shift+k', self.hideUnhideMainTable)


    def hideUnhideMainTable(self):
        if self.tableWidget.isHidden():
            self.tableWidget.show()
        else:
            self.tableWidget.hide()
            self.dockedEditorDriver.activate8show()

    def submitDockEdits(self):
        if self.dockedEditor.isHidden() == False:
            self.dockedEditorDriver.save2cell()

    def closeEvent(self, event):
        self.tableWidget.close()


if __name__ == '__main__':
    from chrSqlClass.guiDbWorker import GuiDbWorker
    from chrSqlClass.guiSqlTable import GuiSqlTable
    import os, sys

    dbLoc = r'C:\local_coding\CHR_packages\_db'
    dbPath = os.path.join(dbLoc, 'labnotes.sqlite')
    localLoc = r'C:\local_coding\~temp'

    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    worker = GuiDbWorker(dbPath, localLoc)

    table = GuiSqlTable(worker, 's')
    table.genTableWidget()

    window = TableWindow(table.widget)
    window.showMaximized()

    sys.exit(app.exec_())
