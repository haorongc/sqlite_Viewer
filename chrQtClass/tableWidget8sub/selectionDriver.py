class SelectionDriver():
    def __init__(self, widget):
        self.tableView = widget.tableView
        self.model = widget.tableView.model()

        self.idCol = widget.idCol
        self.titleCol = widget.titleCol
        self.allFields = widget.allFields

    def setData(self, index, data):
        self.model.setData(index, data)
        pass

    def data6modelIndex(self, index, col=None):
        if index == None:
            return None
        else:
            if col == None:
                return self.model.data(index)
            else:
                row = index.row()
                shiftedIndex = self.model.index(row, col)
                data = self.model.data(shiftedIndex)
                return data

    def id6modelIndex(self, index):
        return self.data6modelIndex(index, self.idCol)

    def idSet6selection(self):
        idSet = set()
        for index in self.tableView.selectedIndexes():
            id = self.id6modelIndex(index)
            idSet.add(id)
        return idSet


    def ids6selection(self):
        idSet = self.idSet6selection()
        ids = list(idSet)
        return ids

    def oneField6selection(self):
        index = self.oneModelIndex6selection()
        col = index.column()
        return self.allFields[col]

    def colSet6selection(self):
        colSet = set()
        for index in self.tableView.selectedIndexes():
            col = index.column()
            colSet.add(col)
        return colSet

    # redundant?
    def indexBelow(self, currentIndex=None):
        # use given index, or one from tableView selection
        if currentIndex == None:
            currentIndex = self.tableView.selectedIndexes()[-1]
        r = currentIndex.row()
        c = currentIndex.column()
        if r < self.model.rowCount():
            return self.model.index(r + 1, c)
        else:
            return currentIndex

    def oneValue6selection(self):
        index = self.oneModelIndex6selection()
        value = self.data6modelIndex(index)
        return value

    def oneId6selection(self):
        index = self.oneModelIndex6selection()
        id = self.data6modelIndex(index, self.idCol)
        return id

    def oneDict6selection(self, fields2request=None):
        index = self.oneModelIndex6selection()
        if index == None:
            return None
        else:
        # something is selected,  get data from the row
            rowDict = dict()
            for col, field in enumerate(self.allFields):
                if fields2request==None or field in fields2request:
                    rowDict[field] = self.data6modelIndex(index, col)
            return rowDict

    def oneModelIndex6selection(self):
        try:
            index = self.tableView.selectedIndexes()[-1]
            return index
        except:
            return None

    def oneTitle6selection(self):
        index = self.oneModelIndex6selection()
        title = self.data6modelIndex(index, self.titleCol)
        return title

    def setIdCol(self, idCol):
        self.idCol = idCol

    def setTitleCol(self, titleCol):
        self.titleCol = titleCol
