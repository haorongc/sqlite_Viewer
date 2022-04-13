from PyQt5.QtSql import QSqlTableModel


class SqlTableModel(QSqlTableModel):  #
    def refresh(self):
        self.loadData()
        # if necessary, make this a faster refresh that not necessarily retrieve all enries
        # self.select()

    def loadData(self):
        self.select()
        while self.canFetchMore():
            self.fetchMore()
