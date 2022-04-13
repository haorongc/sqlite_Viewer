import os
import re
import shutil
import unicodedata
import pathlib
import datetime
from chrSupport.basicFun import dateTimeStamp


class FileInfo():
    dateFirstRegex = re.compile(r'(^\d{6})([a-zA-Z]?)([-_.\s]*)')
    remark = ''  # no remark by default

    picExts = {'.pdf', '.jpg', '.png', '.tif', '.tiff', '.gif', '.bmp'}
    audioExts = {'.mp3', '.wma'}
    pdfExts = {'.pdf'}

    def __init__(self, loc, fname=None):
        if fname == None:
            # passed a path
            self.path = loc
            self.loc, self.fname = os.path.split(self.path)
        else:
            # passed loc and fname
            self.loc = loc
            self.fname = fname
            self.path = os.path.join(loc, fname)

        # path, loc, fname already parsed
        self.nname, self.ext = os.path.splitext(self.fname)

    def isAudioFile(self):
        return self.isOfFileType(self.audioExts)

    def isPdf(self):
        return self.isOfFileType(self.pdfExts)

    def isPicFile(self):
        return self.isOfFileType(self.picExts)

    def isOfFileType(self, exts):
        if self.isFile() == False:
            return False

        if self.ext.lower() in exts:
            return True
        else:
            return False

    def isFile(self):
        return os.path.isfile(self.path)

    def isDir(self):
        return os.path.isdir(self.path)

    def parseDate(self):
        nname = self.nname
        # extract date
        match = self.dateFirstRegex.search(nname)
        if match:
            self.date, letterModifier, separator = match.groups()
            self.datedId = self.date + letterModifier
            datePrefix = self.datedId + separator
            self.descriptor9date = nname.replace(datePrefix, '')
            self.tModStr = self.date
        else:
            self.date = self.getModDateStr()
            self.datedId = None
            self.descriptor9date = nname
            self.tModStr = self.getModTimeStr()

    def reflectMove2loc(self, loc):
        self.loc = loc
        self.path = os.path.join(loc, self.fname)

    def getModDateTime(self):
        pathObj = pathlib.Path(self.path)
        mTime = pathObj.stat().st_mtime
        mTime = datetime.datetime.fromtimestamp(mTime)
        return mTime

    def getModDateStr(self):
        mTime = self.getModDateTime()
        dateStamp = dateTimeStamp(now=mTime, start=2, len=6)
        return dateStamp

    def getModTimeStr(self):
        mTime = self.getModDateTime()
        timeStamp = dateTimeStamp(now=mTime, start=2, len=13)
        return timeStamp

    def addSuffix2nname(self, suffix):
        newNname = self.nname + suffix
        newFname = newNname + self.ext
        newPath = os.path.join(self.loc, newFname)
        try:
            shutil.move(self.path, newPath)
        except:
            print(f'failed to add suffix {suffix}')
            self.changeSuccess = False
        else:
            self.nname = newNname
            self.fname = newFname
            self.path = newPath
            self.changeSuccess = True

    def cleanFname(self):
        cleanExt = self.ext.lower()
        cleanNname = self.cleanStr6str(self.nname)
        if cleanExt == self.ext and cleanNname == self.nname:
            self.changeSuccess = True
            return  # no need to change fname
        else:
            # needs cleaning
            newFname = cleanNname + cleanExt
            newPath = os.path.join(self.loc, newFname)
            try:
                shutil.move(self.path, newPath)
            except:
                print(f'failed to rename {self.fname} to {newFname}')
                self.changeSuccess = False
            else:
                # renaming worked, update record
                self.ext = cleanExt
                self.nname = cleanNname
                self.fname = cleanNname + cleanExt
                self.path = newPath
                self.changeSuccess = True

    def cleanStr6str(self, raw):
        # clean up a string into one that can be used as file name
        raw = str(raw)
        raw = unicodedata.normalize('NFKC', raw)
        raw = re.sub(r'[^\w\s.&+\'\",-\[\]\(\)]', '_', raw)
        raw = re.sub(r'[\s]+', r' ', raw)  # r'[-_\s]+'
        raw = raw.strip()
        return raw


if __name__ == '__main__':
    # path = r'docs.sqlite_bit_default.csv'
    path = r"C:\Users\thinkbanny\Dropbox\transfer\wiki\Albumin.pdf"
    fileInfo = FileInfo(path)
    fileInfo.parseDate()
    tMod = fileInfo.date
    print(tMod)
