from chrSupport.basicFun import dprt
from chrQtClass.qtFun import addShortcut
from functools import partial
from chrQtClass.textInputDialog import TextInputDialog
import pyperclip


class MultiTableBaseDriver:  #
    callingTableIndex = None
    callingTableName = None
    callingTable = None

    def __init__(self, multiTableViewer):
        self.multiTableViewer = multiTableViewer
        self.dbWorker = multiTableViewer.dbWorker
        self.guiTables = multiTableViewer.guiTables
        self.guiTableNames = multiTableViewer.guiTableNames


    def findCallingTable(self):
        self.callingTableIndex = self.multiTableViewer.currentTableIndex()
        self.callingTableName = self.guiTableNames[self.callingTableIndex]
        self.callingTable = self.guiTables[self.callingTableIndex]
