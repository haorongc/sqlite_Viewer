from chrSupport.basicFun import dprt


# from chrSupport.dictWorker import DictWorker
# dictWorker = DictWorker()

class SqlTable:
    def __init__(self, sqlite3Worker, tableName):
        # dprt('creating sqlTable obj')
        self.dbWorker = sqlite3Worker
        self.tableName = tableName
        self.allFields = self.dbWorker.allFields6tableName(self.tableName)
        self.nonIdFields = self.allFields.copy()
        try:
            self.nonIdFields.remove('id')
        except:
            pass

    def getMaxId(self):
        self.dbWorker.exeQuery(f'Select MAX(id) from {self.tableName}')
        row = self.dbWorker.cur.fetchone()
        maxId = row[0]
        if maxId == None:
            return 0
        else:
            return maxId

    def uniqueInsertOrUpdate6dict(self, infoDict, uniqueFields=None):
        tableName = self.tableName
        allowedFields = self.allFields
        self.dbWorker.uniqueInsertOrUpdate6dict(tableName, infoDict, uniqueFields,
                                                allowedFields)
        self.insertedId = self.dbWorker.insertedId

    def uniqueInsertOrIgnore6dict(self, infoDict, uniqueFields=None):
        tableName = self.tableName
        allowedFields = self.allFields
        self.dbWorker.uniqueInsertOrIgnore6dict(tableName, infoDict, uniqueFields,
                                                allowedFields)
        self.insertedId = self.dbWorker.insertedId

    def insert6dict(self, infoDict, allowIgnore=False):
        tableName = self.tableName
        allowedFields = self.allFields
        self.dbWorker.insert6dict(tableName, infoDict,
                                  allowedFields, allowIgnore=allowIgnore)
        self.insertedId = self.dbWorker.insertedId

    def insertOrIgnore6dict(self, infoDict):
        self.insert6dict(infoDict, allowIgnore=True)

    def update6dictPair(self, valueDict, searchDict, searchFields=None):
        tableName = self.tableName
        allowedFields = self.allFields
        self.dbWorker.update6dictPair(tableName, valueDict, searchDict,
                                      searchFields=searchFields, allowedFields=allowedFields)

    def delete6searchDict(self, searchDict, searchFields=None):
        tableName = self.tableName
        self.dbWorker.delete6searchDict(tableName, searchDict, searchFields)

    def allDicts6field(self,fields2request):
        if fields2request == None:
            fields2request = self.allFields
        tableName = self.tableName
        return self.dbWorker.allDicts6table(tableName, fields2request)

    def allValues6field(self, field2request):
        tableName = self.tableName
        return self.dbWorker.allValues6table(tableName, field2request)

    def values6searchDict(self, field2request, searchDict=None, searchFields=None):
        if searchDict== None:
            return self.allValues6field()

        tableName = self.tableName
        return self.dbWorker.values6searchDict(tableName, field2request, searchDict, searchFields=None)
        df = self.dbWorker.df6searchDict(tableName, [field2request], searchDict, searchFields)
        values = df.to_dict('list')
        values = values[field2request]
        return values

    def oneValue6searchDict(self, field2request, searchDict, searchFields=None):
        values = self.values6searchDict(field2request, searchDict, searchFields)
        if len(values) > 0:
            return values[0]
        else:
            return None

    def oneDict6searchDict(self, fields2request, searchDict, searchFields=None):
        if fields2request == None:
            fields2request = self.allFields
        dicts = self.dicts6searchDict(fields2request, searchDict, searchFields)
        if len(dicts) > 0:
            return dicts[0]
        else:
            return None

    def dicts6searchDict(self, fields2request, searchDict, searchFields=None):
        if fields2request==None:
            fields2request=self.allFields
        tableName = self.tableName
        df = self.dbWorker.df6searchDict(tableName, fields2request, searchDict, searchFields)
        dfDicts = df.to_dict('records')
        return dfDicts


if __name__ == '__main__':
    from chrSqlClass.reversibleDbWorker import ReversibleDbWorker
    from chrSqlClass.sqlite3Worker import Sqlite3worker
    import os, sys

    dbLoc = r'C:\local_coding\CHR_packages\_db'
    dbPath = os.path.join(dbLoc, 'docs.sqlite')
    # localLoc = r'C:\local_coding\~temp'

    from PyQt5.QtWidgets import QApplication

    # app = QApplication(sys.argv)

    worker = Sqlite3worker(dbPath)
    worker.activate()
    # worker = DbWorker(dbPath)

    table = worker.getTable('lec')
    table2 = worker.getTable('lec')


    resultDicts = table2.dicts6searchDict(None, {'place': 'bats', 'who':'Emi Lutz'})
    for resultDict in resultDicts:
        print(resultDict)

    # sys.exit(app.exec_())
