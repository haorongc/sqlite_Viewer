from chrQtClass.qtFun import addShortcut
from chrQtClass.tableWidget8sub.cellEditor import CellEditor


class CellEditorDriver():  # QPlainTextEdit, QTextEdit
    def __init__(self, tableWidget):
        super().__init__()
        self.tableWidget = tableWidget
        self.tableView = tableWidget.tableView
        self.cellEditor = CellEditor()
        tableWidget.cellEditor = self.cellEditor
        self.selectionDriver = tableWidget.selectionDriver
        self.selectedIndex = None
        self.model = tableWidget.model
        self.flagsEditLock = tableWidget.configDriver.flagsEditLock

        self.tableView.selectionModel().selectionChanged.connect(self.react2newSelection)
        self.model.dataChanged.connect(self.load6cell)

        self.setupShortCuts()

    def react2newSelection(self):
        # don't react if dock is hidden
        if self.cellEditor.isHidden():
            return

        # dock editor is active
        # self.saveDockedEditor()  # editor to self(old) index
        self.selectedIndex = self.selectionDriver.oneModelIndex6selection()
        self.load6cell()

    def enterDockedEditer(self):
        self.activate8show()

        self.cellEditor.selectAll()

    def hasEdit(self):
        if self.cellEditor.hasFocus() == False:
            return False
        else:
            return self.textChanged()

    def textChanged(self):

        self.editorText = self.cellEditor.toPlainText()
        if self.editorText == self.prevTableText:
            return False
        else:
            return True

    def load6cell(self):
        if self.selectedIndex == None:
            return

        tableData = self.selectionDriver.data6modelIndex(self.selectedIndex)
        col = self.selectedIndex.column()
        flagEditLocked = self.flagsEditLock[col]
        self.cellEditor.setEditLocked(flagEditLocked)

        if tableData == None:
            tableText = ''  # None '' conversion, preserved None in table
        else:
            tableText = str(tableData)
        self.prevTableText = tableText
        self.cellEditor.setPlainText(tableText)
        title = self.selectionDriver.oneTitle6selection()  # title of selected cell
        self.cellEditor.setWindowTitle(str(title))

    def save2cell(self):
        if self.selectedIndex == None:
            return
        col = self.selectedIndex.column()
        if self.flagsEditLock[col]:
            return  # dont send to edit protected columns

        # have a selected and editable cell to save to
        # only update if edits have happened inside docked editor
        if self.textChanged():
            self.cellEditor.saveCursor()
            self.selectionDriver.setData(self.selectedIndex, self.editorText)
            self.cellEditor.reloadCursor()

    def save8exit(self):
        self.save2cell()
        self.tableView.setFocus()

    def discard8exit(self):
        self.load6cell()
        self.tableView.setFocus()

    def activate8show(self):
        self.isActive = True
        self.cellEditor.show()
        self.selectedIndex = self.selectionDriver.oneModelIndex6selection()
        self.load6cell()
        self.cellEditor.setFocus()

    def deactivate8hide(self):
        self.deactivate()
        self.cellEditor.hide()

        if self.tableWidget.isHidden():
            self.tableWidget.show()
        self.tableView.setFocus()

    def deactivate(self):
        self.isActive = False
        self.save2cell()
        self.selectedIndex = None

    def save8go2Next(self):
        self.save8exit()

    def setupShortCuts(self):
        addShortcut(self.cellEditor, 'Escape', self.discard8exit)
        addShortcut(self.cellEditor, 'Ctrl+return', self.save2cell)
        addShortcut(self.cellEditor, 'Ctrl+n', self.save8go2Next)  # not working
        addShortcut(self.tableView, 'F3', self.enterDockedEditer)
        addShortcut(self.tableView, 'Return', self.enterDockedEditer)

    def probeFun(self):
        print('probe fun called in docked edit coordinator')
