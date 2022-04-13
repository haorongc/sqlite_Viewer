#! python3.8
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel
from chrQtClass.qtFun import toggleVisibility


class PicPreviewer(QLabel):
    def __init__(self):
        super().__init__()
        # self.setMinimumSize(400,300)
        self.setAlignment(Qt.AlignCenter)
        self.isActive = False
        self.picPath = None
        # self.setScaledContents(True)

    def toggleActivity(self):
        if self.isActive:
            self.deactivate()
        else:
            self.activate()

    def deactivate(self):
        self.hide()
        self.isActive = False

    def activate(self):
        self.show()
        self.isActive = True
        self.refreshDisplay()

    def update6picPath(self, picPath):
        if self.isActive:
            if picPath != self.picPath:
                # refresh only if picPath has changed
                self.picPath = picPath
                self.refreshDisplay()
        else:
            # window is not active, just save pic Path, don't waste computing power to display
            self.picPath = picPath

    def refreshDisplay(self):
        pix = QPixmap()
        pix.load(self.picPath)
        pix = pix.scaled(self.size(), Qt.KeepAspectRatio, Qt.FastTransformation)
        self.setPixmap(pix)


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
