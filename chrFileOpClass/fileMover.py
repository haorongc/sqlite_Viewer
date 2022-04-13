import os
import shutil
from send2trash import send2trash
from chrSupport.basicFun import dateTimeStamp
from chrFileOpClass.fileInfo import FileInfo


class FileMover:
    def makeDirIfnotExist(self, loc):
        if os.path.isdir(loc) == False:
            os.makedirs(loc)

    def safeMoveFileInfo2loc(self, fileInfo, destLoc, dupLoc=None, want2overwriteOldDupItem=False):
        path = fileInfo.path
        self.safeMovePath2loc(path, destLoc, dupLoc, want2overwriteOldDupItem)
        # self.newFileInfo =

    def safeMovePath2loc(self, path, destLoc, dupLoc=None, want2overwriteOldDupItem=False):
        fname = os.path.basename(path)
        destPath = os.path.join(destLoc, fname)
        success = self.safeMovePath2path(path, destPath, dupLoc, want2overwriteOldDupItem)

    def safeMovePath2path(self, path, destPath, dupLoc=None, want2overwriteOldDupItem=False):
        dstLoc = os.path.dirname(destPath)
        self.makeDirIfnotExist(dstLoc)
        if dupLoc:
            self.makeDirIfnotExist(dupLoc)

        if not os.path.exists(destPath):
            # dest slot is open. move normally
            try:
                shutil.move(path, destPath)
            except:
                print(f'error at moving {path} to destination')
                self.moveSuccess = False
            else:
                self.moveSuccess = True
        else:
            # dest slot is taken. normal move should be failed
            # signal failure
            self.moveSuccess = False
            fname = os.path.basename(path)
            print(f'duplicated item: {fname}')

            # take care of dupItem
            if dupLoc == None:
                # no dupLoc given, can't move to dup loc
                return
            else:
                # dup loc is given, try moving to dup loc
                newPath4dup = os.path.join(dupLoc, fname)
                if os.path.exists(newPath4dup):
                    # dup slot taken, want to overwrite, delete the old dup item
                    if want2overwriteOldDupItem:
                        # open up dup slot
                        send2trash(newPath4dup)
                    else:
                        # dup slot taken, but don't want to overwrite, do nothing
                        return
                    # dup slot open or will overwrite, move to dup slot
                # dup slot open at this point, move item to dup slot
                try:
                    shutil.move(path, newPath4dup)
                except:
                    print('failed to move and overwrite old dup item')
                    return


    def genDerivitivePath(self, path, newLoc=None, prefix=None, suffix=None, separator='', newExt=None):
        fileInfo = FileInfo(path)
        loc, fname = fileInfo.loc, fileInfo.fname
        nname, ext = fileInfo.nname, fileInfo.ext

        if newLoc == None:
            newLoc = loc
        if newExt == None:
            newExt = ext

        if prefix:
            nname = prefix + separator + nname
        if suffix:
            nname = nname + separator + suffix

        newFname = nname + newExt
        newPath = os.path.join(newLoc, newFname)
        return newPath


if __name__ == '__main__':
    srcLoc = r'C:\Users\thinkbanny\Desktop\file moving mock'
    dstLoc = os.path.join(srcLoc, 'dest')
    dupLoc = os.path.join(srcLoc, 'dup')
    srcPath = os.path.join(srcLoc, '1')

    mover = FileMover()
    mover.safeMovePath2loc(srcPath, dstLoc, dupLoc=dupLoc)
    print(mover.moveSuccess)
