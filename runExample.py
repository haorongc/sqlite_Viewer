from chrQtClass.multiTableViewer import MultiTableViewer

if __name__ == '__main__':
    from chrSqlClass.guiDbWorker import GuiDbWorker
    import os, sys

    dbPath = os.path.join('_db', 'example.sqlite')
    localLoc = r'C:\local_coding\~temp'

    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    viewer = MultiTableViewer(dbPath, guiTableNames=['student', 'class'], localLoc=None )

    viewer.showMaximized()

    sys.exit(app.exec_())