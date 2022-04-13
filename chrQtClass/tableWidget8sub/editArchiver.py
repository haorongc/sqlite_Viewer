class EditArchiver():
    editedIdSet = set()

    def __init__(self, tableWidget):
        self.tableName = tableWidget.tableName
        self.dbWorker = tableWidget.dbWorker
        self.mirrorDbWorker = self.dbWorker.mirrorDbWorker
        self.nonIdFields = tableWidget.sqlTable.nonIdFields
        self.model = tableWidget.model

        self.selectionDriver = tableWidget.selectionDriver
        tableWidget.model.dataChanged.connect(self.logEditedId)

        self.sqlTable = tableWidget.sqlTable
        self.mirrorSqlTable = self.mirrorDbWorker.getTable(self.tableName)

    def logEditedId(self, index):
        id = self.selectionDriver.id6modelIndex(index)
        self.editedIdSet.add(id)

    def clearEditLog(self):
        self.editedIdSet.clear()

    def archiveEdits(self):
        self.model.submit()
        for id in self.editedIdSet:
            searchDict = {'id': id}
            insertDict = self.mirrorSqlTable.oneDict6searchDict(self.nonIdFields, searchDict)
            self.sqlTable.update6dictPair(insertDict, searchDict)

        self.dbWorker.commit()
        self.clearEditLog()

    def hasEdits(self):
        if len(self.editedIdSet):
            return True
        else:
            return False

