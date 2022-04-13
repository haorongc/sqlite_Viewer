from chrSqlClass.sqlite3Worker import Sqlite3worker
from chrSupport.basicFun import dateTimeStamp
from chrFileOpClass.fileMover import FileMover
from chrFileOpClass.fileInfo import FileInfo
import shutil
from chrSupport.lengthLimitedStack import LengthLimitedStack


class ReversibleDbWorker(Sqlite3worker):
    maxUndoPoints = 5
    undoPoints = LengthLimitedStack(maxLen=maxUndoPoints)
    redoPoints = LengthLimitedStack(maxLen=maxUndoPoints)
    fileMover = FileMover()

    def __init__(self, dbPath, backupLoc=None):
        super().__init__(dbPath)

        # parse db path, info for gen backup copy
        dbFileInfo = FileInfo(self.dbPath)
        self.dbNname = dbFileInfo.nname
        # prep backup and redo
        if backupLoc==None:
            self.backupLoc = dbFileInfo.loc  # same folder as db
        else:
            self.backupLoc = backupLoc

    def redo(self, description=None):
        print(f'redo not implemented')

    def loadPrevUndoPoint(self, description=None):
        # self.saveDb2RedoPoints(description)

        undoPoint = self.undoPoints.safePop()
        if undoPoint != None:
            dbPath2use, description = undoPoint
            print(f'undo to ~{description}~')
            self.overwriteDb6path(dbPath2use)
        else:
            print('no undo point')

    def genUndoPoint(self, description=None):
        backedDbPath = self.genDbCopy(description)

        if backedDbPath != None:
            undoPoint = (backedDbPath, description)
            self.undoPoints.append(undoPoint)

    # def saveDb2RedoPoints(self, description=None):
    #     backedDbPath = self.backedUpFile(description)
    #
    #     if backedDbPath != None:
    #         self.redoPoints.append(backedDbPath)

    def overwriteDb6path(self, path2use):
        self.deactivate()
        shutil.move(path2use, self.dbPath)
        self.activate()

    def genDbCopy(self, description=None):
        # back up before modification
        timeStamp = dateTimeStamp()
        backedDbPath = self.fileMover.genDerivitivePath(self.dbPath, newLoc=self.backupLoc,
                                         prefix=timeStamp, suffix=description, separator='-')
        try:
            shutil.copy(self.dbPath, backedDbPath)
        except:
            print(f'failed to copy {dbPath}')
            return None
        else:
            return backedDbPath


if __name__ == '__main__':
    from CHR_local import path_definition
    import os

    dropboxLoc = path_definition.dropbox_loc
    dbPath = os.path.join(dropboxLoc, '_db', 'books.sqlite')
    localLoc = r'C:\local_coding\~temp'

    dbWorker = ReversibleDbWorker(dbPath, backupLoc=localLoc)