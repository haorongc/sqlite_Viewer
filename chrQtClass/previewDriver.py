#! python3.8
import sys, os

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel
from chrSqlClass.sqlTable import SqlTable
from docApp8sub.locsKeeper import LocsKeeper
from chrQtClass.qtFun import addShortcut
from chrQtClass.picPreviewer import PicPreviewer


class PreviewDriver:
    def __init__(self, sqlApp):
        self.dbWorker = sqlApp.dbWorker
        self.picPreviewer = PicPreviewer()
        self.picPreviewer.setMinimumSize(600, 500)
        # self.picPreviewer.show()
        self.picTable = sqlApp.guiTables['pic']
        self.fileTable = sqlApp.guiTables['file']
        self.linkTable = SqlTable(self.dbWorker, 'ent_file')
        self.picTable.widget.tableView.selectionModel().selectionChanged.connect(self.updatePreview)
        addShortcut(self.picTable.widget, 'Shift+Alt+v', self.picPreviewer.toggleActivity)
        addShortcut(self.picPreviewer, 'Escape', self.picPreviewer.toggleActivity)

    def updatePreview(self):
        picId = self.picTable.oneId6selection()
        searchDict = {'berlType': 'pic', 'berlId': picId}
        fileId = self.linkTable.oneValue6searchDict('fileId', searchDict)
        pathDict = self.fileTable.oneDict6searchDict(['LC', 'repath'],
                                                     {'id': fileId})
        LC = pathDict['LC']
        repath = pathDict['repath']
        loc = LocsKeeper.LC_loc[LC]
        picPath = os.path.join(loc, repath)
        self.picPreviewer.update6picPath(picPath)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet('''
    # 	QWidget {
    # 		font-size: 30px;
    # 	}
    # ''')

    myApp = PicPreviewer()
    myApp.refreshDisplay('IMG_5114.jpg')
    # myApp.show6path('1625152899183.mp4')
    myApp.showMaximized()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')
