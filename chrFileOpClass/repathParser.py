import os
# from chrFileOpClass.fileMover import FileMover
#
# fileMover = FileMover()
from send2trash import send2trash
from bookManager.locsKeeper import LocsKeeper


class RepathParser():
    def __init__(self):
        # self.locsKeeper = LocsKeeper()
        self.LC_loc = LocsKeeper.LC_loc

    def path6Dict(self, pathDict):
        LC = pathDict['LC']
        repath = pathDict['repath']

        path = self.path6repath(LC, repath)
        return path

    def path6repath(self, LC, repath):
        if LC and repath:
            loc = self.LC_loc[LC]
            path = os.path.join(loc, repath)
            return path
        else:
            return None

    def repath6path(self, LC, path):
        loc = self.LC_loc[LC]
        repath = os.path.relpath(path, loc)
        if repath == '.':
            return ''
        else:
            return repath
