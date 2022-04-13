import os
from chrFileOpClass.fileInfo import FileInfo


class FileScanner:
    def scanTree(self, lookupLoc):
        # results can be called by self.collectedFileInfos
        self.collectedFileInfos = []
        rootInfo = FileInfo(lookupLoc)
        self.visit(rootInfo)

    def scanDirectLeaves(self, lookupLoc):
        # results can be called by self.collectedFileInfos
        self.collectedFileInfos = []
        for fname in os.listdir(lookupLoc):
            fileInfo = FileInfo(lookupLoc, fname)
            if self.judged2exclude(fileInfo):
                continue
            else:
                # no obvious need to exclude, check if should be included
                if self.judged2include(fileInfo):
                    self.collectedFileInfos.append(fileInfo)

    def judged2exclude(self, fileInfo):
        fname = fileInfo.fname
        if fname.startswith('_'):
            return True
        else:
            return False

    def addRemark(self, str):
        for fileInfo in self.collectedFileInfos:
            fileInfo.remark = str

    def judged2include(self, fileInfo):
        return True

    def visit(self, parentInfo):
        if self.judged2exclude(parentInfo):
            return
        else:
            if self.judged2include(parentInfo):
                self.collectedFileInfos.append(parentInfo)
            if parentInfo.isDir():
                parentLoc = parentInfo.path
                for fname in os.listdir(parentLoc):
                    leafInfo = FileInfo(parentLoc, fname)
                    self.visit(leafInfo)
