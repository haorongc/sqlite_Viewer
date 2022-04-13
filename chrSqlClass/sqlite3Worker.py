import sqlite3
import pandas as pd

from chrSqlClass.sqlTable import SqlTable
from chrSupport.basicFun import dprt, dateTimeStamp
import pathlib
from chrSupport.dictWorker import DictWorker
from chrSqlClass.queryTextWorker import QueryTextWorker
dictWorker = DictWorker()



queryTextWorker = QueryTextWorker()


class Sqlite3worker:
    conn = None
    cur = None
    insertedId = 0
    tableName_table = dict()

    def __init__(self, dbPath):
        pathObj = pathlib.Path(dbPath)
        pathObj = pathObj.resolve()
        self.dbPath = str(pathObj)
        self.activate()

    def uniqueInsertOrUpdate6dict(self, tableName, infoDict, uniqueFields,
                                  allowedFields=None):
        found = self.found6searchDict(tableName, infoDict, searchFields=uniqueFields)
        if found:
            # update matching rows
            self.insertedId = 0  # to indicate no insertion
            valueDict = dictWorker.copy8excludeFields(infoDict,
                                                      uniqueFields)  # unique fields match and no need to update
            self.update6dictPair(tableName, valueDict=valueDict, searchDict=infoDict,
                                 searchFields=uniqueFields, allowedFields=allowedFields)
            return
        else:
            self.insert6dict(tableName, infoDict, allowedFields=allowedFields)

    def uniqueInsertOrIgnore6dict(self, tableName, infoDict, uniqueFields=None,
                                  allowedFields=None):
        found = self.found6searchDict(tableName, infoDict, searchFields=uniqueFields)
        if found:
            self.insertedId = 0
            return
        else:
            self.insert6dict(tableName, infoDict, allowedFields=allowedFields)

    def insertOrIgnore6dict(self, tableName, infoDict, allowedFields=None):
        self.insert6dict(tableName, infoDict, allowedFields=allowedFields, allowIgnore=True)

    def insert6dict(self, tableName, infoDict, allowedFields=None, allowIgnore=False):
        fields, values = dictWorker.conciseKeysValues6dict(infoDict, allowedFields)
        if len(fields) == 0:
            return None

        fieldsString = ','.join(fields)
        questions = ['?'] * len(fields)
        questionsString = ','.join(questions)

        if allowIgnore:
            ignorePhrase = 'or ignore'
        else:
            ignorePhrase = ''
        query = f'insert {ignorePhrase} into {tableName} ({fieldsString}) values({questionsString})'

        self.exeQuery(query, values)
        self.insertedId = self.cur.lastrowid
        # dprt(self.insertedId, 'self.insertedId')

    def allFields6tableName(self, tableName):
        # leaves conn cur the same opene/closed state as before calling
        # try:
        self.exeQuery(f"PRAGMA table_info({tableName})")
        columnInfos = self.cur.fetchall()
        #     # if this works, no closing conn cur needed
        # except:
        #     with self.ActivateConnCur(self):
        #         self.exeQuery(f"PRAGMA table_info({tableName})")
        #         columnInfos = self.cur.fetchall()

        allFields = [info[1] for info in columnInfos]
        return allFields

    def update6dictPair(self, tableName, valueDict, searchDict, searchFields=None, allowedFields=None):
        queryTextWorker.importSearchDict(searchDict, searchFields)
        whereClause = queryTextWorker.genWhereClause()
        params = queryTextWorker.genParams()

        self.update6dict8where(tableName, valueDict,
                               whereClause=whereClause, params=params,
                               allowedFields=allowedFields)

    def update6dict8where(self, tableName, newValueDict, whereClause='', params=[], allowedFields=None):
        fields, values = dictWorker.conciseKeysValues6dict(newValueDict, allowedFields)
        if len(fields) == 0:
            # print('no field to update')
            return

        setPhrases = []
        for field in fields:
            setPhrase = f'{field}=?'
            setPhrases.append(setPhrase)
        setSentence = ','.join(setPhrases)

        query = f'update {tableName} set {setSentence} {whereClause}'
        self.exeQuery(query, tuple(values) + tuple(params))

    def delete6searchDict(self, tableName, searchDict, searchFields=None):
        queryTextWorker.importSearchDict(searchDict, searchFields)
        whereClause = queryTextWorker.genWhereClause()
        params = queryTextWorker.genParams()
        self.delete6where(tableName, whereClause=whereClause, params=params)

    def delete6where(self, tableName, whereClause='', params=[]):
        query = f'delete from {tableName} {whereClause}'
        self.exeQuery(query, params)

    def values6searchDict(self, tableName, field2request,
                          searchDict, searchFields=None):
        df = self.df6searchDict(tableName, [field2request], searchDict, searchFields)
        values = df.to_dict('list')
        values = values[field2request]
        return values

    def found6searchDict(self, tableName, searchDict, searchFields=None):
        df = self.df6searchDict(tableName, ['*'], searchDict, searchFields=searchFields)

        if len(df) == 0:
            # dprt('not found')
            return False
        else:
            # dprt('found')
            return True

    # def genJoinTable(self, destTableName, tableNames, joinFields):
    #     query = f'create table {destTableName} as select'
    #     self.exeQuery()

    def dicts6searchDict(self, tableName, fields2request,
                         searchDict, searchFields=None):
        df = self.df6searchDict(tableName, fields2request, searchDict, searchFields)
        dfDicts = df.to_dict('records')
        return dfDicts

    def df6searchDict(self, tableName, fields2request, searchDict, searchFields=None):
        queryTextWorker.importSearchDict(searchDict, searchFields)
        whereClause = queryTextWorker.genWhereClause()
        params = queryTextWorker.genParams()

        df = self.df6where(tableName, fields2request, whereClause, params)
        return df

    def allDicts6table(self, tableName, fields2request):
        df = self.df6where(tableName, fields2request)
        dfDicts = df.to_dict('records')
        return dfDicts

    def allValues6table(self, tableName, field2request):
        df = self.df6where(tableName, [field2request])
        values = df.to_dict('list')
        values = values[field2request]
        return values

    def df6where(self, tableName, fields2request, whereClause=None, params=None):
        fieldsString = ', '.join(fields2request)

        query = f'select {fieldsString} from {tableName}'
        if whereClause:
            query = f'{query} {whereClause}'
            df = pd.read_sql(query, self.conn, params=params)
        else:
            query = f'{query}'
            df = pd.read_sql(query, self.conn)
        return df

    def exeQuery(self, *args):
        # dprt(args[0])
        # if len(args) > 1:
        #     dprt(args[1])
        self.cur.execute(*args)

    def activate(self):
        self.conn = sqlite3.connect(self.dbPath)
        self.cur = self.conn.cursor()

    def deactivate(self, commit=False):
        if commit:
            self.commit()
        self.cur.close()
        self.conn.close()

    def commit(self):
        self.conn.commit()

    class ActivateConnCur():
        def __init__(self, obj, activate=True, commit=False):
            self.obj = obj
            self.want2commit = commit
            self.want2activate = activate

        def __enter__(self):
            if self.want2activate:
                self.obj.conn = sqlite3.connect(self.obj.dbPath)
                self.obj.cur = self.obj.conn.cursor()

        def __exit__(self, exc_type, exc_value, exc_traceback):
            if self.want2activate:
                if self.want2commit:
                    self.obj.conn.commit()
                self.obj.cur.close()
                self.obj.conn.close()

    def getTable(self, tableName):
        try:
            table = self.tableName_table[tableName]
            dprt('use the sqlTable generated before')
            return table
        except:
            table = SqlTable(self, tableName)
            self.tableName_table[tableName] = table
            return table


if __name__ == '__main__':
    from CHR_local import path_definition
    import os

    dropboxLoc = path_definition.dropbox_loc
    dbPath = os.path.join(dropboxLoc, '_db', 'books.sqlite')
    localLoc = r'C:\local_coding\~temp'

    sqlWorker = Sqlite3worker(dbPath)

    query = 'select item.LC'

    sqlWorker.deactivate()
