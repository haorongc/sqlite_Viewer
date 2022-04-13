from functools import partial

from PyQt5.QtCore import Qt


class SortDriver():
    def __init__(self, tableWidget):
        self.tableView = tableWidget.tableView
        filterHeader = tableWidget.filterHeader
        self.sortCol = None
        self.defaultDescent = True

        self.sortButtons = filterHeader.sortButtons
        self.header = self.tableView.horizontalHeader()
        self.sortButtonStyles = filterHeader.sortButtonStyles

        for i, sortButton in enumerate(filterHeader.sortButtons):
            _ = partial(self.sort6Column, i)
            sortButton.clicked.connect(_)
        self.header.sectionClicked.connect(self.sort6Column)

        self.sort6Column(tableWidget.initSortCol)


    def sort6Column(self, col=None):
        # choose sort order, if column index not changed: toggle order
        if col == None:
            return
        elif col == self.sortCol:
            # sort by the same column, toggle switching order
            self.isDescent = not self.isDescent
        else:
            # clicked a diff column, use default sort order
            self.isDescent = self.defaultDescent
        # convert isDescent to sortOrder
        if self.isDescent:
            sortOrder = Qt.DescendingOrder
        else:
            sortOrder = Qt.AscendingOrder
        # perform sort
        self.tableView.sortByColumn(col, sortOrder)

        # update style indicator
        if self.sortCol != None:  # more strict: need to be within boundary
            self.sortButtons[self.sortCol].setStyleSheet(self.sortButtonStyles['normal'])
        if self.isDescent:
            self.sortButtons[col].setStyleSheet(self.sortButtonStyles['descend'])
        else:
            self.sortButtons[col].setStyleSheet(self.sortButtonStyles['ascend'])

        # finished updating style, save current indexSort
        self.sortCol = col
