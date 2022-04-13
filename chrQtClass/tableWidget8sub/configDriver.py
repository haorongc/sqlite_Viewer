# from chrSupport.basicFun import dprt
import pandas as pd
from chrQtClass.qtFun import addShortcut
from functools import partial

class ConfigDriver():
    defaultWidth = 39
    flagsEditLock = None
    widths = None

    def __init__(self, tableWidget):
        self.widget = tableWidget
        self.allFields = tableWidget.allFields
        self.nFields = tableWidget.nFields
        self.tableHeader = self.widget.tableView.horizontalHeader()

        self.field_index = tableWidget.field_index
        self.filterHeader = tableWidget.filterHeader
        self.tableView = tableWidget.tableView

        self.widths = [self.defaultWidth] * self.nFields
        self.flagsEditLock = [False] * self.nFields

        tableName = tableWidget.tableName
        dbPath = tableWidget.sqlTable.dbWorker.dbPath
        self.configPath = f'{dbPath}_{tableName}_default.csv'

        self.load8updateConfig()
        # self.parseFieldEditLock()
        self.applyEditLock()

        # self.parseColumnWidth()
        self.applyWidths()

        self.tableHeader.sectionResized.connect(self.adaptFilterWidths)
        # addShortcut(self.widget, 'Ctrl+h', self.hideSelectedCols)
        addShortcut(self.widget, 'Ctrl+l', partial(self.lockSelectedCols, True))
        addShortcut(self.widget, 'Ctrl+Shift+l', partial(self.lockSelectedCols, False))

    def lockSelectedCols(self, wantLocked):
        selectedColSet = self.widget.selectionDriver.colSet6selection()
        for col in selectedColSet:
            self.flagsEditLock[col] = wantLocked
            self.tableView.setColumnLocked(col, wantLocked)
            self.filterHeader.setColumnLocked(col, wantLocked)

    def hideSelectedCols(self):
        selectedColSet = self.widget.selectionDriver.colSet6selection()
        for col in selectedColSet:
            self.tableView.setColumnHidden(col, True)
            self.filterHeader.setColumnHidden(col, True)

    def saveConfig2file(self):
        df = pd.DataFrame(
            zip(self.allFields, self.flagsEditLock, self.widths))
        # add header for ease of reading
        df.columns = ['field', 'protected', 'width']
        df.to_csv(self.configPath)

    # def parseColumnWidth(self):
    #     self.widths = list()
    #     for field in self.allFields:
    #         width = self.field_width.get(field, self.defaultWidth)
    #         self.widths.append(width)

    # def parseFieldEditLock(self):
    #     self.editableFields = list()
    #     self.flagsEditLock = list()
    #     for field in self.allFields:
    #         protectFlag = self.field_protectFlag.get(field, False)
    #         self.flagsEditLock.append(protectFlag)
    #         if protectFlag == False:
    #             self.editableFields.append(field)
    #     # dprt(self.flagsEditLock, 'self.flagsEditLock')

    def applyEditLock(self):
        self.delegates4setting = list()
        for col, flagEditLock in enumerate(self.flagsEditLock):
            # dprt(col, 'col')
            if flagEditLock:
                self.tableView.setColumnLocked(col, True)
                self.filterHeader.setColumnLocked(col, True)  # made edit locked column appear different

    def applyWidths(self):
        for col, width in enumerate(self.widths):
            # self.filterHeader.setColumnWidth(col, width)
            self.widget.tableView.setColumnWidth(col, width)
        self.adaptFilterWidths()  # this is needed

    def load8updateConfig(self, path=None):
        if path == None:
            path = self.configPath

        try:
            df = pd.read_csv(path)
        except:
            print(f'failed to read config file: {path}')
            return

        # parse config file
        fileFields = df['field']
        fileProtectFlags = df['protected']
        fileWidths = df['width']

        for fileField, fileFlagEditLock, fileWidth in zip(fileFields, fileProtectFlags, fileWidths):
            try:
                col = self.field_index[fileField]
            except:
                pass
            else:
                # fileField is valid, use values to update
                if fileFlagEditLock:
                    self.flagsEditLock[col] = True
                self.widths[col] = fileWidth

    def adaptFilterWidths(self):
        self.measureColumnWidths()
        self.filterHeader.applyWidths(self.widths)

    def measureColumnWidths(self):
        for i in range(self.nFields):
            self.widths[i] = self.tableHeader.sectionSize(i)
